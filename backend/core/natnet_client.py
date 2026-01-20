
import socket
import struct
import threading
import queue
import logging
from typing import Dict, Any

# Configuración de Logging para diagnóstico
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [NATNET] - %(levelname)s - %(message)s')

class NatNetClient:
    """
    Producer Engine para YeiciCap Hub.
    Decodifica el bitstream de NatNet 3.x (Motive 2.x) y lo coloca en una queue thread-safe.
    """
    def __init__(self, multicast_ip="239.255.42.99", data_port=1511, buffer_size=65535):
        self.multicast_ip = multicast_ip
        self.data_port = data_port
        self.buffer_size = buffer_size
        
        # Thread-safe Queue para el Consumer
        self.frame_queue = queue.Queue(maxsize=100)
        
        self._running = False
        self._data_socket = None
        self._stop_event = threading.Event()

    def _create_multicast_socket(self):
        """Inicializa el socket UDP con soporte para Multicast."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind a todas las interfaces en el puerto de datos
            sock.bind(('', self.data_port))
            
            # Unirse al grupo multicast
            mreq = struct.pack("4sl", socket.inet_aton(self.multicast_ip), socket.INADDR_ANY)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            
            logging.info(f"Socket conectado exitosamente a {self.multicast_ip}:{self.data_port}")
            return sock
        except Exception as e:
            logging.error(f"Error al crear el socket: {e}")
            return None

    def _unpack_rigid_body(self, data, offset):
        """Decodifica un Rigid Body individual (NatNet 3.x)."""
        # Estructura: ID (4b), Pos (3x4b float), Rot (4x4b float)
        rb_id = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4
        
        pos = struct.unpack('<fff', data[offset:offset+12])
        offset += 12
        
        rot = struct.unpack('<ffff', data[offset:offset+16])
        offset += 16
        
        return {
            "id": rb_id,
            "pos": pos, # X, Y, Z
            "rot": rot  # X, Y, Z, W
        }, offset

    def _unpack_frame_of_data(self, data):
        """
        Parser principal para PacketID 7 (Frame of Data).
        Basado en la especificación de NatNet 3.x.
        """
        offset = 4 # Saltamos MessageID (2) y PacketSize (2) ya leídos
        
        frame_number = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4
        
        # --- Marcadores (Omitidos por brevedad pero offset avanzado) ---
        marker_set_count = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4
        for _ in range(marker_set_count):
            # Saltar nombre del marker set (null terminated)
            while data[offset] != 0: offset += 1
            offset += 1
            # Saltar markers individuales
            marker_count = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4 + (marker_count * 12)

        # --- Rigid Bodies ---
        rb_count = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4
        rigid_bodies = []
        for _ in range(rb_count):
            rb_data, offset = self._unpack_rigid_body(data, offset)
            rigid_bodies.append(rb_data)
            # NatNet 3.x incluye marker error (4b) después de cada RB
            offset += 4 

        # --- Skeletons (NatNet 3.0+) ---
        sk_count = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4
        skeletons = []
        for _ in range(sk_count):
            sk_id = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            sk_rb_count = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            sk_rbs = []
            for _ in range(sk_rb_count):
                rb_data, offset = self._unpack_rigid_body(data, offset)
                sk_rbs.append(rb_data)
                offset += 4 # Marker error
            skeletons.append({"id": sk_id, "rigid_bodies": sk_rbs})

        return {
            "frame_number": frame_number,
            "rigid_bodies": rigid_bodies,
            "skeletons": skeletons
        }

    def _listen(self):
        """Bucle principal de escucha en hilo secundario."""
        while not self._stop_event.is_set():
            try:
                data, addr = self._data_socket.recvfrom(self.buffer_size)
                if not data: continue
                
                # Identificar PacketID
                message_id = struct.unpack('<H', data[0:2])[0]
                
                # PacketID 7 = Frame of Data
                if message_id == 7:
                    frame = self._unpack_frame_of_data(data)
                    
                    # Intentar poner en queue sin bloquear indefinidamente
                    try:
                        self.frame_queue.put_nowait(frame)
                    except queue.Full:
                        # Si la queue está llena, descartamos el frame más viejo (LIFO-like behavior)
                        # o simplemente ignoramos para priorizar latencia sobre integridad histórica
                        pass
                
            except socket.error as e:
                if self._running:
                    logging.error(f"Socket error: {e}")
            except Exception as e:
                logging.error(f"Error crítico al decodificar paquete: {e}")
                continue # Mantener el socket abierto ante paquetes corruptos

    def start(self):
        """Inicia el proceso de captura."""
        self._data_socket = self._create_multicast_socket()
        if not self._data_socket:
            return False
            
        self._running = True
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._listen, name="NatNetProducer", daemon=True)
        self._thread.start()
        logging.info("Producer iniciado y escuchando activamente.")
        return True

    def stop(self):
        """Detiene el proceso de captura de forma segura."""
        self._running = False
        self._stop_event.set()
        if self._data_socket:
            # Forzar el cierre del socket para desbloquear recvfrom
            self._data_socket.close()
        logging.info("Producer detenido.")
