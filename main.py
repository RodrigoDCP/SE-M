# main.py
from BH import BaseDeHechos
from MoIn import asignar_medico

def hacer_preguntas():
    base_hechos = BaseDeHechos()
    
    # Realizar preguntas y almacenar respuestas
    disponibilidad = input("¿En qué horario prefieres? (mañana, tarde, noche, fines de semana): ")
    base_hechos.agregar_dato("Disponibilidad", disponibilidad)
    
    costo = input("¿Cuál es tu presupuesto? (barato, costeable, caro, muy caro): ")
    base_hechos.agregar_dato("Costo", costo)
    
    historial = input("¿Tienes algún historial médico relevante? (alergias, recién operado, enfermedad crónica, nada): ")
    base_hechos.agregar_dato("Historial Médico", historial)
    
    return base_hechos

def main():
    base_hechos = hacer_preguntas()
    medico = asignar_medico(base_hechos)
    print(f"El médico asignado es: {medico}")

if __name__ == "__main__":
    main()
