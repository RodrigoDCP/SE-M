import json
import tkinter as tk
import tkinter as ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from memoria import aprender_conocimiento
from tkinter import filedialog

def centrar_ventana(ventana):
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = int((ancho_pantalla - ancho) / 2)
    y = int((alto_pantalla - alto) / 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
class InterfazMedica:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Sistema Experto - Asignacion de Doctor")
        self.ventana.geometry("600x700")
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
        centrar_ventana(self.ventana)  # Centramos la ventana después de crearla
        
    def cargar_base_conocimientos(self):
        try:
            with open('base_conocimientos.json', 'r') as archivo_json:
                datos_json = json.load(archivo_json)
                self.base_conocimientos = {}
                for clave, valor in datos_json.items():
                    clave_tupla = tuple(clave.strip("()").replace("'", "").split(", "))
                    self.base_conocimientos[clave_tupla] = valor
        except FileNotFoundError:
            print("No se encontro el archivo de base de conocimientos. Se usara una base vacia.")
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
            return "Lo siento, no tengo una recomendacion adecuada. Podrias considerar consultar con un medico general.", "", None

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
        
        # Ocultar boton de aprender si esta visible
        self.boton_aprender.pack_forget()
        
        # Limpiar variables guardadas
        self.explicacion_guardada = ""
        self.imagen_guardada = None

    def crear_interfaz(self):
        frame_principal = tk.Frame(self.ventana, bg="#2b2b2b", padx=20, pady=20)
        frame_principal.pack(fill="both", expand=True)

        frame_izquierdo = tk.Frame(frame_principal, bg="#1e1e1e")
        frame_izquierdo.pack(side="left", fill="y", padx=10)

        frame_derecho = tk.Frame(frame_principal, bg="#1e1e1e")
        frame_derecho.pack(side="right", fill="both", expand=True, padx=10)

        tk.Label(frame_izquierdo, text="¿Cual es el motivo principal de la consulta?", fg="white", bg="#1e1e1e").pack(anchor="w", pady=5)
        self.opcion_motivo = tk.StringVar(value="Dolor")
        self.opcion_motivo.trace('w', self.limpiar_interfaz)
        opciones_motivo = tk.OptionMenu(frame_izquierdo, self.opcion_motivo, "Dolor", "Control de salud", "Revision de sintomas", "Consulta preventiva")
        opciones_motivo.pack(fill="x", pady=5)

        tk.Label(frame_izquierdo, text="¿Como calificaria la intensidad de sus sintomas?", fg="white", bg="#1e1e1e").pack(anchor="w", pady=5)
        self.opcion_sintomas = tk.StringVar(value="Leve")
        self.opcion_sintomas.trace('w', self.limpiar_interfaz)
        opciones_sintomas = tk.OptionMenu(frame_izquierdo, self.opcion_sintomas, "Leve", "Moderado", "Fuerte", "Muy fuerte")
        opciones_sintomas.pack(fill="x", pady=5)

        tk.Label(frame_izquierdo, text="¿Tiene antecedentes de alguna enfermedad cronica?", fg="white", bg="#1e1e1e").pack(anchor="w", pady=5)
        self.opcion_historial = tk.StringVar(value="No")
        self.opcion_historial.trace('w', self.limpiar_interfaz)
        opciones_historial = tk.OptionMenu(frame_izquierdo, self.opcion_historial, "Alergias a algun alimento", "Alergias a algun medicamento", "Operaciones o cirugias", "No")
        opciones_historial.pack(fill="x", pady=5)

        tk.Label(frame_izquierdo, text="¿Cual es la edad del paciente?", fg="white", bg="#1e1e1e").pack(anchor="w", pady=5)
        self.opcion_edad = tk.StringVar(value="Entre 18-35 anios")
        self.opcion_edad.trace('w', self.limpiar_interfaz)
        opciones_edad = tk.OptionMenu(frame_izquierdo, self.opcion_edad, "Menos de 18 anios", "Entre 18-35 anios", "Entre 36-60 anios", "Mas de 60 anios")
        opciones_edad.pack(fill="x", pady=5)

        self.boton_responder = tk.Button(frame_izquierdo, text="Obtener Asignacion de Doctor", command=self.obtener_respuesta, bg="#005f73", fg="white", font=("Arial", 10, "bold"))
        self.boton_responder.pack(fill="x", pady=10)

        #self.resultado_texto = tk.Text(frame_derecho, height=10, state="disabled", wrap="word", bg="#2b2b2b", fg="white")
        #self.resultado_texto.pack(fill="both", pady=5)

        self.boton_aprender = tk.Button(frame_derecho, text="Aprender", command=self.abrir_ventana_aprender, bg="#e9d8a6", fg="black", font=("Arial", 10, "bold"))
        self.boton_aprender.pack_forget()

        self.boton_explicacion = tk.Button(frame_derecho, text="Mostrar Explicación", command=self.mostrar_explicacion, bg="#2a9d8f", fg="white", font=("Arial", 10, "bold"))
        self.boton_explicacion.pack(pady=10)

        self.boton_ver_doctor = tk.Button(frame_derecho, text="Ver Imagen Doctor", command=self.mostrar_imagen, bg="#264653", fg="white", font=("Arial", 10, "bold"))
        self.boton_ver_doctor.pack(pady=10)

        tk.Label(frame_derecho, text="Resultado del Sistema Experto:", fg="white", bg="#1e1e1e").pack(anchor="w", pady=5)
        self.resultado_texto = tk.Text(frame_derecho, height=10, state="disabled", wrap="word", bg="#2b2b2b", fg="white")
        self.resultado_texto.pack(fill="both", pady=5)


        self.label_imagen = tk.Label(frame_derecho)
        self.label_imagen.pack(pady=10)

        # Aquí van las variables para guardar la explicación y la imagen
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

        # Mostrar u ocultar boton de aprender segun la recomendacion
        if "Lo siento, no tengo una recomendacion adecuada" in recomendacion:
            self.boton_aprender.pack(pady=10)
        else:
            self.boton_aprender.pack_forget()

        self.boton_explicacion.config(state="normal")
        self.boton_ver_doctor.config(state="normal")

    def abrir_ventana_aprender(self):
        def on_aprendizaje_completado():
            self.actualizar_base_conocimientos()
            messagebox.showinfo("exito", "Base de conocimientos actualizada exitosamente")
            ventana_memoria.destroy()
            # Actualizar la interfaz con la nueva informacion
            self.obtener_respuesta()
        
        ventana_memoria = tk.Toplevel(self.ventana)
        aprender_conocimiento(ventana_memoria, self.hechos, on_aprendizaje_completado)
        centrar_ventana(ventana_memoria) #Centramos la ventana

    def mostrar_explicacion(self):
        if self.explicacion_guardada:
            self.resultado_texto.config(state="normal")
            self.resultado_texto.insert(tk.END, "\n\nEXPLICACION:\n" + self.explicacion_guardada)
            self.resultado_texto.config(state="disabled")
        self.boton_explicacion.config(state="disabled")

    def mostrar_imagen(self, event=None):
        if self.imagen_guardada:
            try:
                # Crear nueva ventana
                ventana_imagen = tk.Toplevel(self.ventana)
                ventana_imagen.title("Imagen del Doctor")
                
                # Cargar y mostrar la imagen
                imagen = Image.open(self.imagen_guardada)
                imagen = imagen.resize((300, 300))
                imagen_tk = ImageTk.PhotoImage(imagen)
                label_imagen = tk.Label(ventana_imagen, image=imagen_tk)
                label_imagen.image = imagen_tk
                label_imagen.pack(padx=20, pady=20)
                
                # Centrar la ventana después de crear todo su contenido
                centrar_ventana(ventana_imagen)  # Agregar esta línea
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")

    def iniciar(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = InterfazMedica()
    app.iniciar()