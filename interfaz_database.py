
import sys
import os
from typing import List, Dict, Optional

from database import BaseDatos
from calculadora_impuestos import CalculadoraImpuestos, CategoriaProducto

class InterfazDatabase:
    """Interfaz de consola para gestionar la base de datos de productos e impuestos"""
    
    def __init__(self):
        """Inicializa la interfaz con la base de datos y calculadora"""
        self.db = BaseDatos("calculadora_impuestos.db")
        self.calculadora = CalculadoraImpuestos()
        self.inicializar_sistema()
    
    def inicializar_sistema(self):
        """Inicializa el sistema creando tablas y datos de ejemplo si es necesario"""
        print("🔧 Inicializando sistema de base de datos...")
        
        # Crear tablas
        if not self.db.crear_tablas():
            print("Error al crear las tablas de la base de datos")
            return False
        
        # Verificar si ya hay datos
        categorias = self.db.consultar_todas_categorias()
        if len(categorias) == 0:
            print("Insertando datos de ejemplo...")
            if self.db.inicializar_datos_ejemplo():
                print("Datos de ejemplo insertados correctamente")
            else:
                print("Error al insertar datos de ejemplo")
        
        print("Sistema inicializado correctamente")
        return True
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal de la aplicación"""
        print("\n" + "="*60)
        print("GESTIÓN DE PRODUCTOS E IMPUESTOS - BASE DE DATOS")
        print("="*60)
        print("1. Gestionar Productos")
        print("2. Gestionar Categorías")
        print("3. Gestionar Transacciones")
        print("4. Ver Estadísticas")
        print("5. Calculadora de Impuestos")
        print("6. Consultas Avanzadas")
        print("0. Salir")
        print("-"*60)
    
    def mostrar_menu_productos(self):
        """Muestra el menú de gestión de productos"""
        print("\n" + "="*40)
        print("GESTIÓN DE PRODUCTOS")
        print("="*40)
        print("1. Agregar Producto")
        print("2. Listar Todos los Productos")
        print("3. Buscar Producto por ID")
        print("4. Actualizar Producto")
        print("5. Eliminar Producto")
        print("6. Productos por Categoría")
        print("0. ⬅Volver al Menú Principal")
        print("-"*40)
    
    def mostrar_menu_categorias(self):
        """Muestra el menú de gestión de categorías"""
        print("\n" + "="*40)
        print("GESTIÓN DE CATEGORÍAS")
        print("="*40)
        print("1. Agregar Categoría")
        print("2. Listar Todas las Categorías")
        print("3. Actualizar Categoría")
        print("4. Eliminar Categoría")
        print("0. ⬅Volver al Menú Principal")
        print("-"*40)
    
    def mostrar_menu_transacciones(self):
        """Muestra el menú de gestión de transacciones"""
        print("\n" + "="*40)
        print("GESTIÓN DE TRANSACCIONES")
        print("="*40)
        print("1. Registrar Nueva Venta")
        print("2. Ver Transacciones Recientes")
        print("3. Calcular Impuestos para Venta")
        print("0. ⬅Volver al Menú Principal")
        print("-"*40)
    
    def ejecutar(self):
        """Ejecuta la interfaz principal"""
        try:
            while True:
                self.mostrar_menu_principal()
                opcion = input("Seleccione una opción: ").strip()
                
                if opcion == "1":
                    self.gestionar_productos()
                elif opcion == "2":
                    self.gestionar_categorias()
                elif opcion == "3":
                    self.gestionar_transacciones()
                elif opcion == "4":
                    self.mostrar_estadisticas()
                elif opcion == "5":
                    self.calculadora_impuestos()
                elif opcion == "6":
                    self.consultas_avanzadas()
                elif opcion == "0":
                    print("\n¡Hasta luego! Gracias por usar el sistema.")
                    break
                else:
                    print("Opción inválida. Por favor, seleccione una opción válida.")
        
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego! Gracias por usar el sistema.")
        except Exception as e:
            print(f"\nError inesperado: {e}")
    
    def gestionar_productos(self):
        """Gestiona las operaciones CRUD de productos"""
        while True:
            self.mostrar_menu_productos()
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                self.agregar_producto()
            elif opcion == "2":
                self.listar_productos()
            elif opcion == "3":
                self.buscar_producto_por_id()
            elif opcion == "4":
                self.actualizar_producto()
            elif opcion == "5":
                self.eliminar_producto()
            elif opcion == "6":
                self.productos_por_categoria()
            elif opcion == "0":
                break
            else:
                print("Opción inválida.")
    
    def gestionar_categorias(self):
        """Gestiona las operaciones CRUD de categorías"""
        while True:
            self.mostrar_menu_categorias()
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                self.agregar_categoria()
            elif opcion == "2":
                self.listar_categorias()
            elif opcion == "3":
                self.actualizar_categoria()
            elif opcion == "4":
                self.eliminar_categoria()
            elif opcion == "0":
                break
            else:
                print("Opción inválida.")
    
    def gestionar_transacciones(self):
        """Gestiona las operaciones de transacciones"""
        while True:
            self.mostrar_menu_transacciones()
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                self.registrar_venta()
            elif opcion == "2":
                self.ver_transacciones_recientes()
            elif opcion == "3":
                self.calcular_impuestos_venta()
            elif opcion == "0":
                break
            else:
                print("Opción inválida.")
    
    def agregar_producto(self):
        """Agrega un nuevo producto a la base de datos"""
        print("\nAGREGAR NUEVO PRODUCTO")
        print("-" * 30)
        
        # Mostrar categorías disponibles
        categorias = self.db.consultar_todas_categorias()
        if not categorias:
            print("No hay categorías disponibles. Primero agregue una categoría.")
            return
        
        print("📂 Categorías disponibles:")
        for cat in categorias:
            print(f"   {cat['id']}. {cat['nombre']} (IVA: {cat['tasa_iva']*100:.0f}%)")
        
        try:
            nombre = input("Nombre del producto: ").strip()
            if not nombre:
                print("El nombre es obligatorio.")
                return
            
            descripcion = input("Descripción (opcional): ").strip()
            
            precio_base = float(input("Precio base: $"))
            if precio_base <= 0:
                print("El precio debe ser mayor a 0.")
                return
            
            categoria_id = int(input("ID de la categoría: "))
            
            # Verificar que la categoría existe
            categoria_existe = any(cat['id'] == categoria_id for cat in categorias)
            if not categoria_existe:
                print("La categoría seleccionada no existe.")
                return
            
            estado = input("Estado (Activo/Inactivo/Descontinuado) [Activo]: ").strip()
            if not estado:
                estado = "Activo"
            
            if estado not in ["Activo", "Inactivo", "Descontinuado"]:
                print("Estado inválido.")
                return
            
            # Insertar producto
            if self.db.insertar_producto(nombre, precio_base, categoria_id, descripcion, estado):
                print("Producto agregado correctamente.")
            else:
                print("Error al agregar el producto.")
        
        except ValueError:
            print("Error en los datos ingresados. Verifique que el precio y ID sean números válidos.")
        except Exception as e:
            print(f"Error inesperado: {e}")
    
    def listar_productos(self):
        """Lista todos los productos"""
        print("\nLISTA DE PRODUCTOS")
        print("-" * 50)
        
        productos = self.db.consultar_todos_productos()
        if not productos:
            print("No hay productos registrados.")
            return
        
        print(f"{'ID':<3} {'Nombre':<20} {'Precio':<12} {'Categoría':<15} {'Estado':<12}")
        print("-" * 70)
        
        for producto in productos:
            print(f"{producto['id']:<3} {producto['nombre']:<20} "
                  f"${producto['precio_base']:>10,.0f} {producto['categoria_nombre']:<15} "
                  f"{producto['estado']:<12}")
    
    def buscar_producto_por_id(self):
        """Busca un producto por su ID"""
        print("\nBUSCAR PRODUCTO POR ID")
        print("-" * 30)
        
        try:
            producto_id = int(input("Ingrese el ID del producto: "))
            producto = self.db.consultar_producto_por_id(producto_id)
            
            if producto:
                print(f"\nINFORMACIÓN DEL PRODUCTO")
                print("-" * 30)
                print(f"ID: {producto['id']}")
                print(f"Nombre: {producto['nombre']}")
                print(f"Descripción: {producto['descripcion']}")
                print(f"Precio Base: ${producto['precio_base']:,.2f}")
                print(f"Categoría: {producto['categoria_nombre']}")
                print(f"IVA: {producto['tasa_iva']*100:.0f}%")
                print(f"Estado: {producto['estado']}")
                print(f"Fecha Creación: {producto['fecha_creacion']}")
            else:
                print("Producto no encontrado.")
        
        except ValueError:
            print("ID inválido. Debe ser un número.")
    
    def actualizar_producto(self):
        """Actualiza un producto existente"""
        print("\nACTUALIZAR PRODUCTO")
        print("-" * 30)
        
        try:
            producto_id = int(input("Ingrese el ID del producto a actualizar: "))
            producto = self.db.consultar_producto_por_id(producto_id)
            
            if not producto:
                print("Producto no encontrado.")
                return
            
            print(f"\nProducto actual: {producto['nombre']}")
            print("Deje en blanco los campos que no desea cambiar.")
            
            # Obtener nuevos valores
            nuevo_nombre = input(f"Nombre actual ({producto['nombre']}): ").strip()
            if not nuevo_nombre:
                nuevo_nombre = None
            
            nueva_descripcion = input(f"Descripción actual ({producto['descripcion']}): ").strip()
            if not nueva_descripcion:
                nueva_descripcion = None
            
            nuevo_precio_str = input(f"Precio actual (${producto['precio_base']:,.2f}): ").strip()
            nuevo_precio = None
            if nuevo_precio_str:
                nuevo_precio = float(nuevo_precio_str)
                if nuevo_precio <= 0:
                    print("El precio debe ser mayor a 0.")
                    return
            
            nuevo_estado = input(f"Estado actual ({producto['estado']}): ").strip()
            if not nuevo_estado:
                nuevo_estado = None
            elif nuevo_estado not in ["Activo", "Inactivo", "Descontinuado"]:
                print("Estado inválido.")
                return
            
            # Actualizar producto
            if self.db.actualizar_producto(producto_id, nuevo_nombre, nuevo_precio, 
                                         None, nueva_descripcion, nuevo_estado):
                print("Producto actualizado correctamente.")
            else:
                print("Error al actualizar el producto.")
        
        except ValueError:
            print("Error en los datos ingresados.")
    
    def eliminar_producto(self):
        """Elimina un producto"""
        print("\nELIMINAR PRODUCTO")
        print("-" * 30)
        
        try:
            producto_id = int(input("Ingrese el ID del producto a eliminar: "))
            producto = self.db.consultar_producto_por_id(producto_id)
            
            if not producto:
                print("Producto no encontrado.")
                return
            
            print(f"\n¿Está seguro de eliminar el producto '{producto['nombre']}'?")
            confirmacion = input("Escriba 'SI' para confirmar: ").strip()
            
            if confirmacion.upper() == "SI":
                if self.db.eliminar_producto(producto_id):
                    print("Producto eliminado correctamente.")
                else:
                    print("Error al eliminar el producto.")
            else:
                print("Eliminación cancelada.")
        
        except ValueError:
            print("ID inválido. Debe ser un número.")
    
    def productos_por_categoria(self):
        """Muestra productos agrupados por categoría"""
        print("\nPRODUCTOS POR CATEGORÍA")
        print("-" * 40)
        
        categorias = self.db.consultar_todas_categorias()
        if not categorias:
            print("No hay categorías registradas.")
            return
        
        for categoria in categorias:
            productos = self.db.consultar_productos_por_categoria(categoria['id'])
            print(f"\n{categoria['nombre']} (IVA: {categoria['tasa_iva']*100:.0f}%)")
            print("-" * 40)
            
            if productos:
                for producto in productos:
                    print(f"  • {producto['nombre']} - ${producto['precio_base']:,.2f} ({producto['estado']})")
            else:
                print("  📭 No hay productos en esta categoría.")
    
    def agregar_categoria(self):
        """Agrega una nueva categoría"""
        print("\nAGREGAR NUEVA CATEGORÍA")
        print("-" * 35)
        
        try:
            nombre = input("Nombre de la categoría: ").strip()
            if not nombre:
                print("El nombre es obligatorio.")
                return
            
            descripcion = input("Descripción (opcional): ").strip()
            
            tasa_iva = float(input("Tasa de IVA (0.0 a 1.0) [0.19]: ").strip() or "0.19")
            if tasa_iva < 0 or tasa_iva > 1:
                print("La tasa de IVA debe estar entre 0.0 y 1.0.")
                return
            
            if self.db.insertar_categoria(nombre, descripcion, tasa_iva):
                print("Categoría agregada correctamente.")
            else:
                print("Error al agregar la categoría.")
        
        except ValueError:
            print("Error en los datos ingresados. Verifique que la tasa sea un número válido.")
    
    def listar_categorias(self):
        """Lista todas las categorías"""
        print("\nLISTA DE CATEGORÍAS")
        print("-" * 40)
        
        categorias = self.db.consultar_todas_categorias()
        if not categorias:
            print("No hay categorías registradas.")
            return
        
        print(f"{'ID':<3} {'Nombre':<20} {'IVA':<8} {'Descripción':<30}")
        print("-" * 70)
        
        for categoria in categorias:
            descripcion = categoria['descripcion'][:27] + "..." if len(categoria['descripcion']) > 30 else categoria['descripcion']
            print(f"{categoria['id']:<3} {categoria['nombre']:<20} "
                  f"{categoria['tasa_iva']*100:>5.0f}% {descripcion:<30}")
    
    def actualizar_categoria(self):
        """Actualiza una categoría existente"""
        print("\nACTUALIZAR CATEGORÍA")
        print("-" * 30)
        
        try:
            categoria_id = int(input("Ingrese el ID de la categoría a actualizar: "))
            
            # Buscar la categoría
            categorias = self.db.consultar_todas_categorias()
            categoria = next((cat for cat in categorias if cat['id'] == categoria_id), None)
            
            if not categoria:
                print("Categoría no encontrada.")
                return
            
            print(f"\nCategoría actual: {categoria['nombre']}")
            print("Deje en blanco los campos que no desea cambiar.")
            
            nuevo_nombre = input(f"Nombre actual ({categoria['nombre']}): ").strip()
            if not nuevo_nombre:
                nuevo_nombre = None
            
            nueva_descripcion = input(f"Descripción actual ({categoria['descripcion']}): ").strip()
            if not nueva_descripcion:
                nueva_descripcion = None
            
            nueva_tasa_str = input(f"Tasa IVA actual ({categoria['tasa_iva']*100:.0f}%): ").strip()
            nueva_tasa = None
            if nueva_tasa_str:
                nueva_tasa = float(nueva_tasa_str) / 100
                if nueva_tasa < 0 or nueva_tasa > 1:
                    print("La tasa debe estar entre 0% y 100%.")
                    return
            
            if self.db.actualizar_categoria(categoria_id, nuevo_nombre, nueva_descripcion, nueva_tasa):
                print("Categoría actualizada correctamente.")
            else:
                print("Error al actualizar la categoría.")
        
        except ValueError:
            print("Error en los datos ingresados.")
    
    def eliminar_categoria(self):
        """Elimina una categoría"""
        print("\nELIMINAR CATEGORÍA")
        print("-" * 30)
        
        try:
            categoria_id = int(input("Ingrese el ID de la categoría a eliminar: "))
            
            # Buscar la categoría
            categorias = self.db.consultar_todas_categorias()
            categoria = next((cat for cat in categorias if cat['id'] == categoria_id), None)
            
            if not categoria:
                print("Categoría no encontrada.")
                return
            
            print(f"\n¿Está seguro de eliminar la categoría '{categoria['nombre']}'?")
            print("Esta acción eliminará todos los productos asociados.")
            confirmacion = input("Escriba 'SI' para confirmar: ").strip()
            
            if confirmacion.upper() == "SI":
                if self.db.eliminar_categoria(categoria_id):
                    print("Categoría eliminada correctamente.")
                else:
                    print("Error al eliminar la categoría.")
            else:
                print("Eliminación cancelada.")
        
        except ValueError:
            print("ID inválido. Debe ser un número.")
    
    def registrar_venta(self):
        """Registra una nueva venta/transacción"""
        print("\nREGISTRAR NUEVA VENTA")
        print("-" * 30)
        
        # Mostrar productos disponibles
        productos = self.db.consultar_todos_productos()
        productos_activos = [p for p in productos if p['estado'] == 'Activo']
        
        if not productos_activos:
            print("No hay productos activos disponibles.")
            return
        
        print("Productos disponibles:")
        for producto in productos_activos:
            print(f"   {producto['id']}. {producto['nombre']} - ${producto['precio_base']:,.2f}")
        
        try:
            producto_id = int(input("\nID del producto: "))
            producto = next((p for p in productos_activos if p['id'] == producto_id), None)
            
            if not producto:
                print("Producto no encontrado o no está activo.")
                return
            
            cantidad = int(input("Cantidad: "))
            if cantidad <= 0:
                print("La cantidad debe ser mayor a 0.")
                return
            
            # Calcular impuestos usando la calculadora
            precio_unitario = producto['precio_base']
            subtotal = precio_unitario * cantidad
            
            # Mapear categoría de la BD a enum de la calculadora
            categoria_nombre = producto['categoria_nombre']
            categoria_enum = self.mapear_categoria_a_enum(categoria_nombre)
            
            if categoria_enum:
                resultado_impuestos = self.calculadora.calcular_impuestos(precio_unitario, categoria_enum)
                total_impuestos = resultado_impuestos['total_impuestos'] * cantidad
                total_final = subtotal + total_impuestos
                
                # Mostrar resumen
                print(f"\n📊 RESUMEN DE LA VENTA")
                print("-" * 30)
                print(f"Producto: {producto['nombre']}")
                print(f"Cantidad: {cantidad}")
                print(f"Precio unitario: ${precio_unitario:,.2f}")
                print(f"Subtotal: ${subtotal:,.2f}")
                print(f"Impuestos: ${total_impuestos:,.2f}")
                print(f"Total: ${total_final:,.2f}")
                
                confirmar = input("\n¿Confirmar venta? (s/n): ").strip().lower()
                if confirmar == 's':
                    if self.db.insertar_transaccion(producto_id, cantidad, precio_unitario, 
                                                  subtotal, total_impuestos, total_final):
                        print("Venta registrada correctamente.")
                    else:
                        print("Error al registrar la venta.")
                else:
                    print("Venta cancelada.")
            else:
                print("No se pudo calcular los impuestos para esta categoría.")
        
        except ValueError:
            print("Error en los datos ingresados.")
    
    def ver_transacciones_recientes(self):
        """Muestra las transacciones más recientes"""
        print("\nTRANSACCIONES RECIENTES")
        print("-" * 50)
        
        try:
            limite = int(input("Número de transacciones a mostrar [10]: ").strip() or "10")
            transacciones = self.db.consultar_transacciones_recientes(limite)
            
            if not transacciones:
                print("No hay transacciones registradas.")
                return
            
            print(f"{'ID':<3} {'Producto':<20} {'Cant.':<5} {'Total':<12} {'Fecha':<20}")
            print("-" * 70)
            
            for trans in transacciones:
                fecha = trans['fecha_transaccion'][:19]  # Truncar milisegundos
                print(f"{trans['id']:<3} {trans['producto_nombre']:<20} "
                      f"{trans['cantidad']:<5} ${trans['total_final']:>10,.0f} {fecha:<20}")
        
        except ValueError:
            print("Número inválido.")
    
    def calcular_impuestos_venta(self):
        """Calcula impuestos para una venta específica"""
        print("\nCALCULADORA DE IMPUESTOS")
        print("-" * 35)
        
        try:
            valor_base = float(input("Valor base del producto: $"))
            if valor_base <= 0:
                print("El valor debe ser mayor a 0.")
                return
            
            print("\nCategorías disponibles:")
            categorias = self.calculadora.obtener_categorias_disponibles()
            for i, categoria in enumerate(categorias, 1):
                print(f"   {i}. {categoria}")
            
            categoria_idx = int(input("Seleccione la categoría (número): ")) - 1
            if categoria_idx < 0 or categoria_idx >= len(categorias):
                print("Categoría inválida.")
                return
            
            categoria_nombre = categorias[categoria_idx]
            categoria_enum = self.mapear_categoria_a_enum(categoria_nombre)
            
            if categoria_enum:
                resultado = self.calculadora.calcular_impuestos(valor_base, categoria_enum)
                
                print(f"\nCÁLCULO DE IMPUESTOS")
                print("-" * 30)
                print(f"Valor base: ${resultado['valor_base']:,.2f}")
                print(f"Categoría: {resultado['categoria']}")
                print(f"\nDesglose de impuestos:")
                for impuesto, valor in resultado['impuestos'].items():
                    if valor > 0:
                        print(f"  • {impuesto}: ${valor:,.2f}")
                print(f"\nTotal impuestos: ${resultado['total_impuestos']:,.2f}")
                print(f"Valor total: ${resultado['valor_total']:,.2f}")
            else:
                print("Categoría no válida.")
        
        except ValueError:
            print("Error en los datos ingresados.")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas generales del sistema"""
        print("\nESTADÍSTICAS DEL SISTEMA")
        print("-" * 40)
        
        estadisticas = self.db.obtener_estadisticas()
        
        print(f"Total de categorías: {estadisticas['total_categorias']}")
        print(f"Total de productos: {estadisticas['total_productos']}")
        print(f"Total de transacciones: {estadisticas['total_transacciones']}")
        print(f"Valor total de ventas: ${estadisticas['valor_total_ventas']:,.2f}")
        
        if estadisticas['productos_por_estado']:
            print(f"\nProductos por estado:")
            for estado, cantidad in estadisticas['productos_por_estado'].items():
                print(f"  • {estado}: {cantidad}")
    
    def calculadora_impuestos(self):
        """Interfaz de la calculadora de impuestos original"""
        print("\nCALCULADORA DE IMPUESTOS")
        print("-" * 35)
        
        try:
            valor_base = float(input("Ingrese el valor base del producto: $"))
            if valor_base <= 0:
                print("El valor debe ser mayor a 0.")
                return
            
            print("\nCategorías disponibles:")
            categorias = self.calculadora.obtener_categorias_disponibles()
            for i, categoria in enumerate(categorias, 1):
                print(f"   {i}. {categoria}")
            
            categoria_idx = int(input("Seleccione la categoría (número): ")) - 1
            if categoria_idx < 0 or categoria_idx >= len(categorias):
                print("Categoría inválida.")
                return
            
            categoria_nombre = categorias[categoria_idx]
            categoria_enum = self.mapear_categoria_a_enum(categoria_nombre)
            
            if categoria_enum:
                resultado = self.calculadora.calcular_impuestos(valor_base, categoria_enum)
                
                print(f"\nRESULTADO DEL CÁLCULO")
                print("=" * 40)
                print(f"Valor base: ${resultado['valor_base']:,.2f}")
                print(f"Categoría: {resultado['categoria']}")
                print(f"\nDesglose de impuestos:")
                for impuesto, valor in resultado['impuestos'].items():
                    if valor > 0:
                        print(f"  • {impuesto}: ${valor:,.2f}")
                print(f"\nTotal impuestos: ${resultado['total_impuestos']:,.2f}")
                print(f"Valor total: ${resultado['valor_total']:,.2f}")
            else:
                print("Categoría no válida.")
        
        except ValueError:
            print("Error en los datos ingresados.")
        except Exception as e:
            print(f"Error inesperado: {e}")
    
    def consultas_avanzadas(self):
        """Muestra opciones de consultas avanzadas"""
        print("\nCONSULTAS AVANZADAS")
        print("-" * 30)
        print("1. Productos más caros")
        print("2. Productos más baratos")
        print("3. Ventas por categoría")
        print("4. Productos por estado")
        print("0. ⬅Volver al menú principal")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            self.productos_mas_caros()
        elif opcion == "2":
            self.productos_mas_baratos()
        elif opcion == "3":
            self.ventas_por_categoria()
        elif opcion == "4":
            self.productos_por_estado()
        elif opcion == "0":
            return
        else:
            print("Opción inválida.")
    
    def productos_mas_caros(self):
        """Muestra los productos más caros"""
        print("\nPRODUCTOS MÁS CAROS")
        print("-" * 30)
        
        productos = self.db.consultar_todos_productos()
        if not productos:
            print("No hay productos registrados.")
            return
        
        # Ordenar por precio descendente
        productos_ordenados = sorted(productos, key=lambda x: x['precio_base'], reverse=True)
        
        print("Top 5 productos más caros:")
        for i, producto in enumerate(productos_ordenados[:5], 1):
            print(f"{i}. {producto['nombre']} - ${producto['precio_base']:,.2f}")
    
    def productos_mas_baratos(self):
        """Muestra los productos más baratos"""
        print("\nPRODUCTOS MÁS BARATOS")
        print("-" * 30)
        
        productos = self.db.consultar_todos_productos()
        if not productos:
            print("No hay productos registrados.")
            return
        
        # Ordenar por precio ascendente
        productos_ordenados = sorted(productos, key=lambda x: x['precio_base'])
        
        print("Top 5 productos más baratos:")
        for i, producto in enumerate(productos_ordenados[:5], 1):
            print(f"{i}. {producto['nombre']} - ${producto['precio_base']:,.2f}")
    
    def ventas_por_categoria(self):
        """Muestra resumen de ventas por categoría"""
        print("\nVENTAS POR CATEGORÍA")
        print("-" * 30)
        
        transacciones = self.db.consultar_transacciones_recientes(1000)  # Obtener muchas transacciones
        if not transacciones:
            print("No hay transacciones registradas.")
            return
        
        # Agrupar por categoría
        ventas_por_categoria = {}
        for trans in transacciones:
            categoria = trans['categoria_nombre']
            if categoria not in ventas_por_categoria:
                ventas_por_categoria[categoria] = {'cantidad': 0, 'total': 0}
            ventas_por_categoria[categoria]['cantidad'] += trans['cantidad']
            ventas_por_categoria[categoria]['total'] += trans['total_final']
        
        print(f"{'Categoría':<20} {'Cantidad':<10} {'Total':<15}")
        print("-" * 50)
        for categoria, datos in ventas_por_categoria.items():
            print(f"{categoria:<20} {datos['cantidad']:<10} ${datos['total']:>12,.0f}")
    
    def productos_por_estado(self):
        """Muestra productos agrupados por estado"""
        print("\nPRODUCTOS POR ESTADO")
        print("-" * 30)
        
        productos = self.db.consultar_todos_productos()
        if not productos:
            print("No hay productos registrados.")
            return
        
        # Agrupar por estado
        productos_por_estado = {}
        for producto in productos:
            estado = producto['estado']
            if estado not in productos_por_estado:
                productos_por_estado[estado] = []
            productos_por_estado[estado].append(producto)
        
        for estado, productos_estado in productos_por_estado.items():
            print(f"\n{estado} ({len(productos_estado)} productos):")
            for producto in productos_estado:
                print(f"  • {producto['nombre']} - ${producto['precio_base']:,.2f}")
    
    def mapear_categoria_a_enum(self, categoria_nombre: str) -> Optional[CategoriaProducto]:
        """Mapea el nombre de categoría de la BD al enum de la calculadora"""
        mapeo = {
            "Alimentos Básicos": CategoriaProducto.ALIMENTOS_BASICOS,
            "Licores": CategoriaProducto.LICORES,
            "Bolsas Plásticas": CategoriaProducto.BOLSAS_PLASTICAS,
            "Combustibles": CategoriaProducto.COMBUSTIBLES,
            "Servicios Públicos": CategoriaProducto.SERVICIOS_PUBLICOS,
            "Otros": CategoriaProducto.OTROS
        }
        return mapeo.get(categoria_nombre)
