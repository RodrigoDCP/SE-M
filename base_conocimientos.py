import json
import os

class BaseConocimientos:
    def __init__(self, archivo='base_conocimientos.json'):
        self.archivo = archivo
        self.conocimientos = self._cargar_conocimientos()

    def _cargar_conocimientos(self):
        """Carga los conocimientos desde el archivo JSON"""
        try:
            with open(self.archivo, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def recargar_conocimientos(self):
        """Recarga los conocimientos del archivo"""
        self.conocimientos = self._cargar_conocimientos()
        
    def obtener_conocimiento(self, clave):
        """Obtiene el conocimiento para una clave específica"""
        # Recargar conocimientos antes de obtener
        self.recargar_conocimientos()
        return self.conocimientos.get(str(clave))

    def agregar_conocimiento(self, clave, doctor, explicacion, imagen):
        self.conocimientos[str(clave)] = {
            "recomendacion": doctor,
            "explicacion": explicacion.splitlines(),
            "imagen": imagen
        }
        self.guardar_conocimientos()
        return True

    def guardar_conocimientos(self):
        with open(self.archivo, 'w') as f:
            json.dump(self.conocimientos, f, indent=4)

    def ultima_modificacion(self):
        try:
            return os.path.getmtime(self.archivo)
        except FileNotFoundError:
            return 0