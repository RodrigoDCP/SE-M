from base_hechos import BaseHechos
from base_conocimientos import BaseConocimientos
from modulo_adquisicion import ModuloAdquisicion
from modulo_explicacion import ModuloExplicacion
class MotorInferencia:
    """
    Clase principal que coordina todos los componentes
    """
    def __init__(self):
        self.base_conocimientos = BaseConocimientos()
        self.base_hechos = BaseHechos()
        self.modulo_adquisicion = ModuloAdquisicion(self.base_conocimientos)
        self.modulo_explicacion = ModuloExplicacion()
        
    def inferir(self, hechos):
        self.base_hechos.hechos = hechos
        
        clave = str((
            hechos["motivo_consulta"],
            hechos["nivel_sintomas"],
            hechos["historial_medico"],
            hechos["edad"]
        ))
        
        conocimiento = self.base_conocimientos.obtener_conocimiento(clave)
        
        if conocimiento:
            self.modulo_explicacion.guardar_explicacion(
                conocimiento["recomendacion"],
                conocimiento["explicacion"],
                conocimiento["imagen"]
            )
            return True
        return False
        
    def obtener_explicacion(self):
        return self.modulo_explicacion.obtener_explicacion_completa()
        
    def obtener_imagen(self):
        return self.modulo_explicacion.obtener_imagen_doctor()
        
    def agregar_conocimiento(self, doctor, explicacion, imagen):
        return self.modulo_adquisicion.procesar_nuevo_conocimiento(
            self.base_hechos.hechos,
            doctor,
            explicacion,
            imagen
        )
        
    def ultima_actualizacion(self):
        return self.base_conocimientos.ultima_modificacion()
    def obtener_recomendacion(self):
        """Retorna solo la recomendación del doctor sin la explicación"""
        if hasattr(self.modulo_explicacion, 'ultima_recomendacion'):
            return self.modulo_explicacion.ultima_recomendacion
        return "No hay recomendación disponible."
        
    def obtener_explicacion(self):
        """Retorna solo la explicación detallada"""
        if hasattr(self.modulo_explicacion, 'ultima_explicacion'):
            return "\n".join(self.modulo_explicacion.ultima_explicacion)
        return "No hay explicación disponible."