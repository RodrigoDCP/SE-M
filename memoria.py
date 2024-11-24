import tkinter as tk
from tkinter import filedialog, messagebox
import json

def cargar_base_conocimientos():
    """Carga la base de conocimientos desde un archivo JSON."""
    try:
        with open('base_conocimientos.json', 'r') as archivo_json:
            datos_json = json.load(archivo_json)
            return datos_json
    except FileNotFoundError:
        return {}

def guardar_base_conocimientos(base_conocimientos):
    """Guarda la base de conocimientos en un archivo JSON."""
    with open('base_conocimientos.json', 'w') as archivo_json:
        json.dump(base_conocimientos, archivo_json, indent=4)

def aprender_conocimiento(ventana_padre, hechos_actuales, callback_actualizacion=None):
    """Funcion para aprender nuevo conocimiento basado en los hechos actuales."""
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

        # Creando la clave como una tupla con los hechos actuales
        clave = (
            hechos_actuales["motivo_consulta"],
            hechos_actuales["nivel_sintomas"],
            hechos_actuales["historial_medico"],
            hechos_actuales["edad"]
        )

        # Cargar la base de conocimientos actual
        base_conocimientos = cargar_base_conocimientos()

        # Guardar los nuevos datos
        base_conocimientos[str(clave)] = {
            "recomendacion": doctor,
            "explicacion": explicacion.splitlines(),
            "imagen": imagen
        }

        # Guardar la base de conocimientos actualizada
        guardar_base_conocimientos(base_conocimientos)

        # Llamar al callback de actualizacion si existe
        if callback_actualizacion:
            callback_actualizacion()
        else:
            messagebox.showinfo("exito", "¡Nuevo conocimiento guardado exitosamente!")
            ventana_padre.destroy()

    # Configuracion de la ventana de aprendizaje
    ventana_padre.title("Aprender Nuevo Conocimiento")
    ventana_padre.geometry("400x600")

    # Mostrar los hechos actuales
    tk.Label(ventana_padre, text="Hechos del caso:").pack()
    texto_hechos = f"""
    Motivo: {hechos_actuales['motivo_consulta']}
    Nivel: {hechos_actuales['nivel_sintomas']}
    Historial: {hechos_actuales['historial_medico']}
    Edad: {hechos_actuales['edad']}
    """
    tk.Label(ventana_padre, text=texto_hechos, justify=tk.LEFT).pack()

    tk.Label(ventana_padre, text="Nombre del doctor:").pack()
    campo_doctor = tk.Entry(ventana_padre)
    campo_doctor.pack()

    tk.Label(ventana_padre, text="Explicacion del conocimiento:").pack()
    campo_explicacion = tk.Text(ventana_padre, height=5, width=40)
    campo_explicacion.pack()

    tk.Label(ventana_padre, text="Selecciona una imagen:").pack()
    campo_imagen = tk.Entry(ventana_padre)
    campo_imagen.pack()

    boton_imagen = tk.Button(ventana_padre, text="Seleccionar Imagen", command=cargar_imagen)
    boton_imagen.pack(pady=10)

    boton_guardar = tk.Button(ventana_padre, text="Guardar Conocimiento", command=guardar_nuevo_conocimiento)
    boton_guardar.pack(pady=10)