import unittest

from src.model.calculadora_impuestos import CalculadoraImpuestos, CategoriaProducto, TipoImpuesto


class TestCalculadoraImpuestos(unittest.TestCase):
    def setUp(self):
        self.calculadora = CalculadoraImpuestos()
    
    def test_001_alimentos_basicos_iva_5(self):
        valor_base = 1000.0
        categoria = CategoriaProducto.ALIMENTOS_BASICOS
        resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
        self.assertEqual(resultado['valor_base'], 1000.0)
        self.assertEqual(resultado['categoria'], "Alimentos Básicos")
        self.assertEqual(resultado['impuestos']['IVA 5%'], 50.0)
        self.assertEqual(resultado['total_impuestos'], 50.0)
        self.assertEqual(resultado['valor_total'], 1050.0)
    
    def test_002_licores_impuestos_multiples(self):
        valor_base = 2000.0
        categoria = CategoriaProducto.LICORES
        resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
        self.assertEqual(resultado['valor_base'], 2000.0)
        self.assertEqual(resultado['categoria'], "Licores")
        self.assertEqual(resultado['impuestos']['IVA 19%'], 380.0)
        self.assertEqual(resultado['impuestos']['Impuesto de Rentas a los Licores'], 500.0)
        self.assertEqual(resultado['total_impuestos'], 880.0)
        self.assertEqual(resultado['valor_total'], 2880.0)
    
    def test_003_servicios_publicos_exento(self):
        valor_base = 150000.0
        categoria = CategoriaProducto.SERVICIOS_PUBLICOS
        resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
        self.assertEqual(resultado['valor_base'], 150000.0)
        self.assertEqual(resultado['categoria'], "Servicios Públicos")
        self.assertEqual(resultado['impuestos']['Exento'], 0.0)
        self.assertEqual(resultado['total_impuestos'], 0.0)
        self.assertEqual(resultado['valor_total'], 150000.0)
    
    def test_004_otros_productos_iva_19(self):
        valor_base = 5000.0
        categoria = CategoriaProducto.OTROS
        resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
        self.assertEqual(resultado['valor_base'], 5000.0)
        self.assertEqual(resultado['categoria'], "Otros")
        self.assertEqual(resultado['impuestos']['IVA 19%'], 950.0)
        self.assertEqual(resultado['total_impuestos'], 950.0)
        self.assertEqual(resultado['valor_total'], 5950.0)
    
    def test_005_valor_muy_pequeno(self):
        valor_base = 0.01
        categoria = CategoriaProducto.ALIMENTOS_BASICOS
        resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
        self.assertEqual(resultado['valor_base'], 0.01)
        self.assertEqual(resultado['impuestos']['IVA 5%'], 0.0)
        self.assertEqual(resultado['total_impuestos'], 0.0)
        self.assertEqual(resultado['valor_total'], 0.01)
    
    def test_006_valor_muy_grande(self):
        valor_base = 10000000.0
        categoria = CategoriaProducto.COMBUSTIBLES
        resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
        self.assertEqual(resultado['valor_base'], 10000000.0)
        self.assertEqual(resultado['impuestos']['IVA 19%'], 1900000.0)
        self.assertEqual(resultado['impuestos']['Impuesto Nacional al Consumo'], 800000.0)
        self.assertEqual(resultado['total_impuestos'], 2700000.0)
        self.assertEqual(resultado['valor_total'], 12700000.0)
    
    def test_007_valor_decimal_complejo(self):
        valor_base = 1234.567890
        categoria = CategoriaProducto.BOLSAS_PLASTICAS
        resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
        self.assertEqual(resultado['valor_base'], 1234.567890)
        self.assertEqual(resultado['impuestos']['IVA 19%'], 234.57)
        self.assertEqual(resultado['impuestos']['Impuesto de Bolsas Plásticas'], 246.91)
        self.assertEqual(resultado['total_impuestos'], 481.48)
        self.assertEqual(resultado['valor_total'], 1716.05)
    
    def test_008_verificar_categorias_disponibles(self):
        categorias = self.calculadora.obtener_categorias_disponibles()
        categorias_esperadas = [
            "Alimentos Básicos",
            "Licores", 
            "Bolsas Plásticas",
            "Combustibles",
            "Servicios Públicos",
            "Otros"
        ]
        self.assertEqual(len(categorias), 6)
        for categoria in categorias_esperadas:
            self.assertIn(categoria, categorias)
    
    def test_009_error_valor_negativo(self):
        valor_base = -100.0
        categoria = CategoriaProducto.ALIMENTOS_BASICOS
        with self.assertRaises(ValueError) as context:
            self.calculadora.calcular_impuestos(valor_base, categoria)
        self.assertIn("El valor base debe ser mayor a 0", str(context.exception))
    
    def test_010_error_valor_cero(self):
        valor_base = 0.0
        categoria = CategoriaProducto.OTROS
        with self.assertRaises(ValueError) as context:
            self.calculadora.calcular_impuestos(valor_base, categoria)
        self.assertIn("El valor base debe ser mayor a 0", str(context.exception))
    
    def test_011_error_obtener_impuestos_categoria_invalida(self):
        with self.assertRaises(ValueError) as context:
            self.calculadora.obtener_impuestos_por_categoria(None)
        self.assertIn("Categoría no válida", str(context.exception))


if __name__ == '__main__':
    unittest.main(verbosity=2, buffer=True)


