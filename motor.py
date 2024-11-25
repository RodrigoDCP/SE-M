import json

class MotorInferencia:
    @staticmethod
    def cargar_base_conocimientos():
        try:
            with open('base_conocimientos.json', 'r') as archivo_json:
                datos_json = json.load(archivo_json)
                if not datos_json:  # Si el archivo está vacío
                    return {}
                return datos_json
        except FileNotFoundError:
            with open('base_conocimientos.json', 'w') as archivo_json:
                json.dump({}, archivo_json)
            return {}
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def obtener_recomendacion(hechos):
        base_conocimientos = MotorInferencia.cargar_base_conocimientos()
        clave = str((
            hechos["motivo_consulta"],
            hechos["nivel_sintomas"],
            hechos["historial_medico"],
            hechos["edad"]
        ))
        
        if clave in base_conocimientos:
            return (
                base_conocimientos[clave]["recomendacion"],
                "\n".join(base_conocimientos[clave]["explicacion"]),
                base_conocimientos[clave]["imagen"]
            )
        return "Lo siento, no tengo una recomendacion adecuada.", "", None

    @staticmethod
    def guardar_conocimiento(hechos, doctor, explicacion, imagen):
        try:
            base_conocimientos = MotorInferencia.cargar_base_conocimientos()
            
            clave = str((
                hechos["motivo_consulta"],
                hechos["nivel_sintomas"],
                hechos["historial_medico"],
                hechos["edad"]
            ))
            
            base_conocimientos[clave] = {
                "recomendacion": doctor,
                "explicacion": explicacion.splitlines(),
                "imagen": imagen
            }
            
            with open('base_conocimientos.json', 'w') as archivo:
                json.dump(base_conocimientos, archivo, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar: {str(e)}")
            return False