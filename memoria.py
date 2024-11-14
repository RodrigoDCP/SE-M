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
    campo_motivo = tk.Entry(ventana_aprender)
    campo_motivo.pack()

    tk.Label(ventana_aprender, text="Nivel de síntomas:").pack()
    campo_sintomas = tk.Entry(ventana_aprender)
    campo_sintomas.pack()

    tk.Label(ventana_aprender, text="Historial médico:").pack()
    campo_historial = tk.Entry(ventana_aprender)
    campo_historial.pack()

    tk.Label(ventana_aprender, text="Edad del paciente:").pack()
    campo_edad = tk.Entry(ventana_aprender)
    campo_edad.pack()

    tk.Label(ventana_aprender, text="Horario de atención:").pack()
    campo_horario = tk.Entry(ventana_aprender)
    campo_horario.pack()

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
