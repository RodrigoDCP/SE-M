# motor_de_inferencia.py
def asignar_medico(base_hechos):
    datos = base_hechos.obtener_datos()
    
    # Lógica de inferencia para asignar un médico
    if datos["Costo"] == "barato" and datos["Disponibilidad"] == "mañana":
        return "Dr. Pérez"
    elif datos["Costo"] == "costeable" and datos["Historial Médico"] == "alergias":
        return "Dra. López"
    # Puedes agregar más reglas aquí
    else:
        return "Médico General"
