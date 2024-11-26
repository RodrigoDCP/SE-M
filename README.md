# SISMED - Sistema Experto Médico
---
**Equipo 3: Rodrigo Cañas, Jorge Sarricolea, Daniel Toache, Melisa Vazquez**

## Descripción

SISMED es una herramienta sencilla que asigna médicos a pacientes de forma rápida y fácil. Funciona como un **sistema experto** que hace una serie de preguntas al paciente sobre su motivo de consulta, síntomas, historial médico y edad. Con base en las respuestas, *el sistema recomienda al médico más adecuado según las características del caso*.

| *Criterio*            | *Pregunta*                                        | *Resp 1*                  | *Resp 2*                     | *Resp 3*               | *Resp 4*            |
| --------------------- | ------------------------------------------------- | ------------------------- | ---------------------------- | ---------------------- | ------------------- |
| 1. Motivo de consulta | ¿Cuál es el motivo principal de la consulta?      | Dolor                     | Control de salud             | Revisión de síntomas   | Consulta preventiva |
| 2. Nivel de síntomas  | ¿Cómo calificaría la intensidad de sus síntomas?  | Leve                      | Moderado                     | Fuerte                 | Muy fuerte          |
| 3. Historial médico   | ¿Tiene antecedentes de alguna enfermedad crónica? | Alergias a algún alimento | Alergias a algún medicamento | Operaciones o cirugías | No                  |
| 4. Edad               | ¿Cuál es la edad del paciente?                    | Menos de 18 años          | Entre 18-35 años             | Entre 36-60 años       | Más de 60 años      |

## Estructura de Archivos

El sistema está organizado en los siguientes archivos:

### 1. `main.py`
- Punto de entrada de la aplicación
- Inicializa la ventana de bienvenida

### 2. `bienvenida.py`
- Muestra la ventana inicial
- Presenta información introductoria
- Permite iniciar la consulta

### 3. `base_hechos.py`
- Define la clase BaseHechos
- Almacena y gestiona los datos del paciente actual
- Proporciona métodos para acceder y actualizar hechos

### 4. `base_conocimientos.py`
- Define la clase BaseConocimientos
- Maneja el almacenamiento persistente en JSON
- Métodos para cargar y guardar conocimientos
- Gestiona la búsqueda de recomendaciones

### 5. `motor_inferencia.py`
- Define la clase MotorInferencia
- Coordina la interacción entre componentes
- Realiza el proceso de inferencia
- Gestiona recomendaciones y explicaciones

### 6. `interfaz_medica.py`
- Implementa la interfaz gráfica principal
- Maneja la interacción con el usuario
- Muestra resultados y explicaciones
- Gestiona la adquisición de nuevo conocimiento

### 7. `custom_styles.py`
- Define estilos personalizados
- Proporciona widgets customizados
- Mantiene consistencia visual

## Formato de la Base de Conocimientos (`base_conocimientos.json`)
```json
{
    "('Dolor', 'Muy Fuerte', 'Operaciones o cirugias', 'Entre 36-60 anios')": {
        "recomendacion": "Dra.Elvia Zapata Alvarado, Algologo",
        "explicacion": [
            "Te recomiento este doctor ya que es:",
            "-Adecuado para pacientes con dolor con antecedentes quirurgicos.",
            "-Recomendado si el dolor es persistente a inflamacion postquirurgica.",
            " Costo por consulta: $450"
        ],
        "imagen": "path/to/image.jpeg"
    }
}
```

## Funcionalidades Principales

### 1. Interfaz Intuitiva
- Formularios con desplegables
- Botones de acción claros
- Área de resultados
- Visualización de imágenes
- Ventana de aprendizaje

### 2. Motor de Inferencia
- Procesa hechos del paciente
- Busca coincidencias en la base
- Genera recomendaciones
- Proporciona explicaciones

### 3. Gestión de Conocimiento
- Carga/guarda conocimientos
- Permite agregar nuevos casos
- Mantiene persistencia de datos

### 4. Sistema de Explicaciones
- Muestra recomendación inicial
- Proporciona explicación detallada
- Permite ver imagen del doctor

## Ejemplos de Ramas

### Rama 1: Atención General
| *Pregunta*                                        | *Respuestas del usuario* | *Respuesta del Sistema Experto*                                                                                                                                                                                                                                   |
| ------------------------------------------------- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ¿Cuál es el motivo principal de la consulta?      | Dolor                    | RESPUESTA: Se recomienda al Dr. Rodriguez, Médico General<br><br>EXPLICACIÓN:<br>- Experto en tratar una amplia gama de problemas de salud.<br>- Consultas disponibles en horario vespertino.<br>- Ideal para pacientes sin condiciones alérgicas que requieren atención rapida.<br>- Costo por consulta: $900. |
| ¿Cómo calificaría la intensidad de sus síntomas?  | Moderado                 |                                                                                                                                                                                                                                                                   |
| ¿Tiene antecedentes de alguna enfermedad crónica? | No                       |                                                                                                                                                                                                                                                                   |
| ¿Cuál es la edad del paciente?                    | Entre 18-35 años         |                                                                                                                                                                                                                                                                   |

### Rama 2: Urgencias Pediátricas
| *Pregunta*                                        | *Respuestas del usuario* | *Respuesta del Sistema Experto*                                                                                                                                                                                                                                              |
| ------------------------------------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ¿Cuál es el motivo principal de la consulta?      | Dolor                    | RESPUESTA: Dr. Mariana López, Urgencias Pediátricas<br><br>EXPLICACIÓN:<br>- Especialista en urgencias pediátricas.<br>- Proporciona diagnósticos precisos y tratamientos seguros para menores.<br>- Experiencia en enfoques no invasivos para minimizar el dolor.<br>- Costo por consulta urgente: $1200. |
| ¿Cómo calificaría la intensidad de sus síntomas?  | Fuerte                   |                                                                                                                                                                                                                                                                              |
| ¿Tiene antecedentes de alguna enfermedad crónica? | No                       |                                                                                                                                                                                                                                                                              |
| ¿Cuál es la edad del paciente?                    | Menos de 18              |                                                                                                                                                                                                                                                                              |

## Requerimientos e Instalación

### Requerimientos
- Python 3.x
- Tkinter (incluido en Python)
- Pillow (PIL): `pip install Pillow`

### Instalación
1. Clonar o descargar el repositorio
2. Instalar dependencias: `pip install Pillow`
3. Ejecutar: `python main.py`

## Consideraciones Técnicas
- La base de conocimientos se almacena en formato JSON
- Las imágenes de los doctores deben estar en formatos comunes (jpg, png, gif)
- Todas las ventanas se centran automáticamente

## Estructura del Proyecto
```
sistema_experto/
├── main.py
├── bienvenida.py
├── interfaz_medica.py
├── motor_inferencia.py
├── base_hechos.py
├── base_conocimientos.py
├── custom_styles.py
├── base_conocimientos.json
└── images/
    └── doctores/
```