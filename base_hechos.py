class BaseHechos:
    """
    Clase que maneja los hechos/datos del paciente
    """
    def __init__(self):
        self.hechos = {
            "motivo_consulta": "",
            "nivel_sintomas": "",
            "historial_medico": "",
            "edad": ""
        }
    
    def actualizar_hecho(self, tipo, valor):
        if tipo in self.hechos:
            self.hechos[tipo] = valor
            return True
        return False
    
    def obtener_hechos(self):
        return self.hechos.copy()
    
    def limpiar_hechos(self):
        self.hechos = {key: "" for key in self.hechos}