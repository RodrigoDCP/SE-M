import tkinter as tk
from tkinter import ttk
from interfaz import InterfazMedica

def centrar_ventana(ventana):
    """Centra cualquier ventana en la pantalla."""
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
        self.ventana.geometry("600x500")
        
        # Configuración de colores
        self.COLORS = {
            'primary': '#2563eb',    # Azul principal
            'background': '#f8fafc',  # Fondo claro
            'text': '#1e293b',       # Texto oscuro
            'accent': '#818cf8'      # Acento
        }
        
        # Configurar ventana
        self.ventana.configure(bg=self.COLORS['background'])
        self.crear_interfaz()
        centrar_ventana(self.ventana)
        
    def crear_interfaz(self):
        # Configurar estilos
        style = ttk.Style()
        style.configure('Main.TFrame', background=self.COLORS['background'])
        style.configure('Title.TLabel',
                       background=self.COLORS['background'],
                       foreground=self.COLORS['primary'],
                       font=('Helvetica', 24, 'bold'))
        style.configure('Content.TLabel',
                       background=self.COLORS['background'],
                       foreground=self.COLORS['text'],
                       font=('Helvetica', 12))
        style.configure('Start.TButton',
                       font=('Helvetica', 12, 'bold'),
                       padding=15)

        # Frame principal
        main_frame = ttk.Frame(self.ventana, style='Main.TFrame')
        main_frame.pack(expand=True, fill='both', padx=40, pady=20)

        # Título con ícono
        ttk.Label(
            main_frame,
            text="🏥 Sistema Experto Médico",
            style='Title.TLabel'
        ).pack(pady=(0, 30))

        # Mensaje de bienvenida
        mensaje = """¡Bienvenido al Sistema Experto Médico!

Este sistema está diseñado para ayudarte a encontrar
el médico más adecuado según tus necesidades específicas.

El sistema te guiará a través de algunas preguntas sobre:
• Tu motivo de consulta
• La intensidad de tus síntomas
• Tu historial médico
• Tu edad

Con esta información, podremos recomendarte
el especialista más apropiado para tu caso."""

        # Crear Text widget para el mensaje
        texto = tk.Text(
            main_frame,
            height=10,
            width=45,
            font=('Helvetica', 11),
            bg=self.COLORS['background'],
            fg=self.COLORS['text'],
            bd=0,
            wrap='word'
        )
        texto.pack(pady=20)
        texto.insert('1.0', mensaje)
        texto.configure(state='disabled')

        # Nota importante
        ttk.Label(
            main_frame,
            text="Nota: Este sistema es una guía y no reemplaza\nla consulta con un profesional médico.",
            style='Content.TLabel',
            justify='center'
        ).pack(pady=(0, 30))

        # Frame para el botón
        button_frame = ttk.Frame(main_frame, style='Main.TFrame')
        button_frame.pack(pady=20)

        # Botón comenzar
        boton_comenzar = ttk.Button(
            button_frame,
            text="Comenzar →",
            command=self.iniciar_sistema,
            style='Start.TButton'
        )
        boton_comenzar.pack(pady=10)

    def iniciar_sistema(self):
        """Cierra la ventana de bienvenida e inicia el sistema principal."""
        self.ventana.destroy()
        app = InterfazMedica()
        app.iniciar()

    def iniciar(self):
        """Inicia la ventana de bienvenida."""
        self.ventana.mainloop()

if __name__ == "__main__":
    app = VentanaBienvenida()
    app.iniciar()