import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from memoria import aprender_conocimiento
from tkinter import filedialog

class InterfazMedica:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Sistema Experto - Asignación de Doctor")
        self.ventana.geometry("600x700")
        
        # Base de Hechos como atributo de clase
        self.hechos = {
            "motivo_consulta": "",
            "nivel_sintomas": "",
            "historial_medico": "",
            "edad": ""
        }
        
        # Base de Conocimientos como atributo de clase
        self.base_conocimientos = {}
        self.cargar_base_conocimientos()
        
        self.crear_interfaz()
        
    def cargar_base_conocimientos(self):
        try:
            with open('base_conocimientos.json', 'r') as archivo_json:
                datos_json = json.load(archivo_json)
                self.base_conocimientos = {}
                for clave, valor in datos_json.items():
                    clave_tupla = tuple(clave.strip("()").replace("'", "").split(", "))
                    self.base_conocimientos[clave_tupla] = valor
        except FileNotFoundError:
            print("No se encontró el archivo de base de conocimientos. Se usará una base vacía.")
        except json.JSONDecodeError:
            print("Hubo un error al leer el archivo de base de conocimientos.")

    def motor_inferencia(self):
        clave = tuple(self.hechos.values())
        if clave in self.base_conocimientos:
            recomendacion = self.base_conocimientos[clave]["recomendacion"]
            explicacion = "\n".join(self.base_conocimientos[clave]["explicacion"])
            imagen_path = self.base_conocimientos[clave]["imagen"]
            return recomendacion, explicacion, imagen_path
        else:
            return "Lo siento, no tengo una recomendación adecuada. Podrías considerar consultar con un médico general.", "", None

    def actualizar_base_conocimientos(self):
        self.cargar_base_conocimientos()

    def limpiar_interfaz(self, *args):
        # Limpiar el texto del resultado
        self.resultado_texto.config(state="normal")
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.config(state="disabled")
        
        # Limpiar la imagen
        self.label_imagen.config(image="")
        
        # Restablecer estados de botones
        self.boton_explicacion.config(state="disabled")
        self.boton_ver_doctor.config(state="disabled")
        
        # Ocultar botón de aprender si está visible
        self.boton_aprender.pack_forget()
        
        # Limpiar variables guardadas
        self.explicacion_guardada = ""
        self.imagen_guardada = None

    def crear_interfaz(self):
        tk.Label(self.ventana, text="¿Cuál es el motivo principal de la consulta?").pack()
        self.opcion_motivo = tk.StringVar(value="Dolor")
        self.opcion_motivo.trace('w', self.limpiar_interfaz)
        tk.OptionMenu(self.ventana, self.opcion_motivo, "Dolor", "Control de salud", "Revisión de síntomas", "Consulta preventiva").pack()

        tk.Label(self.ventana, text="¿Cómo calificaría la intensidad de sus síntomas?").pack()
        self.opcion_sintomas = tk.StringVar(value="Leve")
        self.opcion_sintomas.trace('w', self.limpiar_interfaz)
        tk.OptionMenu(self.ventana, self.opcion_sintomas, "Leve", "Moderado", "Fuerte", "Muy fuerte").pack()

        tk.Label(self.ventana, text="¿Tiene antecedentes de alguna enfermedad crónica?").pack()
        self.opcion_historial = tk.StringVar(value="No")
        self.opcion_historial.trace('w', self.limpiar_interfaz)
        tk.OptionMenu(self.ventana, self.opcion_historial, "Alergias a algún alimento", "Alergias a algún medicamento", "Operaciones o cirugías", "No").pack()

        tk.Label(self.ventana, text="¿Cuál es la edad del paciente?").pack()
        self.opcion_edad = tk.StringVar(value="Entre 18-35 años")
        self.opcion_edad.trace('w', self.limpiar_interfaz)
        tk.OptionMenu(self.ventana, self.opcion_edad, "Menos de 18 años", "Entre 18-35 años", "Entre 36-60 años", "Más de 60 años").pack()

        # El botón de aprender inicialmente está oculto
        self.boton_aprender = tk.Button(self.ventana, text="Aprender", command=self.abrir_ventana_aprender)
        # No lo empaquetamos aquí, lo haremos solo cuando sea necesario

        self.boton_responder = tk.Button(self.ventana, text="Obtener Asignación de Doctor", command=self.obtener_respuesta)
        self.boton_responder.pack(pady=10)

        self.boton_explicacion = tk.Button(self.ventana, text="Mostrar explicación", state="disabled", command=self.mostrar_explicacion)
        self.boton_explicacion.pack(pady=10)

        self.boton_ver_doctor = tk.Button(self.ventana, text="Ver Doctor", state="disabled", command=self.mostrar_imagen)
        self.boton_ver_doctor.pack(pady=10)

        tk.Label(self.ventana, text="Resultado del Sistema Experto:").pack()
        self.resultado_texto = tk.Text(self.ventana, height=10, width=70, state="disabled", wrap="word")
        self.resultado_texto.pack()

        self.label_imagen = tk.Label(self.ventana)
        self.label_imagen.pack(pady=10)

        self.explicacion_guardada = ""
        self.imagen_guardada = None

    def obtener_respuesta(self):
        self.hechos["motivo_consulta"] = self.opcion_motivo.get()
        self.hechos["nivel_sintomas"] = self.opcion_sintomas.get()
        self.hechos["historial_medico"] = self.opcion_historial.get()
        self.hechos["edad"] = self.opcion_edad.get()

        recomendacion, explicacion, imagen_path = self.motor_inferencia()
        self.resultado_texto.config(state="normal")
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.insert(tk.END, recomendacion)
        self.resultado_texto.config(state="disabled")

        self.explicacion_guardada = explicacion
        self.imagen_guardada = imagen_path

        # Mostrar u ocultar botón de aprender según la recomendación
        if "Lo siento, no tengo una recomendación adecuada" in recomendacion:
            self.boton_aprender.pack(pady=10)
        else:
            self.boton_aprender.pack_forget()

        self.boton_explicacion.config(state="normal")
        self.boton_ver_doctor.config(state="normal")

    def abrir_ventana_aprender(self):
        def on_aprendizaje_completado():
            self.actualizar_base_conocimientos()
            messagebox.showinfo("Éxito", "Base de conocimientos actualizada exitosamente")
            ventana_memoria.destroy()
            # Actualizar la interfaz con la nueva información
            self.obtener_respuesta()
        
        ventana_memoria = tk.Toplevel(self.ventana)
        aprender_conocimiento(ventana_memoria, self.hechos, on_aprendizaje_completado)

    def mostrar_explicacion(self):
        if self.explicacion_guardada:
            self.resultado_texto.config(state="normal")
            self.resultado_texto.insert(tk.END, "\n\nEXPLICACIÓN:\n" + self.explicacion_guardada)
            self.resultado_texto.config(state="disabled")
        self.boton_explicacion.config(state="disabled")

    def mostrar_imagen(self):
        if self.imagen_guardada:
            imagen = Image.open(self.imagen_guardada)
            imagen = imagen.resize((150, 150), Image.LANCZOS)
            imagen_tk = ImageTk.PhotoImage(imagen)
            self.label_imagen.config(image=imagen_tk)
            self.label_imagen.image = imagen_tk

    def iniciar(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = InterfazMedica()
    app.iniciar()