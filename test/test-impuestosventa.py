import unittest

from impuesto import impuesto_pagar


class PuebasImpuestos(unittest.TestCase):

    def test_extraordinario_1(self):
        # Entradas
        compra = 1_000_000
        impuesto = 21

        # Probar Proceso
        total_calculado = impuesto_pagar(compra, impuesto)

        # Verificar Salidas
        pago_esperado = 1210000

        self.assertAlmostEqual(total_calculado, pago_esperado, 0)

    def test_extraordinario_2(self):
        # Entradas
        compra = 1_000_000
        impuesto = 21

        # Probar Proceso
        total_calculado = impuesto_pagar(compra, impuesto)

        # Verificar Salidas
        pago_esperado = 1210000

        self.assertAlmostEqual(total_calculado, pago_esperado, 0)

    def test_extraordinario_3(self):
        # Entradas
        compra = 1_000_000
        impuesto = 21

        # Probar Proceso
        total_calculado = impuesto_pagar(compra, impuesto)

        # Verificar Salidas
        pago_esperado = 1210000

        self.assertAlmostEqual(total_calculado, pago_esperado, 0)


if '__name__' == '__main__':
    unittest.main()

