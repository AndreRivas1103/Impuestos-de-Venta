"""
Test Suite para la Base de Datos - Calculadora de Impuestos
Pruebas para todas las operaciones CRUD con casos normales y de error
"""

import sys
import os
import unittest
import tempfile
import shutil

from database import BaseDatos

class TestBaseDatos(unittest.TestCase):
    """Test suite para la clase BaseDatos"""
    
    def setUp(self):
        """Configuración inicial antes de cada test"""
        # Crear una base de datos temporal para cada test
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_db.db")
        self.db = BaseDatos(self.db_path)
        
        # Crear las tablas
        self.assertTrue(self.db.crear_tablas(), "Error al crear tablas")
    
    def tearDown(self):
        """Limpieza después de cada test"""
        # Eliminar la base de datos temporal
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        shutil.rmtree(self.temp_dir)
    
    # ==================== PRUEBAS PARA CREAR TABLAS ====================
    
    def test_001_crear_tablas_exitoso(self):
        """Test caso normal: Crear tablas correctamente"""
        # Verificar que las tablas se crearon
        self.db.conectar()
        
        # Verificar tabla categorias
        self.db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='categorias'")
        self.assertIsNotNone(self.db.cursor.fetchone())
        
        # Verificar tabla productos
        self.db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='productos'")
        self.assertIsNotNone(self.db.cursor.fetchone())
        
        # Verificar tabla impuestos_adicionales
        self.db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='impuestos_adicionales'")
        self.assertIsNotNone(self.db.cursor.fetchone())
        
        # Verificar tabla transacciones
        self.db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transacciones'")
        self.assertIsNotNone(self.db.cursor.fetchone())
        
        self.db.desconectar()
    
    def test_002_crear_tablas_repetidas(self):
        """Test caso normal: Crear tablas cuando ya existen (no debe fallar)"""
        # Intentar crear las tablas nuevamente
        resultado = self.db.crear_tablas()
        self.assertTrue(resultado, "Crear tablas repetidas debe ser exitoso")
    
    # ==================== PRUEBAS PARA INSERTAR CATEGORÍAS ====================
    
    def test_003_insertar_categoria_exitoso(self):
        """Test caso normal: Insertar categoría correctamente"""
        resultado = self.db.insertar_categoria("Electrónicos", "Dispositivos electrónicos", 0.19)
        self.assertTrue(resultado, "Insertar categoría debe ser exitoso")
        
        # Verificar que se insertó
        categorias = self.db.consultar_todas_categorias()
        self.assertEqual(len(categorias), 1)
        self.assertEqual(categorias[0]['nombre'], "Electrónicos")
        self.assertEqual(categorias[0]['tasa_iva'], 0.19)
    
    def test_004_insertar_categoria_duplicada(self):
        """Test caso de error: Insertar categoría con nombre duplicado"""
        # Insertar primera categoría
        self.assertTrue(self.db.insertar_categoria("Electrónicos", "Dispositivos", 0.19))
        
        # Intentar insertar categoría con mismo nombre
        resultado = self.db.insertar_categoria("Electrónicos", "Otros dispositivos", 0.19)
        self.assertFalse(resultado, "Insertar categoría duplicada debe fallar")
    
    def test_005_insertar_categoria_tasa_invalida(self):
        """Test caso de error: Insertar categoría con tasa de IVA inválida"""
        # Tasa negativa
        resultado = self.db.insertar_categoria("Test", "Descripción", -0.1)
        self.assertFalse(resultado, "Tasa negativa debe fallar")
        
        # Tasa mayor a 1
        resultado = self.db.insertar_categoria("Test", "Descripción", 1.5)
        self.assertFalse(resultado, "Tasa mayor a 1 debe fallar")
    
    # ==================== PRUEBAS PARA INSERTAR PRODUCTOS ====================
    
    def test_006_insertar_producto_exitoso(self):
        """Test caso normal: Insertar producto correctamente"""
        # Primero insertar una categoría
        self.assertTrue(self.db.insertar_categoria("Electrónicos", "Dispositivos", 0.19))
        
        # Insertar producto
        resultado = self.db.insertar_producto("Laptop", 1500000.0, 1, "Laptop para oficina", "Activo")
        self.assertTrue(resultado, "Insertar producto debe ser exitoso")
        
        # Verificar que se insertó
        productos = self.db.consultar_todos_productos()
        self.assertEqual(len(productos), 1)
        self.assertEqual(productos[0]['nombre'], "Laptop")
        self.assertEqual(productos[0]['precio_base'], 1500000.0)
    
    def test_007_insertar_producto_precio_negativo(self):
        """Test caso de error: Insertar producto con precio negativo"""
        # Insertar categoría primero
        self.assertTrue(self.db.insertar_categoria("Electrónicos", "Dispositivos", 0.19))
        
        # Intentar insertar producto con precio negativo
        resultado = self.db.insertar_producto("Laptop", -1000.0, 1, "Descripción", "Activo")
        self.assertFalse(resultado, "Precio negativo debe fallar")
    
    def test_008_insertar_producto_categoria_inexistente(self):
        """Test caso de error: Insertar producto con categoría inexistente"""
        resultado = self.db.insertar_producto("Laptop", 1500000.0, 999, "Descripción", "Activo")
        self.assertFalse(resultado, "Categoría inexistente debe fallar")
    
    def test_009_insertar_producto_estado_invalido(self):
        """Test caso de error: Insertar producto con estado inválido"""
        # Insertar categoría primero
        self.assertTrue(self.db.insertar_categoria("Electrónicos", "Dispositivos", 0.19))
        
        # Intentar insertar producto con estado inválido
        resultado = self.db.insertar_producto("Laptop", 1500000.0, 1, "Descripción", "EstadoInvalido")
        self.assertFalse(resultado, "Estado inválido debe fallar")
    
    # ==================== PRUEBAS PARA INSERTAR IMPUESTOS ADICIONALES ====================
    
    def test_010_insertar_impuesto_adicional_exitoso(self):
        """Test caso normal: Insertar impuesto adicional correctamente"""
        # Insertar categoría primero
        self.assertTrue(self.db.insertar_categoria("Licores", "Bebidas alcohólicas", 0.19))
        
        # Insertar impuesto adicional
        resultado = self.db.insertar_impuesto_adicional("Impuesto Licores", 0.25, "Impuesto especial", 1)
        self.assertTrue(resultado, "Insertar impuesto adicional debe ser exitoso")
    
    def test_011_insertar_impuesto_adicional_tasa_invalida(self):
        """Test caso de error: Insertar impuesto con tasa inválida"""
        # Tasa negativa
        resultado = self.db.insertar_impuesto_adicional("Test", -0.1, "Descripción")
        self.assertFalse(resultado, "Tasa negativa debe fallar")
        
        # Tasa mayor a 1
        resultado = self.db.insertar_impuesto_adicional("Test", 1.5, "Descripción")
        self.assertFalse(resultado, "Tasa mayor a 1 debe fallar")
    
    def test_012_insertar_impuesto_adicional_duplicado(self):
        """Test caso de error: Insertar impuesto con nombre duplicado"""
        # Insertar primer impuesto
        self.assertTrue(self.db.insertar_impuesto_adicional("Impuesto Test", 0.1, "Descripción"))
        
        # Intentar insertar impuesto con mismo nombre
        resultado = self.db.insertar_impuesto_adicional("Impuesto Test", 0.2, "Otra descripción")
        self.assertFalse(resultado, "Nombre duplicado debe fallar")
    
    # ==================== PRUEBAS PARA INSERTAR TRANSACCIONES ====================
    
    def test_013_insertar_transaccion_exitosa(self):
        """Test caso normal: Insertar transacción correctamente"""
        # Insertar categoría y producto
        self.assertTrue(self.db.insertar_categoria("Electrónicos", "Dispositivos", 0.19))
        self.assertTrue(self.db.insertar_producto("Laptop", 1500000.0, 1, "Descripción", "Activo"))
        
        # Insertar transacción
        resultado = self.db.insertar_transaccion(1, 2, 1500000.0, 3000000.0, 570000.0, 3570000.0)
        self.assertTrue(resultado, "Insertar transacción debe ser exitoso")
        
        # Verificar que se insertó
        transacciones = self.db.consultar_transacciones_recientes(1)
        self.assertEqual(len(transacciones), 1)
        self.assertEqual(transacciones[0]['cantidad'], 2)
        self.assertEqual(transacciones[0]['total_final'], 3570000.0)
    
    def test_014_insertar_transaccion_cantidad_negativa(self):
        """Test caso de error: Insertar transacción con cantidad negativa"""
        # Insertar categoría y producto
        self.assertTrue(self.db.insertar_categoria("Electrónicos", "Dispositivos", 0.19))
        self.assertTrue(self.db.insertar_producto("Laptop", 1500000.0, 1, "Descripción", "Activo"))
        
        # Intentar insertar transacción con cantidad negativa
        resultado = self.db.insertar_transaccion(1, -1, 1500000.0, 1500000.0, 285000.0, 1785000.0)
        self.assertFalse(resultado, "Cantidad negativa debe fallar")
    
    def test_015_insertar_transaccion_producto_inexistente(self):
        """Test caso de error: Insertar transacción con producto inexistente"""
        resultado = self.db.insertar_transaccion(999, 1, 1000.0, 1000.0, 190.0, 1190.0)
        self.assertFalse(resultado, "Producto inexistente debe fallar")
    
    # ==================== PRUEBAS PARA ACTUALIZAR PRODUCTOS ====================
    
    def test_016_actualizar_producto_exitoso(self):
        """Test caso normal: Actualizar producto correctamente"""
        # Insertar categoría y producto
        self.assertTrue(self.db.insertar_categoria("Electrónicos", "Dispositivos", 0.19))
        self.assertTrue(self.db.insertar_producto("Laptop", 1500000.0, 1, "Descripción", "Activo"))
        
        # Actualizar producto
        resultado = self.db.actualizar_producto(1, nombre="Laptop Actualizada", precio_base=1600000.0)
        self.assertTrue(resultado, "Actualizar producto debe ser exitoso")
        
        # Verificar cambios
        producto = self.db.consultar_producto_por_id(1)
        self.assertEqual(producto['nombre'], "Laptop Actualizada")
        self.assertEqual(producto['precio_base'], 1600000.0)
    
    def test_017_actualizar_producto_inexistente(self):
        """Test caso de error: Actualizar producto inexistente"""
        resultado = self.db.actualizar_producto(999, nombre="Nuevo Nombre")
        self.assertFalse(resultado, "Actualizar producto inexistente debe fallar")
    
    def test_018_actualizar_producto_precio_negativo(self):
        """Test caso de error: Actualizar producto con precio negativo"""
        # Insertar categoría y producto
        self.assertTrue(self.db.insertar_categoria("Electrónicos", "Dispositivos", 0.19))
        self.assertTrue(self.db.insertar_producto("Laptop", 1500000.0, 1, "Descripción", "Activo"))
        
        # Intentar actualizar con precio negativo
        resultado = self.db.actualizar_producto(1, precio_base=-1000.0)
        self.assertFalse(resultado, "Precio negativo debe fallar")
    
    def test_019_actualizar_producto_sin_cambios(self):
        """Test caso normal: Actualizar producto sin especificar cambios"""
        # Insertar categoría y producto
        self.assertTrue(self.db.insertar_categoria("Electrónicos", "Dispositivos", 0.19))
        self.assertTrue(self.db.insertar_producto("Laptop", 1500000.0, 1, "Descripción", "Activo"))
        
        # Intentar actualizar sin cambios
        resultado = self.db.actualizar_producto(1)
        self.assertFalse(resultado, "Actualizar sin cambios debe fallar")
    
    # ==================== PRUEBAS PARA ACTUALIZAR CATEGORÍAS ====================
    
    def test_020_actualizar_categoria_exitosa(self):
        """Test caso normal: Actualizar categoría correctamente"""
        # Insertar categoría
        self.assertTrue(self.db.insertar_categoria("Electrónicos", "Dispositivos", 0.19))
        
        # Actualizar categoría
        resultado = self.db.actualizar_categoria(1, nombre="Electrónicos Premium", tasa_iva=0.21)
        self.assertTrue(resultado, "Actualizar categoría debe ser exitoso")
        
        # Verificar cambios
        categorias = self.db.consultar_todas_categorias()
        self.assertEqual(categorias[0]['nombre'], "Electrónicos Premium")
        self.assertEqual(categorias[0]['tasa_iva'], 0.21)
    
    def test_021_actualizar_categoria_inexistente(self):
        """Test caso de error: Actualizar categoría inexistente"""
        resultado = self.db.actualizar_categoria(999, nombre="Nueva Categoría")
        self.assertFalse(resultado, "Actualizar categoría inexistente debe fallar")
    
    # ==================== PRUEBAS PARA ELIMINAR PRODUCTOS ====================
    
    def test_022_eliminar_producto_exitoso(self):
        """Test caso normal: Eliminar producto correctamente"""
        # Insertar categoría y producto
        self.assertTrue(self.db.insertar_categoria("Electrónicos", "Dispositivos", 0.19))
        self.assertTrue(self.db.insertar_producto("Laptop", 1500000.0, 1, "Descripción", "Activo"))
        
        # Verificar que existe
        productos = self.db.consultar_todos_productos()
        self.assertEqual(len(productos), 1)
        
        # Eliminar producto
        resultado = self.db.eliminar_producto(1)
        self.assertTrue(resultado, "Eliminar producto debe ser exitoso")
        
        # Verificar que se eliminó
        productos = self.db.consultar_todos_productos()
        self.assertEqual(len(productos), 0)
    
    def test_023_eliminar_producto_inexistente(self):
        """Test caso de error: Eliminar producto inexistente"""
        resultado = self.db.eliminar_producto(999)
        self.assertFalse(resultado, "Eliminar producto inexistente debe fallar")
    
    # ==================== PRUEBAS PARA ELIMINAR CATEGORÍAS ====================
    
    def test_024_eliminar_categoria_exitosa(self):
        """Test caso normal: Eliminar categoría sin productos asociados"""
        # Insertar categoría
        self.assertTrue(self.db.insertar_categoria("Electrónicos", "Dispositivos", 0.19))
        
        # Verificar que existe
        categorias = self.db.consultar_todas_categorias()
        self.assertEqual(len(categorias), 1)
        
        # Eliminar categoría
        resultado = self.db.eliminar_categoria(1)
        self.assertTrue(resultado, "Eliminar categoría debe ser exitoso")
        
        # Verificar que se eliminó
        categorias = self.db.consultar_todas_categorias()
        self.assertEqual(len(categorias), 0)
    
    def test_025_eliminar_categoria_con_productos(self):
        """Test caso de error: Eliminar categoría con productos asociados"""
        # Insertar categoría y producto
        self.assertTrue(self.db.insertar_categoria("Electrónicos", "Dispositivos", 0.19))
        self.assertTrue(self.db.insertar_producto("Laptop", 1500000.0, 1, "Descripción", "Activo"))
        
        # Intentar eliminar categoría con productos
        resultado = self.db.eliminar_categoria(1)
        self.assertFalse(resultado, "Eliminar categoría con productos debe fallar")
    
    def test_026_eliminar_categoria_inexistente(self):
        """Test caso de error: Eliminar categoría inexistente"""
        resultado = self.db.eliminar_categoria(999)
        self.assertFalse(resultado, "Eliminar categoría inexistente debe fallar")
    
    # ==================== PRUEBAS PARA CONSULTAR PRODUCTOS ====================
    
    def test_027_consultar_todos_productos_vacio(self):
        """Test caso normal: Consultar productos cuando no hay ninguno"""
        productos = self.db.consultar_todos_productos()
        self.assertEqual(len(productos), 0)
    
    def test_028_consultar_todos_productos_con_datos(self):
        """Test caso normal: Consultar todos los productos con datos"""
        # Insertar categoría y productos
        self.assertTrue(self.db.insertar_categoria("Electrónicos", "Dispositivos", 0.19))
        self.assertTrue(self.db.insertar_producto("Laptop", 1500000.0, 1, "Descripción 1", "Activo"))
        self.assertTrue(self.db.insertar_producto("Mouse", 50000.0, 1, "Descripción 2", "Activo"))
        
        # Consultar productos
        productos = self.db.consultar_todos_productos()
        self.assertEqual(len(productos), 2)
        self.assertEqual(productos[0]['categoria_nombre'], "Electrónicos")
        self.assertEqual(productos[1]['categoria_nombre'], "Electrónicos")
    
    def test_029_consultar_producto_por_id_exitoso(self):
        """Test caso normal: Consultar producto por ID existente"""
        # Insertar categoría y producto
        self.assertTrue(self.db.insertar_categoria("Electrónicos", "Dispositivos", 0.19))
        self.assertTrue(self.db.insertar_producto("Laptop", 1500000.0, 1, "Descripción", "Activo"))
        
        # Consultar producto
        producto = self.db.consultar_producto_por_id(1)
        self.assertIsNotNone(producto)
        self.assertEqual(producto['nombre'], "Laptop")
        self.assertEqual(producto['precio_base'], 1500000.0)
    
    def test_030_consultar_producto_por_id_inexistente(self):
        """Test caso normal: Consultar producto por ID inexistente"""
        producto = self.db.consultar_producto_por_id(999)
        self.assertIsNone(producto)
    
    def test_031_consultar_productos_por_categoria(self):
        """Test caso normal: Consultar productos por categoría"""
        # Insertar categorías y productos
        self.assertTrue(self.db.insertar_categoria("Electrónicos", "Dispositivos", 0.19))
        self.assertTrue(self.db.insertar_categoria("Alimentos", "Comida", 0.05))
        
        self.assertTrue(self.db.insertar_producto("Laptop", 1500000.0, 1, "Descripción", "Activo"))
        self.assertTrue(self.db.insertar_producto("Mouse", 50000.0, 1, "Descripción", "Activo"))
        self.assertTrue(self.db.insertar_producto("Arroz", 2500.0, 2, "Descripción", "Activo"))
        
        # Consultar productos de categoría 1
        productos_cat1 = self.db.consultar_productos_por_categoria(1)
        self.assertEqual(len(productos_cat1), 2)
        
        # Consultar productos de categoría 2
        productos_cat2 = self.db.consultar_productos_por_categoria(2)
        self.assertEqual(len(productos_cat2), 1)
    
    # ==================== PRUEBAS PARA CONSULTAR CATEGORÍAS ====================
    
    def test_032_consultar_todas_categorias_vacio(self):
        """Test caso normal: Consultar categorías cuando no hay ninguna"""
        categorias = self.db.consultar_todas_categorias()
        self.assertEqual(len(categorias), 0)
    
    def test_033_consultar_todas_categorias_con_datos(self):
        """Test caso normal: Consultar todas las categorías con datos"""
        # Insertar categorías
        self.assertTrue(self.db.insertar_categoria("Electrónicos", "Dispositivos", 0.19))
        self.assertTrue(self.db.insertar_categoria("Alimentos", "Comida", 0.05))
        
        # Consultar categorías
        categorias = self.db.consultar_todas_categorias()
        self.assertEqual(len(categorias), 2)
        self.assertEqual(categorias[0]['nombre'], "Alimentos")  # Ordenado alfabéticamente
        self.assertEqual(categorias[1]['nombre'], "Electrónicos")
    
    # ==================== PRUEBAS PARA CONSULTAR TRANSACCIONES ====================
    
    def test_034_consultar_transacciones_recientes_vacio(self):
        """Test caso normal: Consultar transacciones cuando no hay ninguna"""
        transacciones = self.db.consultar_transacciones_recientes()
        self.assertEqual(len(transacciones), 0)
    
    def test_035_consultar_transacciones_recientes_con_datos(self):
        """Test caso normal: Consultar transacciones recientes con datos"""
        # Insertar categoría, producto y transacciones
        self.assertTrue(self.db.insertar_categoria("Electrónicos", "Dispositivos", 0.19))
        self.assertTrue(self.db.insertar_producto("Laptop", 1500000.0, 1, "Descripción", "Activo"))
        
        self.assertTrue(self.db.insertar_transaccion(1, 1, 1500000.0, 1500000.0, 285000.0, 1785000.0))
        self.assertTrue(self.db.insertar_transaccion(1, 2, 1500000.0, 3000000.0, 570000.0, 3570000.0))
        
        # Consultar transacciones
        transacciones = self.db.consultar_transacciones_recientes(5)
        self.assertEqual(len(transacciones), 2)
        self.assertEqual(transacciones[0]['cantidad'], 2)  # La más reciente primero
        self.assertEqual(transacciones[1]['cantidad'], 1)
    
    # ==================== PRUEBAS PARA ESTADÍSTICAS ====================
    
    def test_036_obtener_estadisticas_vacio(self):
        """Test caso normal: Obtener estadísticas con base de datos vacía"""
        estadisticas = self.db.obtener_estadisticas()
        
        self.assertEqual(estadisticas['total_categorias'], 0)
        self.assertEqual(estadisticas['total_productos'], 0)
        self.assertEqual(estadisticas['total_transacciones'], 0)
        self.assertEqual(estadisticas['valor_total_ventas'], 0)
        self.assertEqual(len(estadisticas['productos_por_estado']), 0)
    
    def test_037_obtener_estadisticas_con_datos(self):
        """Test caso normal: Obtener estadísticas con datos"""
        # Insertar datos de prueba
        self.assertTrue(self.db.insertar_categoria("Electrónicos", "Dispositivos", 0.19))
        self.assertTrue(self.db.insertar_categoria("Alimentos", "Comida", 0.05))
        
        self.assertTrue(self.db.insertar_producto("Laptop", 1500000.0, 1, "Descripción", "Activo"))
        self.assertTrue(self.db.insertar_producto("Mouse", 50000.0, 1, "Descripción", "Inactivo"))
        self.assertTrue(self.db.insertar_producto("Arroz", 2500.0, 2, "Descripción", "Activo"))
        
        self.assertTrue(self.db.insertar_transaccion(1, 1, 1500000.0, 1500000.0, 285000.0, 1785000.0))
        self.assertTrue(self.db.insertar_transaccion(3, 2, 2500.0, 5000.0, 250.0, 5250.0))
        
        # Obtener estadísticas
        estadisticas = self.db.obtener_estadisticas()
        
        self.assertEqual(estadisticas['total_categorias'], 2)
        self.assertEqual(estadisticas['total_productos'], 3)
        self.assertEqual(estadisticas['total_transacciones'], 2)
        self.assertEqual(estadisticas['valor_total_ventas'], 1790250.0)  # 1785000 + 5250
        self.assertEqual(estadisticas['productos_por_estado']['Activo'], 2)
        self.assertEqual(estadisticas['productos_por_estado']['Inactivo'], 1)
    
    # ==================== PRUEBAS PARA INICIALIZAR DATOS DE EJEMPLO ====================
    
    def test_038_inicializar_datos_ejemplo_exitoso(self):
        """Test caso normal: Inicializar datos de ejemplo correctamente"""
        resultado = self.db.inicializar_datos_ejemplo()
        self.assertTrue(resultado, "Inicializar datos de ejemplo debe ser exitoso")
        
        # Verificar que se insertaron los datos
        categorias = self.db.consultar_todas_categorias()
        self.assertEqual(len(categorias), 6)  # 6 categorías de ejemplo
        
        productos = self.db.consultar_todos_productos()
        self.assertEqual(len(productos), 6)  # 6 productos de ejemplo
        
        # Verificar algunas categorías específicas
        nombres_categorias = [cat['nombre'] for cat in categorias]
        self.assertIn("Alimentos Básicos", nombres_categorias)
        self.assertIn("Licores", nombres_categorias)
        self.assertIn("Servicios Públicos", nombres_categorias)
    
    def test_039_inicializar_datos_ejemplo_repetido(self):
        """Test caso de error: Inicializar datos de ejemplo cuando ya existen"""
        # Primera inicialización
        self.assertTrue(self.db.inicializar_datos_ejemplo())
        
        # Segunda inicialización debe fallar por duplicados
        resultado = self.db.inicializar_datos_ejemplo()
        self.assertFalse(resultado, "Inicializar datos duplicados debe fallar")
    
    # ==================== PRUEBAS DE INTEGRACIÓN ====================
    
    def test_040_flujo_completo_crud(self):
        """Test caso normal: Flujo completo CRUD"""
        # CREATE - Crear categoría
        self.assertTrue(self.db.insertar_categoria("Test", "Categoría de prueba", 0.19))
        
        # CREATE - Crear producto
        self.assertTrue(self.db.insertar_producto("Producto Test", 1000.0, 1, "Descripción", "Activo"))
        
        # READ - Consultar producto
        producto = self.db.consultar_producto_por_id(1)
        self.assertIsNotNone(producto)
        self.assertEqual(producto['nombre'], "Producto Test")
        
        # UPDATE - Actualizar producto
        self.assertTrue(self.db.actualizar_producto(1, nombre="Producto Actualizado", precio_base=1500.0))
        
        # READ - Verificar actualización
        producto_actualizado = self.db.consultar_producto_por_id(1)
        self.assertEqual(producto_actualizado['nombre'], "Producto Actualizado")
        self.assertEqual(producto_actualizado['precio_base'], 1500.0)
        
        # CREATE - Crear transacción
        self.assertTrue(self.db.insertar_transaccion(1, 2, 1500.0, 3000.0, 570.0, 3570.0))
        
        # READ - Consultar transacciones
        transacciones = self.db.consultar_transacciones_recientes(1)
        self.assertEqual(len(transacciones), 1)
        self.assertEqual(transacciones[0]['total_final'], 3570.0)
        
        # NOTA: No podemos eliminar el producto porque tiene transacciones asociadas
        # Esto es el comportamiento correcto del sistema
        
        # DELETE - Intentar eliminar producto (debe fallar por transacciones asociadas)
        resultado_eliminar = self.db.eliminar_producto(1)
        self.assertFalse(resultado_eliminar, "No se debe poder eliminar producto con transacciones")
        
        # READ - Verificar que el producto sigue existiendo
        productos = self.db.consultar_todos_productos()
        self.assertEqual(len(productos), 1)
        
        # DELETE - Eliminar categoría (debe fallar por productos asociados)
        resultado_eliminar_cat = self.db.eliminar_categoria(1)
        self.assertFalse(resultado_eliminar_cat, "No se debe poder eliminar categoría con productos")
        
        # READ - Verificar que la categoría sigue existiendo
        categorias = self.db.consultar_todas_categorias()
        self.assertEqual(len(categorias), 1)


if __name__ == '__main__':
    # Configurar el runner de tests para mostrar información detallada
    unittest.main(verbosity=2, buffer=True)
