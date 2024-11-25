import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import json
from custom_styles import Styles, CustomButton, CustomFrame, CustomLabel, setup_window_style

def cargar_base_conocimientos():
    try:
        with open('base_conocimientos.json', 'r') as archivo_json:
            return json.load(archivo_json)
    except FileNotFoundError:
        return {}

def guardar_base_conocimientos(base_conocimientos):
    with open('base_conocimientos.json', 'w') as archivo_json:
        json.dump(base_conocimientos, archivo_json, indent=4)

def aprender_conocimiento(ventana_padre, hechos_actuales, callback_actualizacion=None):
    def cargar_imagen():
        ruta_imagen = filedialog.askopenfilename(
            title="Selecciona una imagen",
            filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.gif")]
        )
        if ruta_imagen:
            campo_imagen.delete(0, tk.END)
            campo_imagen.insert(0, ruta_imagen)

    def guardar_nuevo_conocimiento():
        doctor = campo_doctor.get()
        explicacion = campo_explicacion.get("1.0", tk.END).strip()
        imagen = campo_imagen.get()

        if not all([doctor, explicacion, imagen]):
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return

        clave = (
            hechos_actuales["motivo_consulta"],
            hechos_actuales["nivel_sintomas"],
            hechos_actuales["historial_medico"],
            hechos_actuales["edad"]
        )

        base_conocimientos = cargar_base_conocimientos()
        base_conocimientos[str(clave)] = {
            "recomendacion": doctor,
            "explicacion": explicacion.splitlines(),
            "imagen": imagen
        }

        guardar_base_conocimientos(base_conocimientos)

        if callback_actualizacion:
            callback_actualizacion()
        else:
            messagebox.showinfo("Exito", "Nuevo conocimiento guardado exitosamente!")
            ventana_padre.destroy()

    # Configuración de la ventana
    ventana_padre.title("Agregar Nuevo Conocimiento")
    ventana_padre.geometry("900x600")  # Ventana más ancha para las dos columnas
    setup_window_style(ventana_padre)

    # Frame principal
    main_frame = CustomFrame(ventana_padre)
    main_frame.pack(expand=True, fill='both', padx=20, pady=20)

    # Título principal
    titulo = CustomLabel(
        main_frame,
        text="Agregar Nuevo Conocimiento",
        font=Styles.FONTS['subheading'],
        fg=Styles.COLORS['primary']
    )
    titulo.pack(pady=(0, 20))

    # Contenedor para las dos columnas
    columns_frame = tk.Frame(main_frame, bg=Styles.COLORS['surface'])
    columns_frame.pack(fill='both', expand=True)

    # Columna izquierda (Datos del caso)
    left_frame = CustomFrame(columns_frame)
    left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

    # Título datos del caso
    CustomLabel(
        left_frame,
        text="Datos del Caso",
        font=Styles.FONTS['body_bold'],
        fg=Styles.COLORS['primary']
    ).pack(pady=(0, 10))

    # Mostrar los datos del caso
    for key, value in hechos_actuales.items():
        case_frame = tk.Frame(left_frame, bg=Styles.COLORS['surface'])
        case_frame.pack(fill='x', pady=5)
        
        CustomLabel(
            case_frame,
            text=f"{key.replace('_', ' ').title()}:",
            font=Styles.FONTS['body_bold'],
            fg=Styles.COLORS['secondary'],
            width=15,
            anchor='e'
        ).pack(side='left', padx=(5, 10))
        
        CustomLabel(
            case_frame,
            text=value,
            anchor='w'
        ).pack(side='left')

    # Columna derecha (Formulario)
    right_frame = CustomFrame(columns_frame)
    right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))

    # Campo doctor
    CustomLabel(
        right_frame,
        text="Nombre del doctor:",
        font=Styles.FONTS['body_bold'],
        fg=Styles.COLORS['secondary']
    ).pack(anchor='w', pady=(0, 5))
    
    campo_doctor = tk.Entry(
        right_frame,
        font=Styles.FONTS['body'],
        bg='white'
    )
    campo_doctor.pack(fill='x', pady=(0, 10))

    # Campo explicación
    CustomLabel(
        right_frame,
        text="Explicacion del conocimiento:",
        font=Styles.FONTS['body_bold'],
        fg=Styles.COLORS['secondary']
    ).pack(anchor='w', pady=(0, 5))
    
    campo_explicacion = scrolledtext.ScrolledText(
        right_frame,
        font=Styles.FONTS['body'],
        bg='white',
        height=8,
        wrap=tk.WORD
    )
    campo_explicacion.pack(fill='x', pady=(0, 10))

    # Campo imagen
    CustomLabel(
        right_frame,
        text="Imagen del doctor:",
        font=Styles.FONTS['body_bold'],
        fg=Styles.COLORS['secondary']
    ).pack(anchor='w', pady=(0, 5))
    
    imagen_frame = tk.Frame(right_frame, bg=Styles.COLORS['surface'])
    imagen_frame.pack(fill='x', pady=(0, 15))
    
    campo_imagen = tk.Entry(
        imagen_frame,
        font=Styles.FONTS['body'],
        bg='white'
    )
    campo_imagen.pack(side='left', fill='x', expand=True, padx=(0, 10))
    
    CustomButton(
        imagen_frame,
        text="Seleccionar",
        command=cargar_imagen,
        width=100,
        color=Styles.COLORS['secondary']
    ).pack(side='right')

    # Botón guardar centrado en la parte inferior
    CustomButton(
        main_frame,
        text="Guardar Conocimiento",
        command=guardar_nuevo_conocimiento,
        width=200
    ).pack(pady=(20, 0))