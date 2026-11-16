import time
import sys

# Tarifas vigentes (Zona EMT Madrid, junio 2025)
TARIFA_PARADO = 0.02      # €/segundo (< 20 km/h o detenido)
TARIFA_MOVIMIENTO = 0.05  # €/segundo

def mostrar_ayuda():
    print("=" * 60)
    print(" 🚕 TAXITECH SOLUTIONS - SISTEMA DE TAXÍMETRO DIGITAL (MVP) ")
    print("=" * 60)
    print(" Instrucciones de uso:")
    print("   [M] - Poner en Movimiento (Tarifa rápida: 0.05 €/s)")
    print("   [P] - Poner Parado / Semáforo (Tarifa lenta: 0.02 €/s)")
    print("   [F] - Finalizar Carrera y cobrar al pasajero")
    print("   [Q] - Salir de la aplicación")
    print("-" * 60)

def ejecutar_carrera(numero_carrera):
    print(f"\n--- INICIANDO CARRERA #{numero_carrera} ---")
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
            print("  ➡️ Vehículo en MOVIMIENTO (0.05 €/s)")
        elif comando == 'P':
            estado = "PARADO"
            print("  ⏸️ Vehículo PARADO / Semáforo (0.02 €/s)")
        elif comando == 'F':
            total = (tiempo_acumulado_parado * TARIFA_PARADO) + (tiempo_acumulado_movimiento * TARIFA_MOVIMIENTO)
            duracion_total = tiempo_acumulado_parado + tiempo_acumulado_movimiento
            
            print("\n" + "="*40)
            print(f" 🏁 CARRERA #{numero_carrera} FINALIZADA")
            print(f" ⏱️ Duración total: {duracion_total:.2f} segundos")
            print(f"    - Parado: {tiempo_acumulado_parado:.2f}s")
            print(f"    - Movimiento: {tiempo_acumulado_movimiento:.2f}s")
            print(f" 💶 TOTAL A COBRAR: {total:.2f} €")
            print("="*40 + "\n")
            return
        else:
            print(" ⚠️ Comando no reconocido. Use M (Movimiento), P (Parado) o F (Finalizar).")

def main():
    mostrar_ayuda()
    num_carrera = 1
    
    while True:
        comando_inicio = input("¿Desea iniciar una nueva carrera? (S para iniciar, Q para salir): ").strip().upper()
        if comando_inicio == 'S':
            ejecutar_carrera(num_carrera)
            num_carrera += 1
        elif comando_inicio == 'Q':
            print("¡Gracias por utilizar TaxiTech Systems! Saliendo...")
            sys.exit(0)
        else:
            print("Comando inválido. Pulse 'S' para iniciar carrera o 'Q' para salir.")

if __name__ == "__main__":
    main()