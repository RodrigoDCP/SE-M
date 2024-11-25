# Documentación: `interfaz.py`
---

## Descripción

SISMED es una herramienta sencilla que asigna médicos a pacientes de forma rápida y fácil. Funciona como un **bot** que hace una serie de preguntas al paciente sobre su motivo de consulta, síntomas, historial médico y cuándo está disponible. Con base en las respuestas, *el sistema busca al médico más adecuado según la especialidad y el horario disponible*.

## Funcionalidades Principales

1. **Interfaz gráfica intuitiva**:

   - Captura información del paciente mediante formularios interactivos con listas desplegables y campos seleccionables.
   - Visualización de resultados, explicaciones y recomendaciones dentro de la misma interfaz.

2. **Motor de inferencia**:

   - Realiza consultas a la base de conocimientos para ofrecer recomendaciones, explicaciones y, si está disponible, una imagen asociada con el profesional médico asignado.

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
  - `motor_inferencia`: Realiza consultas basadas en las entradas del usuario y devuelve recomendaciones.
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

## Notas

1. Asegúrese de que el archivo `base_conocimientos.json` exista en el mismo directorio para evitar errores al cargar la base de conocimientos.
2. Si desea personalizar estilos, edite el módulo `custom_styles`.
3. El sistema admite ampliaciones para incorporar nuevas características, como más preguntas o mejoras en el motor de inferencia.
