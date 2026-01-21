
import customtkinter as ctk
import tkinter as tk
from typing import Optional

# Configuración de apariencia global
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class YeiciApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Ventana Principal
        self.title("YeiciCap Hub v1.9.0 | Production Bridge")
        self.geometry("950x650")

        # Configuración de Grid (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="YEICICAP", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, px=20, py=(20, 10))
        self.version_label = ctk.CTkLabel(self.sidebar_frame, text="PRO HUB v1.9.0", text_color="gray60", font=ctk.CTkFont(size=10))
        self.version_label.grid(row=1, column=0, px=20, py=(0, 20))

        self.btn_dashboard = ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=self.show_dashboard, fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w")
        self.btn_dashboard.grid(row=2, column=0, px=20, py=5, sticky="ew")

        self.btn_config = ctk.CTkButton(self.sidebar_frame, text="Configuración", command=self.show_config, fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w")
        self.btn_config.grid(row=3, column=0, px=20, py=5, sticky="ew")

        self.btn_help_maya = ctk.CTkButton(self.sidebar_frame, text="Ayuda Maya", command=self.show_maya_help, fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w")
        self.btn_help_maya.grid(row=4, column=0, px=20, py=5, sticky="ew")

        self.btn_help_unreal = ctk.CTkButton(self.sidebar_frame, text="Ayuda Unreal", command=self.show_unreal_help, fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w")
        self.btn_help_unreal.grid(row=5, column=0, px=20, py=5, sticky="ew")

        # --- MAIN CONTENT AREA ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", px=20, py=20)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Inicializar Pestañas
        self.frames = {}
        self._init_dashboard()
        self._init_config()
        self._init_help_maya()
        self._init_help_unreal()

        self.show_dashboard()

    def _init_dashboard(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["dashboard"] = frame

        # Header con Estado
        status_frame = ctk.CTkFrame(frame, height=100)
        status_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        status_frame.grid_columnconfigure((0,1,2), weight=1)

        # Indicadores (LEDs)
        self.led_motive = self._create_led(status_frame, "Motive 2.x", 0)
        self.led_maya = self._create_led(status_frame, "Maya Node", 1)
        self.led_unreal = self._create_led(status_frame, "Unreal Live", 2)

        # Botón Central de Control
        self.main_btn = ctk.CTkButton(frame, text="START ENGINE", height=60, font=ctk.CTkFont(size=18, weight="bold"), fg_color="#4F46E5", hover_color="#4338CA", command=self.toggle_engine)
        self.main_btn.grid(row=1, column=0, sticky="ew", pady=10)

        # Consola de Logs
        self.console = ctk.CTkTextbox(frame, font=ctk.CTkFont(family="Consolas", size=12), border_width=1)
        self.console.grid(row=2, column=0, sticky="nsew", pady=10)
        frame.grid_rowconfigure(2, weight=1)
        
        self.console.insert("0.0", "--- YeiciCap Hub System Logs ---\n[INFO] GUI Inicializada correctamente.\n[INFO] Esperando acción del usuario...")

    def _create_led(self, parent, label_text, col):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.grid(row=0, column=col, py=15)
        
        led = ctk.CTkFrame(container, width=15, height=15, corner_radius=10, fg_color="#334155")
        led.grid(row=0, column=0, px=5)
        
        lbl = ctk.CTkLabel(container, text=label_text, font=ctk.CTkFont(size=11, weight="bold"))
        lbl.grid(row=0, column=1, px=5)
        return led

    def _init_config(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["config"] = frame

        lbl = ctk.CTkLabel(frame, text="Configuración de Red", font=ctk.CTkFont(size=18, weight="bold"))
        lbl.grid(row=0, column=0, sticky="w", py=10)

        # Motive IP
        ctk.CTkLabel(frame, text="Motive Multicast IP:").grid(row=1, column=0, sticky="w", py=(10,0))
        self.entry_motive_ip = ctk.CTkEntry(frame, width=300, placeholder_text="239.255.42.99")
        self.entry_motive_ip.grid(row=2, column=0, sticky="w", py=5)

        # Local Interface
        ctk.CTkLabel(frame, text="Local Interface IP:").grid(row=3, column=0, sticky="w", py=(10,0))
        self.entry_local_ip = ctk.CTkEntry(frame, width=300, placeholder_text="127.0.0.1")
        self.entry_local_ip.grid(row=4, column=0, sticky="w", py=5)

        # DCC Port
        ctk.CTkLabel(frame, text="DCC Distribution Port (TCP):").grid(row=5, column=0, sticky="w", py=(10,0))
        self.entry_port = ctk.CTkEntry(frame, width=300, placeholder_text="54321")
        self.entry_port.grid(row=6, column=0, sticky="w", py=5)

        btn_save = ctk.CTkButton(frame, text="Guardar Cambios", command=lambda: print("Config Guardada"))
        btn_save.grid(row=7, column=0, sticky="w", py=20)

    def _init_help_maya(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["maya"] = frame
        
        text = """CONEXIÓN CON AUTODESK MAYA:
        
1. En Maya, abre el Editor de Script (Python).
2. Asegúrate de tener instalado el cliente de YeiciCap.
3. Ejecuta el comando de conexión:
   import yeicicap_maya as yc
   yc.connect(port=54321)
   
4. Verás los esqueletos aparecer en el Outliner automáticamente.
5. El Hub debe estar en estado 'START' para recibir datos."""
        
        lbl = ctk.CTkLabel(frame, text=text, justify="left", font=ctk.CTkFont(size=13), anchor="nw")
        lbl.grid(row=0, column=0, sticky="nsew", px=20, py=20)

    def _init_help_unreal(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["unreal"] = frame
        
        text = """CONEXIÓN CON UNREAL ENGINE 5:
        
1. Habilita el plugin 'Live Link' en tu proyecto.
2. En la ventana Live Link, añade un 'YeiciCap Source'.
3. Configura la IP como '127.0.0.1' y el puerto '54321'.
4. Selecciona el 'Subject' en tu Blueprint de Animación.
   
Nota: Asegúrate de que el Firewall de Windows permita el tráfico UDP."""
        
        lbl = ctk.CTkLabel(frame, text=text, justify="left", font=ctk.CTkFont(size=13), anchor="nw")
        lbl.grid(row=0, column=0, sticky="nsew", px=20, py=20)

    def show_dashboard(self): self._show_frame("dashboard")
    def show_config(self): self._show_frame("config")
    def show_maya_help(self): self._show_frame("maya")
    def show_unreal_help(self): self._show_frame("unreal")

    def _show_frame(self, name):
        for f in self.frames.values(): f.grid_forget()
        self.frames[name].grid(row=0, column=0, sticky="nsew")

    def toggle_engine(self):
        # Lógica visual de inicio/parada
        if self.main_btn.cget("text") == "START ENGINE":
            self.main_btn.configure(text="STOP ENGINE", fg_color="#EF4444", hover_color="#DC2626")
            self.led_motive.configure(fg_color="#10B981") # Verde activo
            self.console.insert(tk.END, "\n[SYSTEM] Engine iniciado. Escuchando Motive...")
        else:
            self.main_btn.configure(text="START ENGINE", fg_color="#4F46E5", hover_color="#4338CA")
            self.led_motive.configure(fg_color="#334155") # Gris inactivo
            self.console.insert(tk.END, "\n[SYSTEM] Engine detenido.")
        self.console.see(tk.END)

if __name__ == "__main__":
    app = YeiciApp()
    app.mainloop()
