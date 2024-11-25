import tkinter as tk
from tkinter import ttk
from interfaz import InterfazMedica
from custom_styles import Styles, CustomButton, CustomFrame, CustomLabel, setup_window_style

def centrar_ventana(ventana):
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = int((ancho_pantalla - ancho) / 2)
    y = int((alto_pantalla - alto) / 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

class VentanaBienvenida:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Bienvenida - Sistema Experto Médico")
        self.ventana.geometry("700x600")
        
        # Configurar estilo de la ventana
        setup_window_style(self.ventana)
        self.crear_interfaz()
        centrar_ventana(self.ventana)
        
    def crear_interfaz(self):
        # Frame principal con efecto de tarjeta
        main_frame = CustomFrame(self.ventana)
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)

        # Logo o icono médico (emoji como placeholder)
        logo_label = CustomLabel(
            main_frame,
            text="🏥",
            font=('Segoe UI', 48)
        )
        logo_label.pack(pady=(20, 0))

        # Titulo principal
        titulo = CustomLabel(
            main_frame,
            text="Sistema Experto Médico",
            font=Styles.FONTS['heading'],
            fg=Styles.COLORS['primary']
        )
        titulo.pack(pady=(0, 30))

        # Frame para el contenido
        content_frame = tk.Frame(main_frame, bg=Styles.COLORS['surface'])
        content_frame.pack(fill='both', expand=True, padx=20)

        # Mensaje de bienvenida con mejor formato
        self.crear_texto_bienvenida(content_frame)

        # Boton comenzar
        CustomButton(
            main_frame,
            text="Comenzar Consulta →",
            command=self.iniciar_sistema,
            width=250
        ).pack(pady=30)

    def crear_texto_bienvenida(self, parent):
        # Frame para los puntos clave
        key_points_frame = CustomFrame(parent)
        key_points_frame.pack(fill='x', pady=10)
        
        CustomLabel(
            key_points_frame,
            text="Este sistema te ayudara a encontrar el médico mas adecuado\n" +
                 "segun tus necesidades especificas.",
            font=Styles.FONTS['body_bold'],
            fg=Styles.COLORS['primary']
        ).pack(pady=(0, 15))

        puntos = [
            "📋 Tu motivo de consulta",
            "📊 La intensidad de tus sintomas",
            "📁 Tu historial médico",
            "👤 Tu edad y condicion actual"
        ]

        for punto in puntos:
            CustomLabel(
                key_points_frame,
                text=punto,
                justify='left',
                pady=5
            ).pack(anchor='w')

    def iniciar_sistema(self):
        self.ventana.destroy()
        app = InterfazMedica()
        app.iniciar()

    def iniciar(self):
        self.ventana.mainloop()