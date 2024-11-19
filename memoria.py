import tkinter as tk
import json
from tkinter import filedialog, messagebox

def cargar_base_conocimientos():
    """Carga la base de conocimientos desde un archivo JSON."""
    try:
        with open('base_conocimientos.json', 'r') as archivo_json:
            datos_json = json.load(archivo_json)
            return datos_json
    except FileNotFoundError:
        return {}  # Si no existe el archivo, retornamos un diccionario vacío

def guardar_base_conocimientos(base_conocimientos):
    """Guarda la base de conocimientos en un archivo JSON."""
    with open('base_conocimientos.json', 'w') as archivo_json:
        json.dump(base_conocimientos, archivo_json, indent=4)

def aprender_conocimiento():
    def cargar_imagen():
        """Función para abrir un cuadro de diálogo y seleccionar una imagen."""
        ruta_imagen = filedialog.askopenfilename(title="Selecciona una imagen", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.gif")])
        if ruta_imagen:
            campo_imagen.delete(0, tk.END)  # Borrar texto anterior
            campo_imagen.insert(0, ruta_imagen)  # Insertar la ruta seleccionada

    def guardar_nuevo_conocimiento():
        # Obtiene los datos ingresados en la ventana
        motivo = campo_motivo.get()
        sintomas = campo_sintomas.get()
        historial = campo_historial.get()
        edad = campo_edad.get()
        horario = campo_horario.get()
        doctor = campo_doctor.get()
        explicacion = campo_explicacion.get("1.0", tk.END).strip()
        imagen = campo_imagen.get()  # Obtener la ruta de la imagen seleccionada

        # Creando la clave como una tupla con los datos ingresados
        clave = (motivo, sintomas, historial, edad, horario)

        # Cargar la base de conocimientos actual
        base_conocimientos = cargar_base_conocimientos()

        # Guardar los nuevos datos en la base de conocimientos
        base_conocimientos[str(clave)] = {
            "recomendacion": doctor,
            "explicacion": explicacion.splitlines(),
            "imagen": imagen  # Guardar la ruta de la imagen
        }

        # Guardamos la base de conocimientos actualizada
        guardar_base_conocimientos(base_conocimientos)

        # Confirmamos que se guardó correctamente
        messagebox.showinfo("Éxito", "¡Nuevo conocimiento guardado exitosamente!")
        ventana_aprender.destroy()

    # Creamos la ventana secundaria para aprender un nuevo conocimiento
    ventana_aprender = tk.Toplevel()
    ventana_aprender.title("Aprender Nuevo Conocimiento")
    ventana_aprender.geometry("400x600")

    # Solicitamos los datos para la base de conocimientos
    tk.Label(ventana_aprender, text="Nombre del doctor:").pack()
    campo_doctor = tk.Entry(ventana_aprender)
    campo_doctor.pack()

    tk.Label(ventana_aprender, text="Motivo de la consulta:").pack()
    opciones_motivo = ["Dolor", "Control de salud", "Revisión de síntomas", "Consulta preventiva"]
    campo_motivo = tk.StringVar(ventana_aprender)
    campo_motivo.set(opciones_motivo[0])  # Valor predeterminado
    menu_motivo = tk.OptionMenu(ventana_aprender, campo_motivo, *opciones_motivo)
    menu_motivo.pack()

    tk.Label(ventana_aprender, text="Nivel de síntomas:").pack()
    opciones_sintomas = ["Leve", "Moderado", "Fuerte", "Muy fuerte"]
    campo_sintomas = tk.StringVar(ventana_aprender)
    campo_sintomas.set(opciones_sintomas[0])  # Valor predeterminado
    menu_sintomas = tk.OptionMenu(ventana_aprender, campo_sintomas, *opciones_sintomas)
    menu_sintomas.pack()

    tk.Label(ventana_aprender, text="Historial médico:").pack()
    opciones_historial = ["No", "Operaciones o cirugías", "Alergias a algún alimento", "Alergias a algún medicamento"]
    campo_historial = tk.StringVar(ventana_aprender)
    campo_historial.set(opciones_historial[0])  # Valor predeterminado
    menu_historial = tk.OptionMenu(ventana_aprender, campo_historial, *opciones_historial)
    menu_historial.pack()

    tk.Label(ventana_aprender, text="Edad del paciente:").pack()
    opciones_edad = ["Menor de 18 años", "Entre 18-35 años", "Entre 36-60 años", "Más de 60 años"]
    campo_edad = tk.StringVar(ventana_aprender)
    campo_edad.set(opciones_edad[0])  # Valor predeterminado
    menu_edad = tk.OptionMenu(ventana_aprender, campo_edad, *opciones_edad)
    menu_edad.pack()

    tk.Label(ventana_aprender, text="Horario de atención:").pack()
    opciones_horario = ["Matutino", "Vespertino", "Nocturno", "Fines de semana"]
    campo_horario = tk.StringVar(ventana_aprender)
    campo_horario.set(opciones_horario[0])  # Valor predeterminado
    menu_horario = tk.OptionMenu(ventana_aprender, campo_horario, *opciones_horario)
    menu_horario.pack()


    tk.Label(ventana_aprender, text="Explicación del conocimiento:").pack()
    campo_explicacion = tk.Text(ventana_aprender, height=5, width=40)
    campo_explicacion.pack()

    # Campo para la ruta de la imagen
    tk.Label(ventana_aprender, text="Selecciona una imagen:").pack()
    campo_imagen = tk.Entry(ventana_aprender)
    campo_imagen.pack()

    # Botón para seleccionar la imagen
    boton_imagen = tk.Button(ventana_aprender, text="Seleccionar Imagen", command=cargar_imagen)
    boton_imagen.pack(pady=10)

    # Botón para guardar el conocimiento
    boton_guardar = tk.Button(ventana_aprender, text="Guardar Conocimiento", command=guardar_nuevo_conocimiento)
    boton_guardar.pack(pady=10)

    ventana_aprender.mainloop()
