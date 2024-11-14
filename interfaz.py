import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Asegúrate de instalar pillow: pip install pillow
from memoria import aprender_conocimiento
from tkinter import filedialog


# 1. Base de Hechos
hechos = {
    "motivo_consulta": "",
    "nivel_sintomas": "",
    "historial_medico": "",
    "edad": "",
    "horario_atencion": ""
}

# 2. Base de Conocimientos
base_conocimientos = {}

# Cargar la base de conocimientos desde un archivo JSON
def cargar_base_conocimientos():
    global base_conocimientos
    try:
        with open('base_conocimientos.json', 'r') as archivo_json:
            datos_json = json.load(archivo_json)
            base_conocimientos = {}
            
            for clave, valor in datos_json.items():
                clave_tupla = tuple(clave.strip("()").replace("'", "").split(", "))
                base_conocimientos[clave_tupla] = valor
    except FileNotFoundError:
        print("No se encontró el archivo de base de conocimientos. Se usará una base vacía.")
    except json.JSONDecodeError:
        print("Hubo un error al leer el archivo de base de conocimientos.")

# Guardar la base de conocimientos en un archivo JSON
def guardar_base_conocimientos():
    datos_json = {str(clave): valor for clave, valor in base_conocimientos.items()}
    with open('base_conocimientos.json', 'w') as archivo_json:
        json.dump(datos_json, archivo_json, indent=4)

# Motor de Inferencia
def motor_inferencia(hechos):
    clave = tuple(hechos.values())
    if clave in base_conocimientos:
        recomendacion = base_conocimientos[clave]["recomendacion"]
        explicacion = "\n".join(base_conocimientos[clave]["explicacion"])
        imagen_path = base_conocimientos[clave]["imagen"]
        return recomendacion, explicacion, imagen_path
    else:
        return "Lo siento, no tengo una recomendación adecuada. Podrías considerar consultar con un médico general.", "", None

# Función para actualizar la base de conocimientos
def actualizar_base_conocimientos():
    cargar_base_conocimientos()

# Función para obtener respuesta del sistema experto
def sistema_experto(hechos):
    recomendacion, explicacion, imagen_path = motor_inferencia(hechos)
    return recomendacion, explicacion, imagen_path


def interfaz_grafica():
    def obtener_respuesta():
        hechos["motivo_consulta"] = opcion_motivo.get()
        hechos["nivel_sintomas"] = opcion_sintomas.get()
        hechos["historial_medico"] = opcion_historial.get()
        hechos["edad"] = opcion_edad.get()
        hechos["horario_atencion"] = opcion_horario.get()

        recomendacion, explicacion, imagen_path = sistema_experto(hechos)
        resultado_texto.config(state="normal")
        resultado_texto.delete(1.0, tk.END)
        resultado_texto.insert(tk.END, recomendacion)
        resultado_texto.config(state="disabled")

        global explicacion_guardada, imagen_guardada
        explicacion_guardada = explicacion
        imagen_guardada = imagen_path

        boton_explicacion.config(state="normal")
        boton_ver_doctor.config(state="normal")

    def abrir_ventana_aprender():
        aprender_conocimiento()
    
    def mostrar_explicacion():
        if explicacion_guardada:
            resultado_texto.config(state="normal")
            resultado_texto.insert(tk.END, "\n\nEXPLICACIÓN:\n" + explicacion_guardada)
            resultado_texto.config(state="disabled")
        boton_explicacion.config(state="disabled")

    def mostrar_imagen():
        if imagen_guardada:
            imagen = Image.open(imagen_guardada)
            imagen = imagen.resize((150, 150), Image.LANCZOS)
            imagen_tk = ImageTk.PhotoImage(imagen)
            label_imagen.config(image=imagen_tk)
            label_imagen.image = imagen_tk

    ventana = tk.Tk()
    ventana.title("Sistema Experto - Asignación de Doctor")
    ventana.geometry("600x700")

    tk.Label(ventana, text="¿Cuál es el motivo principal de la consulta?").pack()
    opcion_motivo = tk.StringVar(value="Dolor")
    tk.OptionMenu(ventana, opcion_motivo, "Dolor", "Control de salud", "Revisión de síntomas", "Consulta preventiva").pack()

    tk.Label(ventana, text="¿Cómo calificaría la intensidad de sus síntomas?").pack()
    opcion_sintomas = tk.StringVar(value="Leve")
    tk.OptionMenu(ventana, opcion_sintomas, "Leve", "Moderado", "Fuerte", "Muy fuerte").pack()

    tk.Label(ventana, text="¿Tiene antecedentes de alguna enfermedad crónica?").pack()
    opcion_historial = tk.StringVar(value="No")
    tk.OptionMenu(ventana, opcion_historial, "Alergias a algún alimento", "Alergias a algún medicamento", "Operaciones o cirugías", "No").pack()

    tk.Label(ventana, text="¿Cuál es la edad del paciente?").pack()
    opcion_edad = tk.StringVar(value="Entre 18-35 años")
    tk.OptionMenu(ventana, opcion_edad, "Menos de 18 años", "Entre 18-35 años", "Entre 36-60 años", "Más de 60 años").pack()

    tk.Label(ventana, text="¿Qué horario de atención necesita?").pack()
    opcion_horario = tk.StringVar(value="Matutino")
    tk.OptionMenu(ventana, opcion_horario, "Matutino", "Vespertino", "Nocturno", "Fines de semana").pack()

    boton_aprender = tk.Button(ventana, text="Aprender", command=abrir_ventana_aprender)
    boton_aprender.pack(pady=10)

    boton_responder = tk.Button(ventana, text="Obtener Asignación de Doctor", command=obtener_respuesta)
    boton_responder.pack(pady=10)

    boton_explicacion = tk.Button(ventana, text="Mostrar explicación", state="disabled", command=mostrar_explicacion)
    boton_explicacion.pack(pady=10)

    boton_ver_doctor = tk.Button(ventana, text="Ver Doctor", state="disabled", command=mostrar_imagen)
    boton_ver_doctor.pack(pady=10)

    tk.Label(ventana, text="Resultado del Sistema Experto:").pack()
    resultado_texto = tk.Text(ventana, height=10, width=70, state="disabled", wrap="word")
    resultado_texto.pack()

    label_imagen = tk.Label(ventana)
    label_imagen.pack(pady=10)

    ventana.mainloop()

if __name__ == "__main__":
    cargar_base_conocimientos()
    interfaz_grafica()

