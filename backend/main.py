
import time
import sys
import queue
import logging
from core.natnet_client import NatNetClient
from logic.processor import MocapTransformer
from exporters.stream_server import StreamServer

# --- CONFIGURACIÓN DE QA ---
DEBUG_MODE = True
REPORT_INTERVAL_FRAMES = 60 # Aproximadamente 1 segundo a 60-120Hz
MAYA_PORT = 54321

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def main_loop():
    print("\n" + "="*50)
    print("      YEICICAP HUB v1.4.0 - FINAL PIPELINE")
    print("="*50)
    
    # 1. Inicialización de componentes
    client = NatNetClient()
    processor = MocapTransformer()
    exporter = StreamServer(port=MAYA_PORT)
    
    # 2. Arranque de servicios
    if not client.start():
        logging.error("FALLO CRÍTICO: No se pudo conectar con Motive.")
        sys.exit(1)
    
    exporter.start()
    
    logging.info(f"Hub listo. Distribuyendo en puerto {MAYA_PORT}...")

    frame_counter = 0
    start_time = time.time()
    
    try:
        while True:
            try:
                # MEDICIÓN DE LATENCIA INTERNA
                t_ingest_start = time.perf_counter()
                
                # A. Ingesta
                raw_frame = client.frame_queue.get(timeout=1.0)
                t_ingest_end = time.perf_counter()
                
                # B. Procesamiento (Numpy Vectorized)
                t_proc_start = time.perf_counter()
                clean_payload = processor.process_frame(raw_frame)
                t_proc_end = time.perf_counter()
                
                # C. Distribución (TCP Broadcast)
                exporter.broadcast(clean_payload)
                
                frame_counter += 1
                
                # --- REPORTE DE DIAGNÓSTICO (DEBUG_MODE) ---
                if DEBUG_MODE and frame_counter >= REPORT_INTERVAL_FRAMES:
                    ms_proc = (t_proc_end - t_proc_start) * 1000
                    active_clients = len(exporter.clients)
                    subjects = len(clean_payload["subjects"])
                    
                    print(f"\n--- DIAGNOSTIC CHECKLIST [Frame #{clean_payload['frame_number']}] ---")
                    print(f"[OK] Motive Connection: ACTIVE (Queue size: {client.frame_queue.qsize()})")
                    print(f"[OK] Parsing: Frame ID detected, payload extracted.")
                    print(f"[OK] Numpy Logic: Transformation completed in {ms_proc:.3f}ms")
                    
                    if active_clients > 0:
                        print(f"[OK] Distribution: Streaming to {active_clients} clients.")
                    else:
                        print(f"[WAITING] DCC Clients: Waiting for connection on port {MAYA_PORT}...")
                    
                    print(f"[INFO] Active Subjects: {subjects}")
                    print("-" * 45)
                    
                    frame_counter = 0
                
                client.frame_queue.task_done()
                
            except queue.Empty:
                if DEBUG_MODE:
                    print("[WARN] No hay datos de Motive... ¿Está el streaming activo?")
                continue
                
    except KeyboardInterrupt:
        logging.info("Apagando YeiciCap Hub...")
    finally:
        client.stop()
        exporter.stop()
        logging.info("Sistema cerrado correctamente.")

if __name__ == "__main__":
    main_loop()
