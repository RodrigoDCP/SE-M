import os
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from PIL import Image, ImageTk
from custom_styles import (
    Styles, 
    CustomButton, 
    CustomDropdown, 
    CustomFrame, 
    CustomLabel, 
    setup_window_style
)
from motor_inferencia import MotorInferencia

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
    """
    Clase que maneja la interfaz gráfica usando el motor de inferencia
    """
    def __init__(self):
        self.ventana = tk.Tk()
        self.motor = MotorInferencia()
        self.ventana.title("Sistema Experto - Asignación de Doctor")
        self.ventana.geometry("600x600")
        
        # Inicializar timestamp
        self.last_modified = os.path.getmtime('base_conocimientos.json') if os.path.exists('base_conocimientos.json') else 0
        
        # Inicializar otras variables
        self.explicacion_guardada = ""
        self.imagen_guardada = None
        
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
                    # Guardar el estado actual del scroll
                    estado_scroll = None
                    if hasattr(self, 'resultado_texto'):
                        estado_scroll = self.resultado_texto.yview()
                    
                    # Actualizar la respuesta
                    self.obtener_respuesta()
                    
                    # Restaurar la posición del scroll
                    if estado_scroll:
                        self.resultado_texto.yview_moveto(estado_scroll[0])
                        
        except FileNotFoundError:
            pass
        finally:
            # Programar la siguiente verificación incluso si hay error
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

        # Título Información del Paciente
        CustomLabel(
            frame_izquierdo,
            text="Información del Paciente",
            font=Styles.FONTS['subheading'],
            fg=Styles.COLORS['primary']
        ).pack(pady=(0, 20))

        # Motivo de consulta
        CustomLabel(frame_izquierdo, text="¿Cuál es el motivo principal de la consulta?").pack(anchor="w", pady=5)
        self.opcion_motivo = tk.StringVar(value="Dolor")
        self.opcion_motivo.trace('w', self.limpiar_interfaz)
        CustomDropdown(frame_izquierdo, 
                      values=["Dolor", "Control de salud", "Revision de sintomas", "Consulta preventiva"],
                      textvariable=self.opcion_motivo).pack(fill="x", pady=5)

        # Nivel de síntomas
        CustomLabel(frame_izquierdo, text="¿Cómo calificaría la intensidad de sus síntomas?").pack(anchor="w", pady=5)
        self.opcion_sintomas = tk.StringVar(value="Leve")
        self.opcion_sintomas.trace('w', self.limpiar_interfaz)
        CustomDropdown(frame_izquierdo,
                      values=["Leve", "Moderado", "Fuerte", "Muy fuerte"],
                      textvariable=self.opcion_sintomas).pack(fill="x", pady=5)

        # Historial médico
        CustomLabel(frame_izquierdo, text="¿Tiene antecedentes de alguna enfermedad crónica?").pack(anchor="w", pady=5)
        self.opcion_historial = tk.StringVar(value="No")
        self.opcion_historial.trace('w', self.limpiar_interfaz)
        CustomDropdown(frame_izquierdo,
                      values=["Alergias a algun alimento", "Alergias a algun medicamento", 
                             "Operaciones o cirugias", "No"],
                      textvariable=self.opcion_historial).pack(fill="x", pady=5)

        # Edad del paciente
        CustomLabel(frame_izquierdo, text="¿Cuál es la edad del paciente?").pack(anchor="w", pady=5)
        self.opcion_edad = tk.StringVar(value="Entre 18-35 anios")
        self.opcion_edad.trace('w', self.limpiar_interfaz)
        CustomDropdown(frame_izquierdo,
                      values=["Menos de 18 anios", "Entre 18-35 anios", "Entre 36-60 anios", "Mas de 60 anios"],
                      textvariable=self.opcion_edad).pack(fill="x", pady=5)

        # Botón obtener asignación
        CustomButton(
            frame_izquierdo,
            text="Obtener Asignación",
            command=self.obtener_respuesta,
            width=250
        ).pack(pady=20)

        # Título Resultado
        CustomLabel(
            frame_derecho,
            text="Resultado del Sistema Experto",
            font=Styles.FONTS['subheading'],
            fg=Styles.COLORS['primary']
        ).pack(pady=(0, 20))

        # Frame para botones
        self.frame_botones = tk.Frame(frame_derecho, bg=Styles.COLORS['surface'])
        
        # Botones de acción
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

        # Área de texto para resultados
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

    def obtener_respuesta(self):
            """Obtiene y muestra la recomendación inicial"""
            hechos = {
                "motivo_consulta": self.opcion_motivo.get(),
                "nivel_sintomas": self.opcion_sintomas.get(),
                "historial_medico": self.opcion_historial.get(),
                "edad": self.opcion_edad.get()
            }
            
            if self.motor.inferir(hechos):
                recomendacion = self.motor.obtener_recomendacion()  # Solo obtener la recomendación inicial
                self.mostrar_resultado(recomendacion)
                self.habilitar_botones_explicacion()
            else:
                self.mostrar_resultado("Lo siento, no tengo una recomendación adecuada.")
                self.habilitar_boton_aprender()
    def mostrar_resultado(self, texto):
        """Muestra el resultado en el área de texto"""
        self.resultado_texto.config(state="normal")
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.insert(tk.END, texto)
        self.resultado_texto.config(state="disabled")

    def habilitar_botones_explicacion(self):
        """Habilita los botones de explicación y ver doctor"""
        self.frame_botones.pack(fill="x", pady=10)
        self.boton_explicacion.pack(side="left", padx=5)
        self.boton_ver_doctor.pack(side="left", padx=5)
        self.boton_aprender.pack_forget()

    def habilitar_boton_aprender(self):
        """Habilita solo el botón de aprender"""
        self.frame_botones.pack(fill="x", pady=10)
        self.boton_aprender.pack(side="left", padx=5)
        self.boton_explicacion.pack_forget()
        self.boton_ver_doctor.pack_forget()

    def mostrar_explicacion(self):
        """Muestra la explicación detallada cuando se presiona el botón"""
        if hasattr(self, 'motor'):
            recomendacion = self.motor.obtener_recomendacion()
            explicacion_completa = self.motor.obtener_explicacion()
            texto_completo = f"{recomendacion}\n\nEXPLICACION:\n{explicacion_completa}"
            self.mostrar_resultado(texto_completo)
            self.boton_explicacion.pack_forget()
    def mostrar_imagen(self):
        """Muestra la imagen del doctor en una nueva ventana"""
        if hasattr(self, 'motor'):
            ruta_imagen = self.motor.obtener_imagen()
            if ruta_imagen:
                try:
                    ventana_imagen = tk.Toplevel(self.ventana)
                    ventana_imagen.title("Imagen del Doctor")
                    
                    imagen = Image.open(ruta_imagen)
                    imagen = imagen.resize((300, 300))
                    imagen_tk = ImageTk.PhotoImage(imagen)
                    label_imagen = tk.Label(ventana_imagen, image=imagen_tk)
                    label_imagen.image = imagen_tk
                    label_imagen.pack(padx=20, pady=20)
                    
                    centrar_ventana(ventana_imagen)
                    
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")

    def abrir_ventana_aprender(self):
        def cargar_imagen():
            ventana_memoria.grab_release()
            ruta_imagen = filedialog.askopenfilename(
                title="Selecciona una imagen",
                filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.gif")]
            )
            ventana_memoria.grab_set()
            if ruta_imagen:
                campo_imagen.delete(0, tk.END)
                campo_imagen.insert(0, ruta_imagen)

        def guardar_nuevo_conocimiento():
            doctor = campo_doctor.get()
            explicacion = campo_explicacion.get("1.0", tk.END).strip()
            imagen = campo_imagen.get()

            if self.motor.agregar_conocimiento(doctor, explicacion, imagen):
                messagebox.showinfo("Éxito", "Nuevo conocimiento guardado exitosamente!")
                self.ultima_actualizacion = self.motor.ultima_actualizacion()
                ventana_memoria.destroy()
                self.obtener_respuesta()
            else:
                messagebox.showerror("Error", "Por favor complete todos los campos")

        # Configuración de la ventana
        ventana_memoria = tk.Toplevel(self.ventana)
        ventana_memoria.title("Agregar Nuevo Conocimiento")
        ventana_memoria.geometry("600x600")
        
        # Hacer la ventana modal
        ventana_memoria.transient(self.ventana)
        ventana_memoria.grab_set()
        ventana_memoria.focus_set()
        
        setup_window_style(ventana_memoria)

        # Frame principal
        main_frame = CustomFrame(ventana_memoria)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Título principal
        titulo = CustomLabel(
            main_frame,
            text="Agregar Nuevo Conocimiento",
            font=Styles.FONTS['subheading'],
            fg=Styles.COLORS['primary']
        )
        titulo.pack(pady=(0, 20))

        # Contenedor para las dos columnas
        columns_frame = tk.Frame(main_frame, bg=Styles.COLORS['surface'])
        columns_frame.pack(fill='both', expand=True)

        # Columna izquierda (Datos del caso)
        left_frame = CustomFrame(columns_frame)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

        # Título datos del caso
        CustomLabel(
            left_frame,
            text="Datos del Caso",
            font=Styles.FONTS['body_bold'],
            fg=Styles.COLORS['primary']
        ).pack(pady=(0, 10))

        # Mostrar los hechos actuales
        hechos_actuales = self.motor.base_hechos.obtener_hechos()
        for key, value in hechos_actuales.items():
            case_frame = tk.Frame(left_frame, bg=Styles.COLORS['surface'])
            case_frame.pack(fill='x', pady=5)
            
            CustomLabel(
                case_frame,
                text=f"{key.replace('_', ' ').title()}:",
                font=Styles.FONTS['body_bold'],
                fg=Styles.COLORS['secondary'],
                width=15,
                anchor='e'
            ).pack(side='left', padx=(5, 10))
            
            CustomLabel(
                case_frame,
                text=value,
                anchor='w'
            ).pack(side='left')

        # Columna derecha (Formulario)
        right_frame = CustomFrame(columns_frame)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))

        # Campo doctor
        CustomLabel(
            right_frame,
            text="Nombre del doctor:",
            font=Styles.FONTS['body_bold'],
            fg=Styles.COLORS['secondary']
        ).pack(anchor='w', pady=(0, 5))
        
        campo_doctor = tk.Entry(
            right_frame,
            font=Styles.FONTS['body'],
            bg='white'
        )
        campo_doctor.pack(fill='x', pady=(0, 10))

        # Campo explicación
        CustomLabel(
            right_frame,
            text="Explicación del conocimiento:",
            font=Styles.FONTS['body_bold'],
            fg=Styles.COLORS['secondary']
        ).pack(anchor='w', pady=(0, 5))
        
        campo_explicacion = scrolledtext.ScrolledText(
            right_frame,
            font=Styles.FONTS['body'],
            bg='white',
            height=8,
            wrap=tk.WORD
        )
        campo_explicacion.pack(fill='x', pady=(0, 10))

        # Campo imagen
        CustomLabel(
            right_frame,
            text="Imagen del doctor:",
            font=Styles.FONTS['body_bold'],
            fg=Styles.COLORS['secondary']
        ).pack(anchor='w', pady=(0, 5))
        
        imagen_frame = tk.Frame(right_frame, bg=Styles.COLORS['surface'])
        imagen_frame.pack(fill='x', pady=(0, 15))
        
        campo_imagen = tk.Entry(
            imagen_frame,
            font=Styles.FONTS['body'],
            bg='white'
        )
        campo_imagen.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        # Botón seleccionar imagen
        CustomButton(
            imagen_frame,
            text="Seleccionar",
            command=cargar_imagen,
            width=100,
            color=Styles.COLORS['secondary']
        ).pack(side='right')

        # Botón guardar
        CustomButton(
            main_frame,
            text="Guardar Conocimiento",
            command=guardar_nuevo_conocimiento,
            width=200
        ).pack(pady=(20, 0))

    def iniciar(self):
        """Inicia el bucle principal de la interfaz"""
        self.ventana.mainloop()

if __name__ == "__main__":
    app = InterfazMedica()
    app.iniciar()