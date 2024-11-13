import json
import tkinter as tk
from tkinter import messagebox

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

# Motor de Inferencia
def motor_inferencia(hechos):
    clave = tuple(hechos.values())
    if clave in base_conocimientos:
        recomendacion = base_conocimientos[clave]["recomendacion"]
        explicacion = "\n".join(base_conocimientos[clave]["explicacion"])
        return recomendacion, explicacion
    else:
        return "Lo siento, no tengo una recomendación adecuada. Podrías considerar consultar con un médico general.", ""

# Función para actualizar la base de conocimientos
def actualizar_base_conocimientos():
    cargar_base_conocimientos()

# Función para obtener respuesta del sistema experto
def sistema_experto(hechos):
    recomendacion, explicacion = motor_inferencia(hechos)
    return recomendacion, explicacion

# Interfaz gráfica con tkinter
def interfaz_grafica():
    def obtener_respuesta():
        # Asignar respuestas seleccionadas a los hechos
        hechos["motivo_consulta"] = opcion_motivo.get()
        hechos["nivel_sintomas"] = opcion_sintomas.get()
        hechos["historial_medico"] = opcion_historial.get()
        hechos["edad"] = opcion_edad.get()
        hechos["horario_atencion"] = opcion_horario.get()

        # Obtener respuesta del sistema experto
        recomendacion, explicacion = sistema_experto(hechos)
        resultado_texto.config(state="normal")  # Habilitar edición para mostrar resultado
        resultado_texto.delete(1.0, tk.END)     # Limpiar cuadro de texto
        resultado_texto.insert(tk.END, recomendacion)  # Insertar solo la recomendación
        resultado_texto.config(state="disabled")  # Deshabilitar edición

        # Guardar la explicación para mostrarla después
        global explicacion_guardada
        explicacion_guardada = explicacion

        # Habilitar el botón de mostrar explicación
        boton_explicacion.config(state="normal")
    
    def mostrar_explicacion():
        # Añadir la explicación al resultado si no está ya
        if explicacion_guardada:
            resultado_texto.config(state="normal")
            resultado_texto.insert(tk.END, "\n\nEXPLICACIÓN:\n" + explicacion_guardada)
            resultado_texto.config(state="disabled")
        
        # Deshabilitar el botón para evitar múltiples clics
        boton_explicacion.config(state="disabled")

    # Configuración de la ventana principal
    ventana = tk.Tk()
    ventana.title("Sistema Experto - Asignación de Doctor")
    ventana.geometry("600x600")

    # Preguntas y opciones
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

    # Botón para enviar respuestas y mostrar el resultado
    boton_responder = tk.Button(ventana, text="Obtener Asignación de Doctor", command=obtener_respuesta)
    boton_responder.pack(pady=10)

    # Botón para mostrar explicación
    boton_explicacion = tk.Button(ventana, text="Mostrar explicación", state="disabled", command=mostrar_explicacion)
    boton_explicacion.pack(pady=10)

    # Área de texto para mostrar el resultado
    tk.Label(ventana, text="Resultado del Sistema Experto:").pack()
    resultado_texto = tk.Text(ventana, height=10, width=70, state="disabled", wrap="word")
    resultado_texto.pack()

    ventana.mainloop()

# Cargar la base de conocimientos y ejecutar la interfaz gráfica
if __name__ == "__main__":
    actualizar_base_conocimientos()
    interfaz_grafica()
