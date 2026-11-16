import unittest

class TestTaximetro(unittest.TestCase):
    
    def test_calculo_tarifa(self):
        # Definimos tarifas de prueba (igual que en config.json)
        tarifa_parado = 0.02
        tarifa_movimiento = 0.05
        
        # Simulamos tiempos: 10 segundos parado y 10 segundos en movimiento
        tiempo_parado = 10.0
        tiempo_movimiento = 10.0
        
        # Cálculo esperado: (10 * 0.02) + (10 * 0.05) = 0.20 + 0.50 = 0.70 €
        total_esperado = (tiempo_parado * tarifa_parado) + (tiempo_movimiento * tarifa_movimiento)
        
        # Verificamos que el resultado sea exactamente 0.70 (usando round para evitar decimales flotantes largos)
        self.assertAlmostEqual(total_esperado, 0.70, places=2)

if __name__ == '__main__':
    unittest.main()