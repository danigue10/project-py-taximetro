import time
import sys
import logging
import json
import os

# Configuración del sistema de logs (US-06)
logging.basicConfig(
    filename='taxitech.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# Tarifas vigentes (Zona EMT Madrid, junio 2025)
# Cargar tarifas desde el fichero de configuración externo (US-07)
try:
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
        TARIFA_PARADO = config.get("tarifa_parado", 0.02)
        TARIFA_MOVIMIENTO = config.get("tarifa_movimiento", 0.05)
        logging.info("Tarifas cargadas correctamente desde config.json")
except Exception as e:
    # Valores por defecto de seguridad por si el archivo fallara
    TARIFA_PARADO = 0.02
    TARIFA_MOVIMIENTO = 0.05
    logging.warning(f"No se pudo leer config.json, usando tarifas por defecto: {e}")

def mostrar_ayuda():
    print("=" * 60)
    print(" 🚕 TAXITECH SOLUTIONS - SISTEMA DE TAXÍMETRO DIGITAL (Fase 2) ")
    print("=" * 60)
    print(" Instrucciones de uso:")
    print("   [M] - Poner en Movimiento (Tarifa rápida: 0.05 €/s)")
    print("   [P] - Poner Parado / Semáforo (Tarifa lenta: 0.02 €/s)")
    print("   [F] - Finalizar Carrera y cobrar al pasajero")
    print("   [Q] - Salir de la aplicación")
    print("-" * 60)

def guardar_carrera_en_historico(numero_carrera, duracion, parado, movimiento, total):
    registro = {
        "carrera": numero_carrera,
        "fecha": time.strftime("%Y-%m-%d %H:%M:%S"),
        "duracion_total_segundos": round(duracion, 2),
        "tiempo_parado_segundos": round(parado, 2),
        "tiempo_movimiento_segundos": round(movimiento, 2),
        "total_euros": round(total, 2)
    }
    
    archivo = "historial_carreras.json"
    datos = []
    
    # Si el archivo ya existe, leemos lo que hay dentro
    if os.path.exists(archivo):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
        except json.JSONDecodeError:
            datos = []
            
    # Añadimos la nueva carrera
    datos.append(registro)
    
    # Guardamos de nuevo el archivo actualizado
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
        
    logging.info(f"Carrera #{numero_carrera} guardada en el histórico persistente.")

def guardar_carrera_en_historico(numero_carrera, duracion, parado, movimiento, total):
    # Aquí vamos a empaquetar los datos de la carrera en un diccionario
    registro = {
        "carrera": numero_carrera,
        "fecha": time.strftime("%Y-%m-%d %H:%M:%S"),
        "duracion_total_segundos": round(duracion, 2),
        "tiempo_parado_segundos": round(parado, 2),
        "tiempo_movimiento_segundos": round(movimiento, 2),
        "total_euros": round(total, 2)
    }

    archivo = "historial_carreras.json"
    datos = []
    
    # Si el archivo ya existe, leemos lo que hay dentro
    if os.path.exists(archivo):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
        except json.JSONDecodeError:
            datos = []
            
    # Añadimos la nueva carrera a la lista
    datos.append(registro)
    
    # Guardamos de nuevo el archivo actualizado en formato JSON bonito (indentado)
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
        
    logging.info(f"Carrera #{numero_carrera} guardada en el histórico persistente.")

def ejecutar_carrera(numero_carrera):
    print(f"\n--- INICIANDO CARRERA #{numero_carrera} ---")
    logging.info(f"Iniciando carrera #{numero_carrera}")
    print("Comandos: [M] Movimiento | [P] Parado | [F] Finalizar")
    
    estado = "PARADO"  # Estado inicial por defecto
    inicio_carrera = time.time()
    tiempo_acumulado_parado = 0.0
    tiempo_acumulado_movimiento = 0.0
    
    ultimo_cambio = inicio_carrera

    while True:
        comando = input(f"[{estado}] Estado actual. Introduzca comando (M/P/F): ").strip().upper()
        
        ahora = time.time()
        duracion_tramo = ahora - ultimo_cambio
        
        if estado == "PARADO":
            tiempo_acumulado_parado += duracion_tramo
        elif estado == "MOVIMIENTO":
            tiempo_acumulado_movimiento += duracion_tramo
            
        ultimo_cambio = ahora

        if comando == 'M':
            estado = "MOVIMIENTO"
            logging.info(f"Carrera #{numero_carrera}: Cambio de estado a MOVIMIENTO")
            print("  ➡️ Vehículo en MOVIMIENTO (0.05 €/s)")
        elif comando == 'P':
            estado = "PARADO"
            logging.info(f"Carrera #{numero_carrera}: Cambio de estado a PARADO")
            print("  ⏸️ Vehículo PARADO / Semáforo (0.02 €/s)")
        elif comando == 'F':
            total = (tiempo_acumulado_parado * TARIFA_PARADO) + (tiempo_acumulado_movimiento * TARIFA_MOVIMIENTO)
            duracion_total = tiempo_acumulado_parado + tiempo_acumulado_movimiento
            
            logging.info(f"Carrera #{numero_carrera} finalizada. Duración: {duracion_total:.2f}s, Total: {total:.2f} €")

            # Guardar en el histórico persistente (US-05)
            guardar_carrera_en_historico(numero_carrera, duracion_total, tiempo_acumulado_parado, tiempo_acumulado_movimiento, total)

            print("\n" + "="*40)
            print(f" 🏁 CARRERA #{numero_carrera} FINALIZADA")
            print(f" ⏱️ Duración total: {duracion_total:.2f} segundos")
            print(f"    - Parado: {tiempo_acumulado_parado:.2f}s")
            print(f"    - Movimiento: {tiempo_acumulado_movimiento:.2f}s")
            print(f" 💶 TOTAL A COBRAR: {total:.2f} €")
            print("="*40 + "\n")
            return
        else:
            logging.warning(f"Carrera #{numero_carrera}: Comando no reconocido introducido: {comando}")
            print(" ⚠️ Comando no reconocido. Use M (Movimiento), P (Parado) o F (Finalizar).")

def main():
    logging.info("Aplicación de taxímetro iniciada.")
    mostrar_ayuda()
    num_carrera = 1
    
    while True:
        comando_inicio = input("¿Desea iniciar una nueva carrera? (S para iniciar, Q para salir): ").strip().upper()
        if comando_inicio == 'S':
            ejecutar_carrera(num_carrera)
            num_carrera += 1
        elif comando_inicio == 'Q':
            logging.info("Aplicación cerrada por el usuario.")
            print("¡Gracias por utilizar TaxiTech Systems! Saliendo...")
            sys.exit(0)
        else:
            logging.warning(f"Comando de menú principal inválido: {comando_inicio}")
            print("Comando inválido. Pulse 'S' para iniciar carrera o 'Q' para salir.")

if __name__ == "__main__":
    main()
