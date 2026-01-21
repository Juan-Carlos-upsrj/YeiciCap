
import logging
import sys
from gui_app import YeiciApp

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def launch_gui():
    """Lanza la interfaz gráfica principal."""
    try:
        logging.info("Iniciando YeiciCap Hub GUI...")
        app = YeiciApp()
        app.mainloop()
    except Exception as e:
        logging.error(f"Error fatal al iniciar la GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # En el futuro, podríamos añadir argumentos de línea de comando para modo headless
    # if "--headless" in sys.argv: run_cli_mode()
    launch_gui()
