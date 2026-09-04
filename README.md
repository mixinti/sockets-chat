# Chat Multicliente con Sockets TCP

Aplicación de chat en tiempo real cliente-servidor desarrollada en Python utilizando librerías nativas.

## Características Técnicas

* **Arquitectura Cliente-Servidor:** Comunicación síncrona basada en el protocolo TCP.
* **Servidor No Bloqueante:** Utiliza el módulo `select` para gestionar múltiples clientes simultáneos en un solo hilo (Multiplexación de I/O).
* **Cliente Concurrente:** Implementa hilos con `threading` para recibir mensajes en segundo plano sin bloquear la terminal.
* **Resiliencia:** Manejo de desconexiones abruptas, sistema de reintentos automáticos en el cliente y cierre limpio de sockets.

## Arquitectura del Proyecto

* `servidor.py`: Administra las conexiones, valida los nombres de usuario y distribuye los mensajes.
* `cliente.py`: Conecta al usuario con el servidor, envía datos y escucha la sala de manera asíncrona.

## Instalación y Uso

1. Iniciar el servidor:
   ```bash
   python servidor.py
   ```

2. Iniciar los clientes necesarios:
   ```bash
   python cliente.py
   ```
