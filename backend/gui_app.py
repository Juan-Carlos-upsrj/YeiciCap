
import customtkinter as ctk
import tkinter as tk
from typing import Dict

# Configuración Global de Apariencia
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class YeiciApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Ventana Principal ---
        self.title("YeiciCap Hub | MoCap Bridge Professional v2.2.0")
        self.geometry("1000x700")

        # Grid Principal: 1 columna (Sidebar) + 1 columna (Contenido)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar (Izquierda) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="YEICICAP HUB", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, py=(30, 10))
        
        self.version_tag = ctk.CTkLabel(
            self.sidebar_frame, 
            text="CORE v2.2.0-STABLE", 
            text_color="#5DADE2",
            font=ctk.CTkFont(size=10, weight="bold")
        )
        self.version_tag.grid(row=1, column=0, padx=20, py=(0, 30))

        # Botones de Navegación
        self.nav_buttons = []
        self.btn_dashboard = self._add_nav_button("Dashboard", 2, self.show_dashboard)
        self.btn_config = self._add_nav_button("Configuración", 3, self.show_config)
        self.btn_maya = self._add_nav_button("Ayuda Maya", 4, self.show_maya_help)
        self.btn_unreal = self._add_nav_button("Ayuda Unreal", 5, self.show_unreal_help)

        # --- Área de Contenido Principal ---
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, py=20)
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(0, weight=1)

        # Diccionario de Frames (Pestañas)
        self.frames: Dict[str, ctk.CTkFrame] = {}
        
        self._init_dashboard_frame()
        self._init_config_frame()
        self._init_maya_frame()
        self._init_unreal_frame()

        # Mostrar Dashboard por defecto
        self.show_dashboard()

    def _add_nav_button(self, text, row, command):
        btn = ctk.CTkButton(
            self.sidebar_frame, 
            text=text, 
            command=command,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            height=40
        )
        btn.grid(row=row, column=0, padx=20, py=5, sticky="ew")
        self.nav_buttons.append(btn)
        return btn

    def _init_dashboard_frame(self):
        frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.frames["dashboard"] = frame

        # 1. Panel de Estado
        status_panel = ctk.CTkFrame(frame, height=120)
        status_panel.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        status_panel.grid_columnconfigure((0, 1, 2), weight=1)

        self.status_motive = self._create_status_indicator(status_panel, "MOTIVE: DESCONECTADO", 0)
        self.status_maya = self._create_status_indicator(status_panel, "MAYA: ESPERANDO", 1)
        self.status_unreal = self._create_status_indicator(status_panel, "UNREAL: ESPERANDO", 2)

        # 2. Botón Maestro
        self.btn_start = ctk.CTkButton(
            frame, 
            text="INICIAR SERVIDOR", 
            height=80,
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color="#1F618D",
            hover_color="#1A5276"
        )
        self.btn_start.grid(row=1, column=0, sticky="ew", pady=10)

        # 3. Consola de Logs
        self.console = ctk.CTkTextbox(
            frame, 
            font=ctk.CTkFont(family="Consolas", size=12),
            border_width=1,
            fg_color="#1C1C1C"
        )
        self.console.grid(row=2, column=0, sticky="nsew", pady=(10, 0))
        self.console.insert("0.0", "--- YeiciCap Hub System Console ---\n[INFO] Sistema iniciado correctamente.\n[INFO] Interfaz v2.2.0 lista para operar.\n")
        self.console.configure(state="disabled")
        frame.grid_rowconfigure(2, weight=1)

    def _create_status_indicator(self, parent, text, col):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.grid(row=0, column=col, padx=10, pady=20)
        
        # El "LED" visual
        led = ctk.CTkFrame(container, width=15, height=15, corner_radius=10, fg_color="#566573")
        led.grid(row=0, column=0, padx=(0, 10))
        
        label = ctk.CTkLabel(container, text=text, font=ctk.CTkFont(size=11, weight="bold"))
        label.grid(row=0, column=1)
        return led

    def _init_config_frame(self):
        frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.frames["config"] = frame
        
        lbl = ctk.CTkLabel(frame, text="Configuración Global", font=ctk.CTkFont(size=20, weight="bold"))
        lbl.pack(pady=20, anchor="w")
        
        # Inputs de ejemplo
        self._add_config_input(frame, "IP Multicast Motive:", "239.255.42.99")
        self._add_config_input(frame, "Puerto de Datos (NatNet):", "1511")
        self._add_config_input(frame, "Puerto de Salida (Bridge):", "54321")

    def _add_config_input(self, parent, label_text, default):
        ctk.CTkLabel(parent, text=label_text).pack(pady=(10, 0), anchor="w")
        entry = ctk.CTkEntry(parent, width=400)
        entry.insert(0, default)
        entry.pack(pady=5, anchor="w")

    def _init_maya_frame(self):
        frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.frames["maya"] = frame
        
        title = ctk.CTkLabel(frame, text="Integración con Autodesk Maya", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20, anchor="w")
        
        instructions = (
            "1. Asegúrate de que el Servidor del Hub esté en estado 'Iniciado'.\n"
            "2. En Maya, abre el Script Editor (Python tab).\n"
            "3. Copia y ejecuta el siguiente script de conexión.\n"
            "4. Los objetos se crearán automáticamente en el Outliner."
        )
        ctk.CTkLabel(frame, text=instructions, justify="left", font=ctk.CTkFont(size=13)).pack(pady=10, anchor="w")
        
        btn_copy = ctk.CTkButton(frame, text="Copiar Script Maya", fg_color="#2E4053", width=200)
        btn_copy.pack(pady=20, anchor="w")

    def _init_unreal_frame(self):
        frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.frames["unreal"] = frame
        
        title = ctk.CTkLabel(frame, text="Integración con Unreal Engine 5", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20, anchor="w")
        
        instructions = (
            "1. Habilita el plugin 'Live Link' en tu proyecto de Unreal.\n"
            "2. En la ventana Live Link, añade un 'YeiciCap Source'.\n"
            "3. Configura la IP Local y el puerto 54321.\n"
            "4. Los esqueletos aparecerán como 'Subjects' disponibles."
        )
        ctk.CTkLabel(frame, text=instructions, justify="left", font=ctk.CTkFont(size=13)).pack(pady=10, anchor="w")
        
        btn_copy = ctk.CTkButton(frame, text="Copiar Blueprint Node", fg_color="#2E4053", width=200)
        btn_copy.pack(pady=20, anchor="w")

    def _show_frame(self, name):
        """Gestiona el intercambio de pestañas."""
        for f in self.frames.values():
            f.pack_forget()
        self.frames[name].pack(fill="both", expand=True)
        
        # Feedback visual en botones laterales
        for btn in self.nav_buttons:
            if btn.cget("text") in [name.replace("_", " ").title(), "Dashboard" if name=="dashboard" else ""]:
                btn.configure(fg_color=("gray75", "gray25"))
            else:
                btn.configure(fg_color="transparent")

    def show_dashboard(self): self._show_frame("dashboard")
    def show_config(self): self._show_frame("config")
    def show_maya_help(self): self._show_frame("maya")
    def show_unreal_help(self): self._show_frame("unreal")

if __name__ == "__main__":
    app = YeiciApp()
    app.mainloop()
