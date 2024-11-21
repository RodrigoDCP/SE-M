# SISMED "Sistema de asignación médica"

**Definición**: SISMED es una herramienta sencilla que asigna médicos a pacientes de forma rápida y fácil. Funciona como un **bot** que hace una serie de preguntas al paciente sobre su motivo de consulta, síntomas, historial médico y cuándo está disponible. Con base en las respuestas, *el sistema busca al médico más adecuado según la especialidad y el horario disponible*.

## Tabla de preguntas y respuestas

| *Criterio*            | *Pregunta*                                        | *Resp 1*                  | *Resp 2*                     | *Resp 3*               | *Resp 4*            |
| --------------------- | ------------------------------------------------- | ------------------------- | ---------------------------- | ---------------------- | ------------------- |
| 1. Motivo de consulta | ¿Cuál es el motivo principal de la consulta?      | Dolor                     | Control de salud             | Revisión de síntomas   | Consulta preventiva |
| 2. Nivel de síntomas  | ¿Cómo calificaría la intensidad de sus síntomas?  | Leve                      | Moderado                     | Fuerte                 | Muy fuerte          |
| 3. Historial médico   | ¿Tiene antecedentes de alguna enfermedad crónica? | Alergias a algún alimento | Alergias a algún medicamento | Operaciones o cirugías | No                  |
| 4. Edad               | ¿Cuál es la edad del paciente?                    | Menos de 18 años          | Entre 18-35 años             | Entre 36-60 años       | Más de 60 años      |
### Ejemplo Rama 1:

| *Pregunta*                                        | *Respuestas del usuario* | *Respuesta del Sistema Experto*                                                                                                                                                                                                                                   |
| ------------------------------------------------- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ¿Cuál es el motivo principal de la consulta?      | Dolor                    | RESPUESTA: Se recomienda al Dr. Rodríguez, Médico General. <br><br> EXPLICACIÓN:<br>- Experto en tratar una amplia gama de problemas de salud.<br>- Consultas disponibles en horario vespertino.<br>- Consulta en 2-3 días hábiles<br>- Costo por consulta: $900. |
| ¿Cómo calificaría la intensidad de sus síntomas?  | Moderado                 |                                                                                                                                                                                                                                                                   |
| ¿Tiene antecedentes de alguna enfermedad crónica? | No                       |                                                                                                                                                                                                                                                                   |
| ¿Cuál es la edad del paciente?                    | Entre 18-35 años         |                                                                                                                                                                                                                                                                   |

### Ejemplo Rama 2:

| *Pregunta*                                        | *Respuestas del usuario* | *Respuesta del Sistema Experto*                                                                                                                                                              |
| ------------------------------------------------- | ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ¿Cuál es el motivo principal de la consulta?      | Dolor                    | RESPUESTA: Dr. López, Urgencias Pediátricas<br><br>EXPLICACIÓN:<br>- Especialista en urgencias pediátricas.<br>- Consultas disponibles de inmediato.<br>- Costo por consulta urgente: $1200. |
| ¿Cómo calificaría la intensidad de sus síntomas?  | Fuerte                   |                                                                                                                                                                                              |
| ¿Tiene antecedentes de alguna enfermedad crónica? | No                       |                                                                                                                                                                                              |
| ¿Cuál es la edad del paciente?                    | Menos de 18 años         |                                                                                                                                                                                              |

## Base de hechos

~~~python
# 1. Base de Hechos: Datos específicos del paciente
hechos = {
    "motivo_consulta": "",
    "nivel_sintomas": "",
    "historial_medico": "",
    "edad": "",
}
~~~

## Base de conocimientos

~~~json
{
	{
    "('Revisión de síntomas', 'Muy fuerte', 'Operaciones o cirugías', 'Más de 60 años')": {
        "recomendacion": "Dra. Ana García, Cirujana General",
        "explicacion": [
            "- Especialista en tratar síntomas severos postquirúrgicos en adultos mayores.",
            "- Ofrece seguimiento cercano y diagnóstico inmediato para evitar complicaciones.",
            "- Recomendado para personas mayores con dolor severo después de la cirugía.",
            "- Costo por consulta: $800."
        ],
        "imagen": "/home/keny/Descargas/descom/image/doc8.jpeg"
    }
}
~~~

## Respuestas

~~~python
def motor_inferencia(hechos):
    clave = tuple(hechos.values())
    if clave in base_conocimientos:
        recomendacion = base_conocimientos[clave]["recomendacion"]
        explicacion = "\n".join(base_conocimientos[clave]["explicacion"])
        imagen_path = base_conocimientos[clave]["imagen"]
        return recomendacion, explicacion, imagen_path
    else:
        return "Lo siento, no tengo una recomendación adecuada. Podrías considerar consultar con un médico general.", "", None

~~~


