# base_de_hechos.py
class BaseDeHechos:
    def __init__(self):
        self.datos_paciente = {}

    def agregar_dato(self, pregunta, respuesta):
        self.datos_paciente[pregunta] = respuesta

    def obtener_datos(self):
        return self.datos_paciente
