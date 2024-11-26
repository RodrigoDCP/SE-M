class ModuloExplicacion:
    """
    Clase que maneja la generación de explicaciones
    """
    def __init__(self):
        self.ultima_recomendacion = None
        self.ultima_explicacion = None
        self.ultima_imagen = None
        
    def guardar_explicacion(self, recomendacion, explicacion, imagen):
        self.ultima_recomendacion = recomendacion
        self.ultima_explicacion = explicacion
        self.ultima_imagen = imagen
        
    def obtener_explicacion_completa(self):
        if not self.ultima_recomendacion:
            return "No hay explicación disponible."
            
        explicacion = f"RECOMENDACIÓN:\n{self.ultima_recomendacion}\n\n"
        explicacion += "EXPLICACIÓN:\n" + "\n".join(self.ultima_explicacion)
        return explicacion
        
    def obtener_imagen_doctor(self):
        return self.ultima_imagen