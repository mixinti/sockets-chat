import socket     
import threading 
import sys        
import time       

HOST = "127.0.0.1"  
PORT = 5555         

MAX_REINTENTOS = 3   

nombre = input("Ingresa tu nombre de usuario: ").strip()   
if not nombre:        
    nombre = "Anonimo"

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

conectado = False    

for intento in range(1, MAX_REINTENTOS + 1):   
    try:
        cliente.connect((HOST, PORT))   
        conectado = True                
        break                          
    except Exception as e:
        print(f"Intento {intento}/{MAX_REINTENTOS} fallido: {e}")
        if intento < MAX_REINTENTOS:             
            print("Reintentando en 2 segundos...")
            time.sleep(2)                       

if not conectado:    
    print("No se pudo conectar. Asegurate de que servidor.py este corriendo.")
    sys.exit()      

print(f"Conectado al servidor como '{nombre}'!")
print("Escribe tus mensajes. Usa /exit para salir.\n")

cliente.send(nombre.encode())   

confirmacion = cliente.recv(1024).decode()  
print(f"[Servidor]: {confirmacion}\n")

def recibir():
    while True:
        try:
            mensaje = cliente.recv(1024)   
            if mensaje:
                print(mensaje.decode())   
            else:
                print("El servidor se desconecto.")
                cliente.close()
                sys.exit()
        except:
            print("Se perdio la conexion con el servidor.")
            cliente.close()
            sys.exit()

hilo = threading.Thread(target=recibir)   
hilo.daemon = True                        
hilo.start()                             

while True:
    try:
        texto = input()       

        if not texto:         
            continue           

        cliente.send(texto.encode())   

        if texto == "/exit":           
            print("Saliendo del chat...")
            cliente.close()         
            break                    

    except KeyboardInterrupt:
        print("\nSaliendo...")
        try:
            cliente.send("/exit".encode())
        except:
            pass          
        cliente.close()
        break

    except Exception as e:
        print(f"Error al enviar mensaje: {e}")
        break