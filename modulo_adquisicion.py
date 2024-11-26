class ModuloAdquisicion:
    """
    Clase que maneja la adquisición de nuevos conocimientos
    """
    def __init__(self, base_conocimientos):
        self.base_conocimientos = base_conocimientos
        
    def validar_datos(self, doctor, explicacion, imagen):
        return all([doctor, explicacion, imagen])
        
    def procesar_nuevo_conocimiento(self, hechos, doctor, explicacion, imagen):
        if not self.validar_datos(doctor, explicacion, imagen):
            return False
            
        clave = str((
            hechos["motivo_consulta"],
            hechos["nivel_sintomas"],
            hechos["historial_medico"],
            hechos["edad"]
        ))
        
        self.base_conocimientos.agregar_conocimiento(clave, doctor, explicacion, imagen)
        return True