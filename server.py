import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import json

# Configuración del servidor
HOST = '127.0.0.1'
PORT = 8080
MAX_WORKERS = 4  # Nuestro pool de hilos (workers)

def procesar_tarea(datos_tarea):
    """Simula el trabajo pesado que hace el worker"""
    print(f"[Worker] Procesando tarea ID: {datos_tarea.get('id')} - Acción: {datos_tarea.get('accion')}")
    # Simulamos un procesamiento
    resultado = f"Tarea {datos_tarea.get('id')} procesada con éxito por el worker."
    return {"status": "OK", "resultado": resultado}

def manejar_cliente(conn, addr):
    print(f"[+] Conexión establecida desde {addr}")
    try:
        data = conn.recv(1024).decode('utf-8')
        if data:
            tarea = json.loads(data)
            print(f"[Servidor] Tarea recibida: {tarea}")
            
            # Derivamos la tarea al pool de workers
            futuro = executor.submit(procesar_tarea, tarea)
            respuesta = futuro.result() # Esperamos el resultado del worker
            
            # Respondemos al cliente
            conn.sendall(json.dumps(respuesta).encode('utf-8'))
    except Exception as e:
        error_resp = {"status": "ERROR", "mensaje": str(e)}
        conn.sendall(json.dumps(error_resp).encode('utf-8'))
    finally:
        conn.close()
        print(f"[-] Conexión cerrada con {addr}")

def iniciar_servidor():
    global executor
    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Servidor escuchando en {HOST}:{PORT} con un pool de {MAX_WORKERS} workers...")
    
    try:
        while True:
            conn, addr = server.accept()
            # Creamos un hilo para atender al cliente que se conecta por socket
            hilo_cliente = threading.Thread(target=manejar_cliente, args=(conn, addr))
            hilo_cliente.start()
    except KeyboardInterrupt:
        print("\n[!] Apagando servidor...")
    finally:
        server.close()
        executor.shutdown()

if __name__ == "__main__":
    iniciar_servidor()