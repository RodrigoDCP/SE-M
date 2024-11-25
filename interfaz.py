import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from memoria import aprender_conocimiento
from tkinter import filedialog
from custom_styles import Styles, CustomButton, CustomDropdown, CustomFrame, CustomLabel, setup_window_style


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
        #self.ventana.state('zoomed') 
        self.ventana.geometry("600x600")
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
        # Frame principal con padding
        frame_principal = tk.Frame(self.ventana, bg=Styles.COLORS['background'], padx=20, pady=20)
        frame_principal.pack(fill="both", expand=True)

        # Frame izquierdo (formulario)
        frame_izquierdo = CustomFrame(frame_principal)
        frame_izquierdo.pack(side="left", fill="y", padx=10)

        # Frame derecho (resultados)
        frame_derecho = CustomFrame(frame_principal)
        frame_derecho.pack(side="right", fill="both", expand=True, padx=10)

        # Título
        CustomLabel(
            frame_izquierdo,
            text="Información del Paciente",
            font=Styles.FONTS['subheading'],
            fg=Styles.COLORS['primary']
        ).pack(pady=(0, 20))

        # Campos del formulario
        CustomLabel(frame_izquierdo, text="¿Cuál es el motivo principal de la consulta?").pack(anchor="w", pady=5)
        self.opcion_motivo = tk.StringVar(value="Dolor")
        self.opcion_motivo.trace('w', self.limpiar_interfaz)
        CustomDropdown(frame_izquierdo, 
                      values=["Dolor", "Control de salud", "Revision de sintomas", "Consulta preventiva"],
                      textvariable=self.opcion_motivo).pack(fill="x", pady=5)

        CustomLabel(frame_izquierdo, text="¿Cómo calificaría la intensidad de sus síntomas?").pack(anchor="w", pady=5)
        self.opcion_sintomas = tk.StringVar(value="Leve")
        self.opcion_sintomas.trace('w', self.limpiar_interfaz)
        CustomDropdown(frame_izquierdo,
                      values=["Leve", "Moderado", "Fuerte", "Muy fuerte"],
                      textvariable=self.opcion_sintomas).pack(fill="x", pady=5)

        CustomLabel(frame_izquierdo, text="¿Tiene antecedentes de alguna enfermedad crónica?").pack(anchor="w", pady=5)
        self.opcion_historial = tk.StringVar(value="No")
        self.opcion_historial.trace('w', self.limpiar_interfaz)
        CustomDropdown(frame_izquierdo,
                      values=["Alergias a algun alimento", "Alergias a algun medicamento", 
                             "Operaciones o cirugias", "No"],
                      textvariable=self.opcion_historial).pack(fill="x", pady=5)

        CustomLabel(frame_izquierdo, text="¿Cuál es la edad del paciente?").pack(anchor="w", pady=5)
        self.opcion_edad = tk.StringVar(value="Entre 18-35 anios")
        self.opcion_edad.trace('w', self.limpiar_interfaz)
        CustomDropdown(frame_izquierdo,
                      values=["Menos de 18 anios", "Entre 18-35 anios", "Entre 36-60 anios", "Mas de 60 anios"],
                      textvariable=self.opcion_edad).pack(fill="x", pady=5)

        # Botón de consulta
        CustomButton(
            frame_izquierdo,
            text="Obtener Asignación",
            command=self.obtener_respuesta,
            width=250
        ).pack(pady=20)

        # Frame derecho
        CustomLabel(
            frame_derecho,
            text="Resultado del Sistema Experto",
            font=Styles.FONTS['subheading'],
            fg=Styles.COLORS['primary']
        ).pack(pady=(0, 20))

        # Frame para botones de acción
        frame_botones = tk.Frame(frame_derecho, bg=Styles.COLORS['surface'])
        frame_botones.pack(fill="x", pady=10)

        # Botones de acción
        self.boton_explicacion = CustomButton(
            frame_botones,
            text="Ver Explicación",
            command=self.mostrar_explicacion,
            width=180,
            color=Styles.COLORS['secondary']
        )
        self.boton_explicacion.pack(side="left", padx=5)
        
        self.boton_ver_doctor = CustomButton(
            frame_botones,
            text="Ver Doctor",
            command=self.mostrar_imagen,
            width=180,
            color=Styles.COLORS['secondary']
        )
        self.boton_ver_doctor.pack(side="left", padx=5)
        
        self.boton_aprender = CustomButton(
            frame_botones,
            text="Aprender Caso",
            command=self.abrir_ventana_aprender,
            width=180,
            color=Styles.COLORS['warning']
        )

        # Área de resultado
        self.resultado_texto = tk.Text(
            frame_derecho,
            height=10,
            wrap="word",
            font=Styles.FONTS['body'],
            bg=Styles.COLORS['surface'],
            fg=Styles.COLORS['text'],
            padx=10,
            pady=10
        )
        self.resultado_texto.pack(fill="both", expand=True, pady=10)

        # Label para imagen
        self.label_imagen = tk.Label(frame_derecho, bg=Styles.COLORS['surface'])
        self.label_imagen.pack(pady=10)

        # Variables para guardar datos
        self.explicacion_guardada = ""
        self.imagen_guardada = None

        # Deshabilitar botones inicialmente
        self.boton_explicacion.config(state="disabled")
        self.boton_ver_doctor.config(state="disabled")

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
            self.boton_aprender.pack(side="left", padx=5)
        else:
            self.boton_aprender.pack_forget()

        self.boton_explicacion.config(state="normal")
        self.boton_ver_doctor.config(state="normal")

    def mostrar_explicacion(self):
        if self.explicacion_guardada:
            self.resultado_texto.config(state="normal")
            self.resultado_texto.insert(tk.END, "\n\nEXPLICACION:\n" + self.explicacion_guardada)
            self.resultado_texto.config(state="disabled")
        self.boton_explicacion.config(state="disabled")

    def mostrar_imagen(self):
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
                
                centrar_ventana(ventana_imagen)
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")

    def abrir_ventana_aprender(self):
        def on_aprendizaje_completado():
            self.actualizar_base_conocimientos()
            messagebox.showinfo("Exito", "Base de conocimientos actualizada exitosamente")
            ventana_memoria.destroy()
            # Actualizar la interfaz con la nueva informacion
            self.obtener_respuesta()
        
        ventana_memoria = tk.Toplevel(self.ventana)
        aprender_conocimiento(ventana_memoria, self.hechos, on_aprendizaje_completado)
        centrar_ventana(ventana_memoria)

    def iniciar(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = InterfazMedica()
    app.iniciar()