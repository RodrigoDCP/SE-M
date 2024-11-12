import json

# 1. Base de Hechos: Datos específicos del paciente
hechos = {
    "motivo_consulta": "",
    "nivel_sintomas": "",
    "historial_medico": "",
    "edad": "",
    "horario_atencion": ""
}

# 2. Base de Conocimientos: Reglas que determinan qué respuesta ofrecer según las respuestas del usuario
base_conocimientos = {}

# 3. Cargar la base de conocimientos desde un archivo JSON
def cargar_base_conocimientos():
    global base_conocimientos
    try:
        with open('base_conocimientos.json', 'r') as archivo_json:
            datos_json = json.load(archivo_json)
            base_conocimientos = {}
            
            # Convierte cada clave de cadena a tupla de forma segura
            for clave, valor in datos_json.items():
                # Remueve los paréntesis y divide los elementos en una lista
                clave_tupla = tuple(clave.strip("()").replace("'", "").split(", "))
                base_conocimientos[clave_tupla] = valor
            
            # Comentada la línea que imprime la base de conocimientos
            # print("Base de conocimientos cargada:", base_conocimientos)  # Verifica el contenido cargado
    except FileNotFoundError:
        print("No se encontró el archivo de base de conocimientos. Se usará una base vacía.")
    except json.JSONDecodeError:
        print("Hubo un error al leer el archivo de base de conocimientos.")

# 4. Guardar la base de conocimientos a un archivo JSON
def guardar_base_conocimientos():
    try:
        # Convertimos las claves de vuelta a cadenas de texto antes de guardarlas
        datos_json = {str(clave): valor for clave, valor in base_conocimientos.items()}
        with open('base_conocimientos.json', 'w') as archivo_json:
            json.dump(datos_json, archivo_json, indent=4)
    except Exception as e:
        print(f"Error al guardar la base de conocimientos: {e}")

# 5. Motor de Inferencia: Determina la respuesta del sistema experto según los hechos
def motor_inferencia(hechos):
    clave = tuple(hechos.values())  # Crear una clave basada en todas las respuestas
    if clave in base_conocimientos:
        recomendacion = base_conocimientos[clave]["recomendacion"]
        explicacion = "\n".join(base_conocimientos[clave]["explicacion"])  # Unir la lista de explicaciones con saltos de línea
        return f"RESPUESTA: {recomendacion}\n\nEXPLICACIÓN:\n{explicacion}"
    else:
        return "Lo siento, no tengo una recomendación adecuada, pero podrías considerar consultar con un médico general."

# 6. Función para actualizar la base de conocimientos (ahora solo carga el JSON)
def actualizar_base_conocimientos():
    cargar_base_conocimientos()  # Solo se carga la base de conocimientos desde el JSON

# 7. Función principal para obtener la respuesta del sistema experto
def sistema_experto(hechos):
    respuesta = motor_inferencia(hechos)
    return respuesta  # Retornamos directamente la respuesta de motor_inferencia

# 8. Función para mostrar preguntas y recibir respuestas por número
def seleccionar_respuesta(pregunta, opciones):
    print(f"{pregunta}")
    for i, opcion in enumerate(opciones, 1):
        print(f"{i}. {opcion}")
    seleccion = int(input("Selecciona una opción (1, 2, 3, etc.): "))
    return opciones[seleccion - 1]

# 9. Interfaz de usuario para recibir entradas y mostrar resultados
def interfaz_usuario():
    # Recibir las respuestas del paciente
    print("Responde las siguientes preguntas:")
    hechos["motivo_consulta"] = seleccionar_respuesta("¿Cuál es el motivo principal de la consulta?", 
                                                      ["Dolor", "Control de salud", "Revisión de síntomas", "Consulta preventiva"])
    hechos["nivel_sintomas"] = seleccionar_respuesta("¿Cómo calificaría la intensidad de sus síntomas?", 
                                                     ["Leve", "Moderado", "Fuerte", "Muy fuerte"])
    hechos["historial_medico"] = seleccionar_respuesta("¿Tiene antecedentes de alguna enfermedad crónica?", 
                                                      ["Alergias a algún alimento", "Alergias a algún medicamento", "Operaciones o cirugías", "No"])
    hechos["edad"] = seleccionar_respuesta("¿Cuál es la edad del paciente?", 
                                           ["Menos de 18 años", "Entre 18-35 años", "Entre 36-60 años", "Más de 60 años"])
    hechos["horario_atencion"] = seleccionar_respuesta("¿Qué horario de atención necesita?", 
                                                       ["Matutino", "Vespertino", "Nocturno", "Fines de semana"])
    
    # Mostrar la respuesta del sistema experto
    print("-----------------------------")
    resultado = sistema_experto(hechos)
    print("\n" + resultado)

# Llamada para ejecutar la interfaz de usuario
if __name__ == "__main__":
    # Primero, actualizamos la base de conocimientos desde el archivo JSON
    actualizar_base_conocimientos()
    
    # Luego ejecutamos la interfaz de usuario
    interfaz_usuario()