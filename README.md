### Documentación: `interfaz.py`
---
**Equipo 3: Rodrigo Cañas, Jorge Sarricolea, Daniel Toache, Melisa Vazquez**
## Descripción

SISMED es una herramienta sencilla que asigna médicos a pacientes de forma rápida y fácil. Funciona como un **bot** que hace una serie de preguntas al paciente sobre su motivo de consulta, síntomas, historial médico y cuándo está disponible. Con base en las respuestas, *el sistema busca al médico más adecuado según la especialidad y el horario disponible*.


| *Criterio*            | *Pregunta*                                        | *Resp 1*                  | *Resp 2*                     | *Resp 3*               | *Resp 4*            |
| --------------------- | ------------------------------------------------- | ------------------------- | ---------------------------- | ---------------------- | ------------------- |
| 1. Motivo de consulta | ¿Cuál es el motivo principal de la consulta?      | Dolor                     | Control de salud             | Revisión de síntomas   | Consulta preventiva |
| 2. Nivel de síntomas  | ¿Cómo calificaría la intensidad de sus síntomas?  | Leve                      | Moderado                     | Fuerte                 | Muy fuerte          |
| 3. Historial médico   | ¿Tiene antecedentes de alguna enfermedad crónica? | Alergias a algún alimento | Alergias a algún medicamento | Operaciones o cirugías | No                  |
| 4. Edad               | ¿Cuál es la edad del paciente?                    | Menos de 18 años          | Entre 18-35 años             | Entre 36-60 años       | Más de 60 años      |


## Funcionalidades Principales

1. **Interfaz gráfica intuitiva**:

   - Captura información del paciente mediante formularios interactivos con listas desplegables y campos seleccionables.
   - Visualización de resultados, explicaciones y recomendaciones dentro de la misma interfaz.

2. **Motor de inferencia**:

   - Realiza consultas a la base de conocimientos para ofrecer recomendaciones, explicaciones y, si está disponible, una imagen asociada con el profesional médico asignado.

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

3. **Aprendizaje dinámico**:

   - Permite actualizar la base de conocimientos mediante una ventana de aprendizaje, incorporando nuevos casos a la base de datos.

4. **Gestión de imágenes**:

   - Visualización de imágenes asociadas a doctores o recomendaciones dentro de la interfaz.

5. **Estilo personalizable**:
   - Utiliza un sistema modular de estilos para un diseño consistente y amigable.

---

## Componentes del Sistema

### 1. **Clase `InterfazMedica`**

- Encargada de gestionar la lógica y la estructura de la interfaz gráfica.
- Principales métodos:
  - `__init__`: Configura la ventana principal, inicializa variables y carga la base de conocimientos.
  - `crear_interfaz`: Diseña la GUI dividiéndola en un área de entrada (formulario) y un área de resultados.
  - `MotorInferencia`: Realiza consultas basadas en las entradas del usuario y devuelve recomendaciones.
  - `obtener_respuesta`: Recupera los datos ingresados, ejecuta el motor de inferencia y muestra los resultados.
  - `mostrar_explicacion`: Muestra una explicación detallada de la recomendación.
  - `mostrar_imagen`: Abre una ventana con la imagen asociada a la recomendación (si está disponible).
  - `abrir_ventana_aprender`: Permite al sistema aprender nuevos casos y actualizar la base de conocimientos.

---

### 2. **Base de Conocimientos**

- **Archivo**: `base_conocimientos.json`
- Contiene reglas codificadas en formato clave-valor, donde:

  - La clave es una tupla con las características del paciente (motivo, síntomas, historial médico, edad).
  - El valor es un diccionario con la recomendación, explicación y, opcionalmente, una imagen asociada.

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

- Métodos asociados:
  - `cargar_base_conocimientos`: Carga las reglas desde el archivo JSON.
  - `actualizar_base_conocimientos`: Recarga la base de conocimientos tras un aprendizaje exitoso.

---

### 3. **Interacción Dinámica**

- **Entrada de Datos**:
  - Preguntas sobre el motivo de consulta, nivel de síntomas, historial médico y edad, capturadas mediante listas desplegables.
- **Resultados**:
  - Se muestra una recomendación textual en un cuadro de texto.
  - Si aplica, el usuario puede ver una explicación detallada y una imagen asociada al médico o tratamiento sugerido.
- **Aprendizaje**:
  - Los casos desconocidos pueden ser almacenados en la base de conocimientos mediante la función `aprender_conocimiento` de un módulo externo.

---

## Componentes Externos Utilizados

1. **Bibliotecas externas**:

   - `tkinter`: Para la construcción de la interfaz gráfica.
   - `PIL (Pillow)`: Para gestionar imágenes.
   - `json`: Para la manipulación de la base de conocimientos.

2. **Módulos personalizados**:
   - `memoria`: Proporciona la funcionalidad para aprender nuevos conocimientos.
   - `custom_styles`: Define estilos y widgets personalizados como `CustomButton`, `CustomDropdown`, `CustomFrame` y `CustomLabel`.

---

## Flujo General del Programa

1. **Inicio**:

   - La ventana principal se inicializa con el método `iniciar`.
   - La base de conocimientos se carga desde el archivo JSON.

2. **Interacción del Usuario**:

   - El usuario responde preguntas a través de la interfaz.
   - Se genera una recomendación al hacer clic en "Obtener Asignación".

3. **Resultados**:

   - El sistema muestra la recomendación, una explicación (si aplica) y una imagen.

4. **Aprendizaje**:
   - Si no hay recomendaciones disponibles, el sistema permite aprender y actualizar la base de conocimientos.

---

## Ramas:

### Ejemplo Rama 1:

| *Pregunta*                                        | *Respuestas del usuario* | *Respuesta del Sistema Experto*                                                                                                                                                                                                                            |
| ------------------------------------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ¿Cuál es el motivo principal de la consulta?      | Control de salud         | RESPUESTA: Dra. Elena Rodríguez, Geriatra<br><br>EXPLICACION:<br>- Especialista en salud geriátrica, brindando seguimiento y control regular.<br>- Asesoría para mantener un estilo de vida saludable en la tercera edad.<br>- Costo por consulta: $1,000. |
| ¿Cómo calificaría la intensidad de sus síntomas?  | Moderado                 |                                                                                                                                                                                                                                                            |
| ¿Tiene antecedentes de alguna enfermedad crónica? | No                       |                                                                                                                                                                                                                                                            |
| ¿Cuál es la edad del paciente?                    | Más de 60 años           |                                                                                                                                                                                                                                                            |

### Ejemplo Rama 2:

| *Pregunta*                                        | *Respuestas del usuario* | *Respuesta del Sistema Experto*                                                                                                                                                                                                                                                                                                                                   |
| ------------------------------------------------- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ¿Cuál es el motivo principal de la consulta?      | Dolor                    | RESPUESTA: Dra. Sara Rodriguez Diaz, Medico General<br><br>EXPLICACION:<br>- Especialista en el manejo de dolores leves en adultos jovenes.<br>- Ofrece un enfoque integral para identificar la causa del dolor y tratarlo de manera efectiva.<br>- Brinda orientacion sobre habitos saludables y prevencion de futuras molestias.<br>- Costo por consulta: $500. |
| ¿Cómo calificaría la intensidad de sus síntomas?  | Leve                     |                                                                                                                                                                                                                                                                                                                                                                   |
| ¿Tiene antecedentes de alguna enfermedad crónica? | No                       |                                                                                                                                                                                                                                                                                                                                                                   |
| ¿Cuál es la edad del paciente?                    | Entre 18 y 35 años.      |                                                                                                                                                                                                                                                                                                                                                                   |
