import os
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from memoria import aprender_conocimiento
from tkinter import filedialog
from custom_styles import Styles, CustomButton, CustomDropdown, CustomFrame, CustomLabel, setup_window_style
from motor import MotorInferencia

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
        
        # Agregar control de última modificación
        self.last_modified = os.path.getmtime('base_conocimientos.json') if os.path.exists('base_conocimientos.json') else 0
        
        self.crear_interfaz()
        centrar_ventana(self.ventana)
        
        # Iniciar verificación periódica
        self.verificar_cambios()

    def verificar_cambios(self):
        """Verifica cambios en el archivo cada 2 segundos"""
        try:
            current_modified = os.path.getmtime('base_conocimientos.json')
            if current_modified > self.last_modified:
                self.last_modified = current_modified
                # Solo actualizar si hay una consulta activa
                if all([
                    self.opcion_motivo.get(),
                    self.opcion_sintomas.get(),
                    self.opcion_historial.get(),
                    self.opcion_edad.get()
                ]):
                    self.obtener_respuesta()
        except FileNotFoundError:
            pass
        
        # Programar la siguiente verificación
        self.ventana.after(2000, self.verificar_cambios)

    def limpiar_interfaz(self, *args):
        if hasattr(self, 'resultado_texto'):
            self.resultado_texto.config(state="normal")
            self.resultado_texto.delete(1.0, tk.END)
            self.resultado_texto.config(state="disabled")
            
            self.frame_botones.pack_forget()
            self.boton_aprender.pack_forget()
            self.boton_explicacion.pack_forget()
            self.boton_ver_doctor.pack_forget()
            
            self.explicacion_guardada = ""
            self.imagen_guardada = None

    def crear_interfaz(self):
        frame_principal = tk.Frame(self.ventana, bg=Styles.COLORS['background'], padx=20, pady=20)
        frame_principal.pack(fill="both", expand=True)

        frame_izquierdo = CustomFrame(frame_principal)
        frame_izquierdo.pack(side="left", fill="y", padx=10)

        frame_derecho = CustomFrame(frame_principal)
        frame_derecho.pack(side="right", fill="both", expand=True, padx=10)

        CustomLabel(
            frame_izquierdo,
            text="Información del Paciente",
            font=Styles.FONTS['subheading'],
            fg=Styles.COLORS['primary']
        ).pack(pady=(0, 20))

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

        CustomButton(
            frame_izquierdo,
            text="Obtener Asignación",
            command=self.obtener_respuesta,
            width=250
        ).pack(pady=20)

        CustomLabel(
            frame_derecho,
            text="Resultado del Sistema Experto",
            font=Styles.FONTS['subheading'],
            fg=Styles.COLORS['primary']
        ).pack(pady=(0, 20))

        self.frame_botones = tk.Frame(frame_derecho, bg=Styles.COLORS['surface'])
        
        self.boton_explicacion = CustomButton(
            self.frame_botones,
            text="Ver Explicación",
            command=self.mostrar_explicacion,
            width=180,
            color=Styles.COLORS['secondary']
        )
        
        self.boton_ver_doctor = CustomButton(
            self.frame_botones,
            text="Ver Doctor",
            command=self.mostrar_imagen,
            width=180,
            color=Styles.COLORS['secondary']
        )
        
        self.boton_aprender = CustomButton(
            self.frame_botones,
            text="Aprender Caso",
            command=self.abrir_ventana_aprender,
            width=180,
            color=Styles.COLORS['warning']
        )

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

        self.label_imagen = tk.Label(frame_derecho, bg=Styles.COLORS['surface'])
        self.label_imagen.pack(pady=10)

        self.explicacion_guardada = ""
        self.imagen_guardada = None

    def obtener_respuesta(self):
        self.hechos["motivo_consulta"] = self.opcion_motivo.get()
        self.hechos["nivel_sintomas"] = self.opcion_sintomas.get()
        self.hechos["historial_medico"] = self.opcion_historial.get()
        self.hechos["edad"] = self.opcion_edad.get()

        recomendacion, explicacion, imagen_path = MotorInferencia.obtener_recomendacion(self.hechos)
        
        self.resultado_texto.config(state="normal")
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.insert(tk.END, recomendacion)
        self.resultado_texto.config(state="disabled")

        self.explicacion_guardada = explicacion
        self.imagen_guardada = imagen_path

        if "Lo siento, no tengo una recomendacion adecuada" not in recomendacion:
            self.frame_botones.pack(fill="x", pady=10)
            self.boton_explicacion.pack(side="left", padx=5)
            self.boton_ver_doctor.pack(side="left", padx=5)
            self.boton_aprender.pack_forget()
        else:
            self.frame_botones.pack(fill="x", pady=10)
            self.boton_aprender.pack(side="left", padx=5)
            self.boton_explicacion.pack_forget()
            self.boton_ver_doctor.pack_forget()

    def mostrar_explicacion(self):
        if self.explicacion_guardada:
            self.resultado_texto.config(state="normal")
            self.resultado_texto.insert(tk.END, "\n\nEXPLICACION:\n" + self.explicacion_guardada)
            self.resultado_texto.config(state="disabled")
        self.boton_explicacion.pack_forget()

    def mostrar_imagen(self):
        if self.imagen_guardada:
            try:
                ventana_imagen = tk.Toplevel(self.ventana)
                ventana_imagen.title("Imagen del Doctor")
                
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
            self.last_modified = os.path.getmtime('base_conocimientos.json')  # Actualizar timestamp
            messagebox.showinfo("Exito", "Base de conocimientos actualizada exitosamente")
            ventana_memoria.destroy()
            self.obtener_respuesta()
        
        ventana_memoria = tk.Toplevel(self.ventana)
        aprender_conocimiento(ventana_memoria, self.hechos, on_aprendizaje_completado)
        centrar_ventana(ventana_memoria)

    def iniciar(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = InterfazMedica()
    app.iniciar()