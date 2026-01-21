
import customtkinter as ctk
import tkinter as tk
import logging
import queue
import threading
from typing import Optional

# Importaciones del Backend
from core.natnet_client import NatNetClient
from exporters.stream_server import StreamServer
from logic.processor import MocapTransformer

# Configuración de apariencia
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ConsoleHandler(logging.Handler):
    """Redirige los logs de Python al widget CTkTextbox de la GUI."""
    def __init__(self, textbox):
        super().__init__()
        self.textbox = textbox

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.textbox.insert(tk.END, f"{msg}\n")
            self.textbox.see(tk.END)
        # Usar after para asegurar thread-safety con Tkinter
        self.textbox.after(0, append)

class YeiciApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- LÓGICA DEL ENGINE ---
        self.natnet: Optional[NatNetClient] = None
        self.server: Optional[StreamServer] = None
        self.transformer = MocapTransformer()
        self.engine_running = False
        self.heartbeat_state = False

        # --- UI SETUP ---
        self.title("YeiciCap Hub v2.1.0 | Connected Engine")
        self.geometry("950x650")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self._init_sidebar()

        # Main Container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", px=20, py=20)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        self.frames = {}
        self._init_dashboard()
        self._init_config()
        self._init_help_maya()
        self._init_help_unreal()

        # Configurar Logs después de crear la consola
        self._setup_logging()
        
        self.show_dashboard()

    def _setup_logging(self):
        """Conecta el sistema de logging de Python a la consola de la UI."""
        handler = ConsoleHandler(self.console)
        handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%H:%M:%S'))
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.INFO)

    def _init_sidebar(self):
        self.sidebar_frame.grid_rowconfigure(6, weight=1)
        ctk.CTkLabel(self.sidebar_frame, text="YEICICAP", font=ctk.CTkFont(size=22, weight="bold")).grid(row=0, column=0, px=20, py=(20, 10))
        ctk.CTkLabel(self.sidebar_frame, text="CORE v2.1.0", text_color="#6366F1", font=ctk.CTkFont(size=10, weight="bold")).grid(row=1, column=0, px=20, py=(0, 20))

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Configuración", self.show_config),
            ("Ayuda Maya", self.show_maya_help),
            ("Ayuda Unreal", self.show_unreal_help)
        ]
        for i, (text, cmd) in enumerate(buttons):
            ctk.CTkButton(self.sidebar_frame, text=text, command=cmd, fg_color="transparent", text_color="gray90", hover_color="gray30", anchor="w").grid(row=i+2, column=0, px=20, py=5, sticky="ew")

    def _init_dashboard(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["dashboard"] = frame

        # Status LEDs
        status_frame = ctk.CTkFrame(frame, height=80)
        status_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        status_frame.grid_columnconfigure((0,1,2), weight=1)

        self.led_motive = self._create_led(status_frame, "Motive Stream", 0)
        self.led_maya = self._create_led(status_frame, "TCP Out (Clients)", 1)
        self.led_unreal = self._create_led(status_frame, "LiveLink Sync", 2)

        # Main Toggle
        self.main_btn = ctk.CTkButton(frame, text="START ENGINE", height=60, font=ctk.CTkFont(size=18, weight="bold"), fg_color="#4F46E5", hover_color="#4338CA", command=self.toggle_engine)
        self.main_btn.grid(row=1, column=0, sticky="ew", pady=10)

        # Logs Console
        self.console = ctk.CTkTextbox(frame, font=ctk.CTkFont(family="Consolas", size=12), border_width=1)
        self.console.grid(row=2, column=0, sticky="nsew", pady=10)
        frame.grid_rowconfigure(2, weight=1)

    def _create_led(self, parent, label_text, col):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.grid(row=0, column=col, py=15)
        led = ctk.CTkFrame(container, width=14, height=14, corner_radius=7, fg_color="#334155")
        led.grid(row=0, column=0, px=5)
        ctk.CTkLabel(container, text=label_text, font=ctk.CTkFont(size=11)).grid(row=0, column=1, px=5)
        return led

    def _init_config(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["config"] = frame
        ctk.CTkLabel(frame, text="Network Interface", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, sticky="w", py=10)
        
        self.entry_motive_ip = self._create_input(frame, "Motive Multicast IP:", "239.255.42.99", 1)
        self.entry_port = self._create_input(frame, "Stream Port (TCP):", "54321", 3)

    def _create_input(self, parent, label, default, row):
        ctk.CTkLabel(parent, text=label).grid(row=row, column=0, sticky="w", py=(10,0))
        entry = ctk.CTkEntry(parent, width=300)
        entry.insert(0, default)
        entry.grid(row=row+1, column=0, sticky="w", py=5)
        return entry

    def _init_help_maya(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["maya"] = frame
        ctk.CTkLabel(frame, text="MAYA INTEGRATION\n\n1. Use TCP Client to connect to localhost:54321\n2. The hub sends JSON packets with bone data.", justify="left").grid(row=0, column=0, px=20, py=20)

    def _init_help_unreal(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["unreal"] = frame
        ctk.CTkLabel(frame, text="UNREAL ENGINE\n\n1. Enable LiveLink Plugin\n2. Add YeiciCap Source pointing to this IP.", justify="left").grid(row=0, column=0, px=20, py=20)

    # --- ENGINE CONTROLS ---

    def toggle_engine(self):
        if not self.engine_running:
            self._start_engine()
        else:
            self._stop_engine()

    def _start_engine(self):
        try:
            m_ip = self.entry_motive_ip.get()
            s_port = int(self.entry_port.get())

            logging.info(f"Iniciando Engine en Multicast {m_ip}...")
            
            # Inicializar Componentes
            self.natnet = NatNetClient(multicast_ip=m_ip)
            self.server = StreamServer(port=s_port)
            
            if self.natnet.start():
                self.server.start()
                self.engine_running = True
                self.main_btn.configure(text="STOP ENGINE", fg_color="#EF4444", hover_color="#DC2626")
                
                # Iniciar bucle de procesamiento de la UI
                self.update_engine_loop()
                logging.info("Engine operacional. Esperando frames de Motive...")
            else:
                logging.error("No se pudo iniciar NatNet. Revisa la IP Multicast.")
                
        except Exception as e:
            logging.error(f"Error al iniciar: {e}")

    def _stop_engine(self):
        logging.info("Deteniendo Engine...")
        if self.natnet: self.natnet.stop()
        if self.server: self.server.stop()
        
        self.engine_running = False
        self.main_btn.configure(text="START ENGINE", fg_color="#4F46E5", hover_color="#4338CA")
        self.led_motive.configure(fg_color="#334155")
        self.led_maya.configure(fg_color="#334155")

    def update_engine_loop(self):
        """Bucle de alta frecuencia que procesa la cola de frames."""
        if not self.engine_running:
            return

        try:
            # Procesar todos los frames pendientes en la cola
            processed_any = False
            while not self.natnet.frame_queue.empty():
                raw_frame = self.natnet.frame_queue.get_nowait()
                
                # Transformar datos
                processed_frame = self.transformer.process_frame(raw_frame)
                
                # Distribuir a clientes conectados
                self.server.broadcast(processed_frame)
                processed_any = True

            if processed_any:
                self._toggle_heartbeat()
                
            # Actualizar estado del servidor TCP
            if self.server.clients:
                self.led_maya.configure(fg_color="#10B981") # Verde si hay clientes
            else:
                self.led_maya.configure(fg_color="#334155")

        except queue.Empty:
            pass
        except Exception as e:
            logging.error(f"Error en loop de procesamiento: {e}")

        # Programar siguiente iteración (~120 fps de polling)
        self.after(8, self.update_engine_loop)

    def _toggle_heartbeat(self):
        """Hace parpadear el indicador de Motive para mostrar tráfico activo."""
        self.heartbeat_state = not self.heartbeat_state
        color = "#10B981" if self.heartbeat_state else "#059669" # Dos tonos de verde
        self.led_motive.configure(fg_color=color)

    # --- NAVIGATION ---
    def show_dashboard(self): self._show_frame("dashboard")
    def show_config(self): self._show_frame("config")
    def show_maya_help(self): self._show_frame("maya")
    def show_unreal_help(self): self._show_frame("unreal")

    def _show_frame(self, name):
        for f in self.frames.values(): f.grid_forget()
        self.frames[name].grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    app = YeiciApp()
    app.mainloop()
