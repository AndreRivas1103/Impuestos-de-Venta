import sys
import os
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.model.calculadora_impuestos import CalculadoraImpuestos, CategoriaProducto, TipoImpuesto


class TestCalculadoraImpuestos(unittest.TestCase):
    """Test suite para la Calculadora de Impuestos de Venta"""
    
    def setUp(self):
        """Configuración inicial antes de cada test"""
        self.calculadora = CalculadoraImpuestos()
    
    # CASOS NORMALES (4 tests)
    
    def test_001_alimentos_basicos_iva_5(self):
        """Test caso normal: Cálculo de IVA 5% para alimentos básicos"""
        valor_base = 1000.0
        categoria = CategoriaProducto.ALIMENTOS_BASICOS
        
        resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
        
        self.assertEqual(resultado['valor_base'], 1000.0)
        self.assertEqual(resultado['categoria'], "Alimentos Básicos")
        self.assertEqual(resultado['impuestos']['IVA 5%'], 50.0)
        self.assertEqual(resultado['total_impuestos'], 50.0)
        self.assertEqual(resultado['valor_total'], 1050.0)
    
    def test_002_licores_impuestos_multiples(self):
        """Test caso normal: Cálculo de impuestos múltiples para licores"""
        valor_base = 2000.0
        categoria = CategoriaProducto.LICORES
        
        resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
        
        self.assertEqual(resultado['valor_base'], 2000.0)
        self.assertEqual(resultado['categoria'], "Licores")
        self.assertEqual(resultado['impuestos']['IVA 19%'], 380.0)  # 2000 * 0.19
        self.assertEqual(resultado['impuestos']['Impuesto de Rentas a los Licores'], 500.0)  # 2000 * 0.25
        self.assertEqual(resultado['total_impuestos'], 880.0)
        self.assertEqual(resultado['valor_total'], 2880.0)
    
    def test_003_servicios_publicos_exento(self):
        """Test caso normal: Servicios públicos exentos de impuestos"""
        valor_base = 150000.0
        categoria = CategoriaProducto.SERVICIOS_PUBLICOS
        
        resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
        
        self.assertEqual(resultado['valor_base'], 150000.0)
        self.assertEqual(resultado['categoria'], "Servicios Públicos")
        self.assertEqual(resultado['impuestos']['Exento'], 0.0)
        self.assertEqual(resultado['total_impuestos'], 0.0)
        self.assertEqual(resultado['valor_total'], 150000.0)
    
    def test_004_otros_productos_iva_19(self):
        """Test caso normal: Otros productos con IVA 19%"""
        valor_base = 5000.0
        categoria = CategoriaProducto.OTROS
        
        resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
        
        self.assertEqual(resultado['valor_base'], 5000.0)
        self.assertEqual(resultado['categoria'], "Otros")
        self.assertEqual(resultado['impuestos']['IVA 19%'], 950.0)
        self.assertEqual(resultado['total_impuestos'], 950.0)
        self.assertEqual(resultado['valor_total'], 5950.0)
    
    # CASOS EXTRAORDINARIOS (4 tests)
    
    def test_005_valor_muy_pequeno(self):
        """Test caso extraordinario: Valor muy pequeño (centavos)"""
        valor_base = 0.01
        categoria = CategoriaProducto.ALIMENTOS_BASICOS
        
        resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
        
        self.assertEqual(resultado['valor_base'], 0.01)
        self.assertAlmostEqual(resultado['impuestos']['IVA 5%'], 0.0005, places=4)
        self.assertAlmostEqual(resultado['total_impuestos'], 0.0005, places=4)
        self.assertAlmostEqual(resultado['valor_total'], 0.0105, places=4)
    
    def test_006_valor_muy_grande(self):
        """Test caso extraordinario: Valor muy grande (millones)"""
        valor_base = 10000000.0
        categoria = CategoriaProducto.COMBUSTIBLES
        
        resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
        
        self.assertEqual(resultado['valor_base'], 10000000.0)
        self.assertEqual(resultado['impuestos']['IVA 19%'], 1900000.0)  # 10M * 0.19
        self.assertEqual(resultado['impuestos']['Impuesto Nacional al Consumo'], 800000.0)  # 10M * 0.08
        self.assertEqual(resultado['total_impuestos'], 2700000.0)
        self.assertEqual(resultado['valor_total'], 12700000.0)
    
    def test_007_valor_decimal_complejo(self):
        """Test caso extraordinario: Valor con muchos decimales"""
        valor_base = 1234.567890
        categoria = CategoriaProducto.BOLSAS_PLASTICAS
        
        resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
        
        self.assertEqual(resultado['valor_base'], 1234.567890)
        self.assertAlmostEqual(resultado['impuestos']['IVA 19%'], 234.567899, places=6)
        self.assertAlmostEqual(resultado['impuestos']['Impuesto de Bolsas Plásticas'], 246.913578, places=6)
        self.assertAlmostEqual(resultado['total_impuestos'], 481.481477, places=6)
        self.assertAlmostEqual(resultado['valor_total'], 1716.049367, places=6)
    
    def test_008_verificar_categorias_disponibles(self):
        """Test caso extraordinario: Verificar que todas las categorías están disponibles"""
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
    
    # CASOS DE ERROR (3 tests)
    
    def test_009_error_valor_negativo(self):
        """Test caso de error: Valor base negativo"""
        valor_base = -100.0
        categoria = CategoriaProducto.ALIMENTOS_BASICOS
        
        with self.assertRaises(ValueError) as context:
            self.calculadora.calcular_impuestos(valor_base, categoria)
        
        self.assertIn("El valor base debe ser mayor a 0", str(context.exception))
    
    def test_010_error_valor_cero(self):
        """Test caso de error: Valor base igual a cero"""
        valor_base = 0.0
        categoria = CategoriaProducto.OTROS
        
        with self.assertRaises(ValueError) as context:
            self.calculadora.calcular_impuestos(valor_base, categoria)
        
        self.assertIn("El valor base debe ser mayor a 0", str(context.exception))
    
    def test_011_error_obtener_impuestos_categoria_invalida(self):
        """Test caso de error: Obtener impuestos de categoría inválida usando None"""
        with self.assertRaises(ValueError) as context:
            self.calculadora.obtener_impuestos_por_categoria(None)
        
        self.assertIn("Categoría no válida", str(context.exception))


if __name__ == '__main__':
    # Configurar el runner de tests para mostrar información detallada
    unittest.main(verbosity=2, buffer=True)