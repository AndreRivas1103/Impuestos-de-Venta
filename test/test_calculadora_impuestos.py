import sys
import os
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from model.calculadora_impuestos import CalculadoraImpuestos, CategoriaProducto, TipoImpuesto

class TestCalculadoraImpuestos(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.calculadora = CalculadoraImpuestos()
    
    # ===== PRUEBAS NORMALES =====
    
    def test_calcular_impuestos_alimentos_basicos(self):
        """Prueba normal: Calcular impuestos para alimentos básicos (IVA 5%)"""
        valor_base = 1000
        categoria = CategoriaProducto.ALIMENTOS_BASICOS
        
        resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
        
        self.assertEqual(resultado['valor_base'], 1000)
        self.assertEqual(resultado['categoria'], 'Alimentos Básicos')
        self.assertEqual(resultado['impuestos']['IVA 5%'], 50)
        self.assertEqual(resultado['total_impuestos'], 50)
        self.assertEqual(resultado['valor_total'], 1050)
    
    def test_calcular_impuestos_otros_productos(self):
        """Prueba normal: Calcular impuestos para otros productos (IVA 19%)"""
        valor_base = 2000
        categoria = CategoriaProducto.OTROS
        
        resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
        
        self.assertEqual(resultado['valor_base'], 2000)
        self.assertEqual(resultado['categoria'], 'Otros')
        self.assertEqual(resultado['impuestos']['IVA 19%'], 380)
        self.assertEqual(resultado['total_impuestos'], 380)
        self.assertEqual(resultado['valor_total'], 2380)
    
    def test_calcular_impuestos_servicios_publicos(self):
        """Prueba normal: Calcular impuestos para servicios públicos (Exento)"""
        valor_base = 500
        categoria = CategoriaProducto.SERVICIOS_PUBLICOS
        
        resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
        
        self.assertEqual(resultado['valor_base'], 500)
        self.assertEqual(resultado['categoria'], 'Servicios Públicos')
        self.assertEqual(resultado['impuestos']['Exento'], 0)
        self.assertEqual(resultado['total_impuestos'], 0)
        self.assertEqual(resultado['valor_total'], 500)
    
    def test_obtener_categorias_disponibles(self):
        """Prueba normal: Obtener lista de categorías disponibles"""
        categorias = self.calculadora.obtener_categorias_disponibles()
        
        self.assertIsInstance(categorias, list)
        self.assertEqual(len(categorias), 6)
        self.assertIn('Alimentos Básicos', categorias)
        self.assertIn('Licores', categorias)
        self.assertIn('Bolsas Plásticas', categorias)
        self.assertIn('Combustibles', categorias)
        self.assertIn('Servicios Públicos', categorias)
        self.assertIn('Otros', categorias)
    
    # ===== PRUEBAS EXTRAORDINARIAS =====
    
    def test_calcular_impuestos_licores_multiple(self):
        """Prueba extraordinaria: Calcular impuestos para licores (IVA 19% + Impuesto Licores)"""
        valor_base = 1000
        categoria = CategoriaProducto.LICORES
        
        resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
        
        self.assertEqual(resultado['valor_base'], 1000)
        self.assertEqual(resultado['categoria'], 'Licores')
        self.assertEqual(resultado['impuestos']['IVA 19%'], 190)
        self.assertEqual(resultado['impuestos']['Impuesto de Rentas a los Licores'], 250)
        self.assertEqual(resultado['total_impuestos'], 440)
        self.assertEqual(resultado['valor_total'], 1440)
    
    def test_calcular_impuestos_combustibles_multiple(self):
        """Prueba extraordinaria: Calcular impuestos para combustibles (IVA 19% + INC)"""
        valor_base = 5000
        categoria = CategoriaProducto.COMBUSTIBLES
        
        resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
        
        self.assertEqual(resultado['valor_base'], 5000)
        self.assertEqual(resultado['categoria'], 'Combustibles')
        self.assertEqual(resultado['impuestos']['IVA 19%'], 950)
        self.assertEqual(resultado['impuestos']['Impuesto Nacional al Consumo'], 400)
        self.assertEqual(resultado['total_impuestos'], 1350)
        self.assertEqual(resultado['valor_total'], 6350)
    
    def test_calcular_impuestos_bolsas_plasticas_multiple(self):
        """Prueba extraordinaria: Calcular impuestos para bolsas plásticas (IVA 19% + Impuesto Bolsas)"""
        valor_base = 100
        categoria = CategoriaProducto.BOLSAS_PLASTICAS
        
        resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
        
        self.assertEqual(resultado['valor_base'], 100)
        self.assertEqual(resultado['categoria'], 'Bolsas Plásticas')
        self.assertEqual(resultado['impuestos']['IVA 19%'], 19)
        self.assertEqual(resultado['impuestos']['Impuesto de Bolsas Plásticas'], 20)
        self.assertEqual(resultado['total_impuestos'], 39)
        self.assertEqual(resultado['valor_total'], 139)
    
    def test_obtener_impuestos_por_categoria(self):
        """Prueba extraordinaria: Obtener impuestos específicos por categoría"""
        categoria = CategoriaProducto.LICORES
        impuestos = self.calculadora.obtener_impuestos_por_categoria(categoria)
        
        self.assertIsInstance(impuestos, list)
        self.assertEqual(len(impuestos), 2)
        self.assertIn('IVA 19%', impuestos)
        self.assertIn('Impuesto de Rentas a los Licores', impuestos)
    
    # ===== PRUEBAS DE ERROR =====
    
    def test_error_valor_base_negativo(self):
        """Prueba de error: Valor base negativo"""
        valor_base = -100
        categoria = CategoriaProducto.OTROS
        
        with self.assertRaises(ValueError) as context:
            self.calculadora.calcular_impuestos(valor_base, categoria)
        
        self.assertIn("El valor base debe ser mayor a 0", str(context.exception))
    
    def test_error_valor_base_cero(self):
        """Prueba de error: Valor base igual a cero"""
        valor_base = 0
        categoria = CategoriaProducto.ALIMENTOS_BASICOS
        
        with self.assertRaises(ValueError) as context:
            self.calculadora.calcular_impuestos(valor_base, categoria)
        
        self.assertIn("El valor base debe ser mayor a 0", str(context.exception))
    
    def test_error_categoria_invalida(self):
        """Prueba de error: Categoría inválida"""
        valor_base = 1000
        categoria_invalida = "Categoria Invalida"
        
        with self.assertRaises(ValueError) as context:
            self.calculadora.calcular_impuestos(valor_base, categoria_invalida)
        
        self.assertIn("Categoría no válida", str(context.exception))

if __name__ == '__main__':
    unittest.main(verbosity=2) 