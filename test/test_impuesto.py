import unittest
import impuestos

class PruebasImpuesto(unittest.TestCase):

    def test_normal_1(self):
        compra = 1000000
        impuesto = 19
        esperado_T = 1190000

        T = impuestos.calcular_total(compra, impuesto)

        self.assertAlmostEqual(T, esperado_T,0)

    def test_normal_2(self):
        compra = 800_000
        impuesto = 19
        esperado_T = 952_000

        T = impuestos.calcular_total(compra, impuesto)
        self.assertAlmostEqual(T, esperado_T,0)

    def test_normal_3(self):
        compra = 700_000
        impuesto = 19
        esperado_T = 833_000
        T = impuestos.calcular_total(compra, impuesto)
        self.assertAlmostEqual(T, esperado_T,0)

if __name__ == '__main__':
    unittest.main()