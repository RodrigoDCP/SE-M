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

# 3. Motor de Inferencia: Determina la respuesta del sistema experto según los hechos
def motor_inferencia(hechos):
    clave = tuple(hechos.values())  # Crear una clave basada en todas las respuestas
    if clave in base_conocimientos:
        recomendacion = base_conocimientos[clave]["recomendacion"]
        explicacion = "\n".join(base_conocimientos[clave]["explicacion"])  # Unir la lista de explicaciones con saltos de línea
        return f"RESPUESTA: {recomendacion}\n\nEXPLICACIÓN:\n{explicacion}"
    else:
        return "Lo siento, no tengo una recomendación adecuada, pero podrías considerar consultar con un médico general."


# 4. Función para actualizar la base de conocimientos (esto lo haría el experto)
def actualizar_base_conocimientos():
    # Ejemplo de actualización, añadiendo reglas personalizadas
    base_conocimientos[("Dolor", "Leve", "No", "Menos de 18 años", "Matutino")] = {
        "recomendacion": "Dr. García, Pediatra",
        "explicacion": [
            "- Especialista en el cuidado y tratamiento de niños.",
            "- Consultas disponibles en horario matutino.",
            "- Consulta en 2-3 días hábiles.",
            "- Costo por consulta: $800."
        ]
    }

    # Regla 2: Dolor, Fuerte, Sin antecedentes, Menos de 18 años, Matutino
    base_conocimientos[("Dolor", "Fuerte", "No", "Menos de 18 años", "Matutino")] = {
        "recomendacion": "Dr. López, Urgencias Pediátricas",
        "explicacion": [
            "- Especialista en urgencias pediátricas.",
            "- Consultas disponibles de inmediato.",
            "- Costo por consulta urgente: $1200."
        ]
    }

    # Agregar más reglas como sea necesario.
    # Agregar más reglas como sea necesario.
    # Agregar más reglas como sea necesario.
    # Agregar más reglas como sea necesario.
    # Agregar más reglas como sea necesario.
    # Agregar más reglas como sea necesario.
    # Agregar más reglas como sea necesario.
    # Agregar más reglas como sea necesario.
    # Agregar más reglas como sea necesario.

# 5. Función principal para obtener la respuesta del sistema experto
def sistema_experto(hechos):
    respuesta = motor_inferencia(hechos)
    return respuesta  # Retornamos directamente la respuesta de motor_inferencia

# 6. Función para mostrar preguntas y recibir respuestas por número
def seleccionar_respuesta(pregunta, opciones):
    print(f"{pregunta}")
    for i, opcion in enumerate(opciones, 1):
        print(f"{i}. {opcion}")
    seleccion = int(input("Selecciona una opción (1, 2, 3, etc.): "))
    return opciones[seleccion - 1]

# 7. Interfaz de usuario para recibir entradas y mostrar resultados
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
    # Primero, actualizamos la base de conocimientos con algunas reglas
    actualizar_base_conocimientos()
    
    # Luego ejecutamos la interfaz de usuario
    interfaz_usuario()
