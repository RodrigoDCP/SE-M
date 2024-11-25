import tkinter as tk
from tkinter import ttk

class Styles:
    # Colores principales
    COLORS = {
        'primary': '#0ea5e9',      # Azul cielo
        'primary_dark': '#0284c7',
        'secondary': '#6366f1',    # Indigo
        'background': '#f8fafc',   # Gris muy claro
        'surface': '#ffffff',      # Blanco
        'text': '#1e293b',        # Azul oscuro
        'text_light': '#64748b',  # Gris azulado
        'error': '#ef4444',       # Rojo
        'success': '#22c55e',     # Verde
        'warning': '#f59e0b',     # Amarillo
        'border': '#e2e8f0'       # Gris claro
    }
    
    # Fuentes
    FONTS = {
        'heading': ('Segoe UI', 24, 'bold'),
        'subheading': ('Segoe UI', 18, 'bold'),
        'body': ('Segoe UI', 12),
        'body_bold': ('Segoe UI', 12, 'bold'),
        'small': ('Segoe UI', 10),
        'button': ('Segoe UI', 11, 'bold')
    }

class CustomButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=200, height=40, color=Styles.COLORS['primary'], 
                 hover_color=Styles.COLORS['primary_dark'], **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)
        self.configure(bg=Styles.COLORS['background'])
        
        self.color = color
        self.hover_color = hover_color
        self.command = command
        self.text = text
        self.width = width
        self.height = height
        
        # Crear el boton redondeado
        self.create_rounded_button()
        
        # Eventos del raton
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_click)
        
    def create_rounded_button(self, color=None):
        if color is None:
            color = self.color
            
        # Limpiar el canvas
        self.delete('all')
        
        # Dibujar el rectangulo redondeado
        self.create_rounded_rectangle(2, 2, self.width-2, self.height-2, 
                                    radius=self.height//2, fill=color)
        
        # Aniadir el texto
        self.create_text(self.width//2, self.height//2, text=self.text,
                        fill='white', font=Styles.FONTS['button'])
        
    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
        
    def on_enter(self, event):
        self.create_rounded_button(self.hover_color)
        
    def on_leave(self, event):
        self.create_rounded_button(self.color)
        
    def on_click(self, event):
        if self.command:
            self.command()

class CustomDropdown(ttk.Combobox):
    def __init__(self, parent, values, **kwargs):
        super().__init__(parent, values=values, state='readonly', **kwargs)
        self.configure(font=Styles.FONTS['body'])
        
        # Estilo personalizado para el dropdown
        self.option_add('*TCombobox*Listbox.font', Styles.FONTS['body'])
        
        # Configurar estilos
        style = ttk.Style()
        style.configure('TCombobox', 
                       foreground=Styles.COLORS['text'],
                       background=Styles.COLORS['surface'],
                       fieldbackground=Styles.COLORS['surface'],
                       arrowcolor=Styles.COLORS['primary'])

class CustomFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(
            bg=Styles.COLORS['surface'],
            highlightbackground=Styles.COLORS['border'],
            highlightthickness=1,
            padx=15,
            pady=15
        )

class CustomLabel(tk.Label):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(
            bg=Styles.COLORS['surface'],
            fg=Styles.COLORS['text'],
            font=Styles.FONTS['body']
        )

def setup_window_style(window):
    """Configura el estilo basico de una ventana"""
    window.configure(bg=Styles.COLORS['background'])
    
    # Configurar el estilo de los widgets ttk
    style = ttk.Style()
    style.configure('TFrame', background=Styles.COLORS['background'])
    style.configure('TLabel', 
                   background=Styles.COLORS['background'],
                   foreground=Styles.COLORS['text'],
                   font=Styles.FONTS['body'])
    
    return style