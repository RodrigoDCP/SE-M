import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from motor import MotorInferencia
from custom_styles import Styles, CustomButton, CustomFrame, CustomLabel, setup_window_style

def aprender_conocimiento(ventana_padre, hechos_actuales, callback_actualizacion=None):
    def cargar_imagen():
        ventana_memoria.grab_release()  # Liberar temporalmente el control
        ruta_imagen = filedialog.askopenfilename(
            title="Selecciona una imagen",
            filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.gif")]
        )
        ventana_memoria.grab_set()  # Recuperar el control
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

        if MotorInferencia.guardar_conocimiento(hechos_actuales, doctor, explicacion, imagen):
            if callback_actualizacion:
                callback_actualizacion()
            messagebox.showinfo("Exito", "Nuevo conocimiento guardado exitosamente!")
            ventana_memoria.destroy()
        else:
            messagebox.showerror("Error", "No se pudo guardar el conocimiento")

    # Configuración de la ventana
    ventana_memoria = tk.Toplevel(ventana_padre)
    ventana_memoria.title("Agregar Nuevo Conocimiento")
    ventana_memoria.geometry("900x600")
    
    # Hacer la ventana modal
    ventana_memoria.transient(ventana_padre)
    ventana_memoria.grab_set()
    ventana_memoria.focus_set()
    
    setup_window_style(ventana_memoria)

    # Frame principal
    main_frame = CustomFrame(ventana_memoria)
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
    
    # Botón seleccionar imagen
    CustomButton(
        imagen_frame,
        text="Seleccionar",
        command=cargar_imagen,
        width=100,
        color=Styles.COLORS['secondary']
    ).pack(side='right')

    # Botón guardar
    CustomButton(
        main_frame,
        text="Guardar Conocimiento",
        command=guardar_nuevo_conocimiento,
        width=200
    ).pack(pady=(20, 0))