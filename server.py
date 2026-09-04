import socket    
import select    
import sys       

HOST = "127.0.0.1"  
PORT = 5555       

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    servidor.bind((HOST, PORT))   
    servidor.listen()          
    print(f"Servidor escuchando en {HOST}:{PORT} ...")
except OSError as e:
    print(f"No se pudo iniciar el servidor: {e}")
    sys.exit()

sockets = [servidor]  
nombres = {}         
pendientes = []       

def broadcast(mensaje, emisor):
    for s in sockets:                        
        if s != servidor and s != emisor:  
            try:
                s.send(mensaje.encode())      
            except:
                desconectar(s)                 

def desconectar(s):
    nombre = nombres.get(s, "Anonimo")      
    print(f"{nombre} se desconecto.")
    broadcast(f"{nombre} se fue del chat.", s) 
    if s in sockets:                          
        sockets.remove(s)
    if s in nombres:
        del nombres[s]
    if s in pendientes:                       
        pendientes.remove(s)     
    s.close()                                  

print("Esperando conexiones...")

try:
    while True:   
        try:
            listos, _, con_error = select.select(sockets + pendientes, [], sockets + pendientes)
        except Exception as e:
            print(f"Error en select: {e}")
            break

        for s in con_error:                  
            print("Un socket tuvo un error.")
            desconectar(s)

        for s in listos:                     

            if s == servidor:
                try:
                    cliente, direccion = servidor.accept()  
                    pendientes.append(cliente)               
                    print(f"Nueva conexion desde {direccion[0]}:{direccion[1]}, esperando nombre...")
                except Exception as e:
                    print(f"Error al aceptar conexion: {e}")

            elif s in pendientes:
                try:
                    datos = s.recv(1024)       

                    if datos:
                        nombre = datos.decode()            
                        nombres[s] = nombre                
                        pendientes.remove(s)               
                        sockets.append(s)                  

                        print(f"{nombre} se conecto.")
                        broadcast(f"{nombre} entro al chat!", s)            
                        s.send("Conectado! Ya podes escribir.".encode())   
                    else:
                        pendientes.remove(s)
                        s.close()
                except Exception as e:
                    print(f"Error al recibir nombre: {e}")
                    pendientes.remove(s)
                    s.close()

            else:
                try:
                    mensaje = s.recv(1024)     

                    if mensaje:
                        texto = mensaje.decode()
                        nombre = nombres.get(s, "Desconocido")

                        if texto == "/exit":            
                            desconectar(s)
                        else:
                            print(f"[{nombre}]: {texto}")
                            broadcast(f"[{nombre}]: {texto}", s)   
                    else:
                        desconectar(s)

                except Exception as e:
                    print(f"Error al recibir mensaje: {e}")
                    desconectar(s)

except KeyboardInterrupt:
    print("\nCerrando el servidor...")

    for s in list(sockets) + list(pendientes):  
        if s != servidor:
            try:
                s.send("El servidor se cerro.".encode())  
            except:
                pass       
            s.close()

    servidor.close()      
    print("Servidor cerrado. Hasta luego!")