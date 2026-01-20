
import socket
import threading
import json
import logging
import select

class StreamServer:
    """
    Servidor de distribución de YeiciCap Hub.
    Envía payloads procesados a clientes conectados (Maya/Unreal) vía TCP.
    """
    def __init__(self, host='127.0.0.1', port=54321):
        self.host = host
        self.port = port
        self.clients = []
        self._running = False
        self._server_socket = None

    def start(self):
        """Inicia el servidor TCP en un hilo separado."""
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self.host, self.port))
        self._server_socket.listen(5)
        self._server_socket.setblocking(False)
        
        self._running = True
        self._thread = threading.Thread(target=self._run_server, name="StreamServer", daemon=True)
        self._thread.start()
        logging.info(f"StreamServer iniciado en {self.host}:{self.port}")

    def _run_server(self):
        while self._running:
            # Usar select para manejar nuevas conexiones y limpieza de sockets
            readable, _, _ = select.select([self._server_socket] + self.clients, [], [], 0.1)
            
            for s in readable:
                if s is self._server_socket:
                    conn, addr = s.accept()
                    conn.setblocking(False)
                    self.clients.append(conn)
                    logging.info(f"Nuevo cliente conectado: {addr}")
                else:
                    # Si un cliente envía algo o cierra la conexión
                    try:
                        data = s.recv(1024)
                        if not data:
                            self._remove_client(s)
                    except:
                        self._remove_client(s)

    def _remove_client(self, client_socket):
        if client_socket in self.clients:
            self.clients.remove(client_socket)
            client_socket.close()
            logging.info("Cliente desconectado.")

    def broadcast(self, payload: dict):
        """Envía el JSON del payload a todos los clientes conectados."""
        if not self.clients:
            return

        # Serializar a JSON y añadir newline como delimitador de paquete
        message = (json.dumps(payload) + "\n").encode('utf-8')
        
        for client in self.clients[:]:
            try:
                client.sendall(message)
            except (socket.error, BrokenPipeError):
                self._remove_client(client)

    def stop(self):
        self._running = False
        for c in self.clients:
            c.close()
        if self._server_socket:
            self._server_socket.close()
