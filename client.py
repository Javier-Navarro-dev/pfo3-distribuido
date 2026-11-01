import socket
import json

HOST = '127.0.0.1'
PORT = 8080

def enviar_tarea(id_tarea, accion_tarea):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((HOST, PORT))
        
        # Armamos la tarea en formato JSON
        payload = {
            "id": id_tarea,
            "accion": accion_tarea
        }
        
        print(f"[Cliente] Enviando tarea al servidor...")
        cliente.sendall(json.dumps(payload).encode('utf-8'))
        
        # Recibimos la respuesta del servidor
        respuesta_raw = cliente.recv(1024).decode('utf-8')
        respuesta = json.loads(respuesta_raw)
        
        print(f"[Cliente] Respuesta recibida del servidor: {respuesta}")
        
    except Exception as e:
        print(f"[Error] No se pudo conectar con el servidor: {e}")
    finally:
        cliente.close()

if __name__ == "__main__":
    # Probamos enviando una tarea de ejemplo
    enviar_tarea(101, "generar_reporte_mensual")