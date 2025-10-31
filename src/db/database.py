"""
Modelo de Base de Datos para la Calculadora de Impuestos
Implementa un ORM simple para gestionar productos, categorías e impuestos
"""

import sqlite3
import os
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from enum import Enum

class EstadoProducto(Enum):
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"
    DESCONTINUADO = "Descontinuado"

class BaseDatos:
    """Clase principal para manejar la base de datos SQLite"""
    
    def __init__(self, nombre_db: str = "calculadora_impuestos.db"):
        self.nombre_db = nombre_db
        self.conexion = None
        self.cursor = None
    
    def conectar(self):
        try:
            self.conexion = sqlite3.connect(self.nombre_db)
            self.cursor = self.conexion.cursor()
            self.conexion.execute("PRAGMA foreign_keys = ON")
            return True
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            return False
    
    def desconectar(self):
        try:
            if self.cursor:
                self.cursor.close()
                self.cursor = None
        except:
            pass
        
        try:
            if self.conexion:
                self.conexion.close()
                self.conexion = None
        except:
            pass
    
    def crear_tablas(self) -> bool:
        try:
            if not self.conectar():
                return False
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS categorias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    descripcion TEXT,
                    tasa_iva REAL DEFAULT 0.19,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    precio_base REAL NOT NULL CHECK (precio_base > 0),
                    categoria_id INTEGER NOT NULL,
                    estado TEXT DEFAULT 'Activo' CHECK (estado IN ('Activo', 'Inactivo', 'Descontinuado')),
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (categoria_id) REFERENCES categorias (id)
                )
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS impuestos_adicionales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    tasa REAL NOT NULL CHECK (tasa >= 0 AND tasa <= 1),
                    descripcion TEXT,
                    aplicable_a_categoria_id INTEGER,
                    activo BOOLEAN DEFAULT 1,
                    FOREIGN KEY (aplicable_a_categoria_id) REFERENCES categorias (id)
                )
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS transacciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto_id INTEGER NOT NULL,
                    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
                    precio_unitario REAL NOT NULL CHECK (precio_unitario > 0),
                    subtotal REAL NOT NULL,
                    total_impuestos REAL NOT NULL,
                    total_final REAL NOT NULL,
                    fecha_transaccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (producto_id) REFERENCES productos (id)
                )
            """)
            
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_productos_categoria ON productos(categoria_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_transacciones_fecha ON transacciones(fecha_transaccion)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_productos_estado ON productos(estado)")
            
            self.conexion.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"Error al crear tablas: {e}")
            if self.conexion:
                self.conexion.rollback()
            return False
        finally:
            self.desconectar()
    
    def insertar_categoria(self, nombre: str, descripcion: str = "", tasa_iva: float = 0.19) -> bool:
        try:
            if tasa_iva < 0 or tasa_iva > 1:
                return False
            
            if not self.conectar():
                return False
            
            self.cursor.execute("""
                INSERT INTO categorias (nombre, descripcion, tasa_iva)
                VALUES (?, ?, ?)
            """, (nombre, descripcion, tasa_iva))
            
            self.conexion.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"Error al insertar categoría: {e}")
            if self.conexion:
                self.conexion.rollback()
            return False
        finally:
            if self.conexion:
                self.desconectar()
    
    def insertar_producto(self, nombre: str, precio_base: float, categoria_id: int, 
                         descripcion: str = "", estado: str = "Activo") -> bool:
        try:
            if not self.conectar():
                return False
            
            self.cursor.execute("""
                INSERT INTO productos (nombre, descripcion, precio_base, categoria_id, estado)
                VALUES (?, ?, ?, ?, ?)
            """, (nombre, descripcion, precio_base, categoria_id, estado))
            
            self.conexion.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"Error al insertar producto: {e}")
            if self.conexion:
                self.conexion.rollback()
            return False
        finally:
            self.desconectar()
    
    def insertar_impuesto_adicional(self, nombre: str, tasa: float, descripcion: str = "",
                                   categoria_id: Optional[int] = None) -> bool:
        try:
            if not self.conectar():
                return False
            
            self.cursor.execute("""
                INSERT INTO impuestos_adicionales (nombre, tasa, descripcion, aplicable_a_categoria_id)
                VALUES (?, ?, ?, ?)
            """, (nombre, tasa, descripcion, categoria_id))
            
            self.conexion.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"Error al insertar impuesto adicional: {e}")
            if self.conexion:
                self.conexion.rollback()
            return False
        finally:
            self.desconectar()
    
    def insertar_transaccion(self, producto_id: int, cantidad: int, precio_unitario: float,
                           subtotal: float, total_impuestos: float, total_final: float) -> bool:
        try:
            if not self.conectar():
                return False
            
            self.cursor.execute("""
                INSERT INTO transacciones (producto_id, cantidad, precio_unitario, 
                                         subtotal, total_impuestos, total_final)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (producto_id, cantidad, precio_unitario, subtotal, total_impuestos, total_final))
            
            self.conexion.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"Error al insertar transacción: {e}")
            if self.conexion:
                self.conexion.rollback()
            return False
        finally:
            self.desconectar()
    
    def actualizar_producto(self, producto_id: int, nombre: str = None, precio_base: float = None,
                           categoria_id: int = None, descripcion: str = None, 
                           estado: str = None) -> bool:
        try:
            if not self.conectar():
                return False
            
            campos_actualizar = []
            valores = []
            
            if nombre is not None:
                campos_actualizar.append("nombre = ?")
                valores.append(nombre)
            
            if precio_base is not None:
                campos_actualizar.append("precio_base = ?")
                valores.append(precio_base)
            
            if categoria_id is not None:
                campos_actualizar.append("categoria_id = ?")
                valores.append(categoria_id)
            
            if descripcion is not None:
                campos_actualizar.append("descripcion = ?")
                valores.append(descripcion)
            
            if estado is not None:
                campos_actualizar.append("estado = ?")
                valores.append(estado)
            
            if not campos_actualizar:
                return False
            
            campos_actualizar.append("fecha_actualizacion = CURRENT_TIMESTAMP")
            valores.append(producto_id)
            
            consulta = f"""
                UPDATE productos 
                SET {', '.join(campos_actualizar)}
                WHERE id = ?
            """
            
            self.cursor.execute(consulta, valores)
            
            if self.cursor.rowcount == 0:
                print(f"No se encontró el producto con ID {producto_id}")
                return False
            
            self.conexion.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"Error al actualizar producto: {e}")
            if self.conexion:
                self.conexion.rollback()
            return False
        finally:
            self.desconectar()
    
    def actualizar_categoria(self, categoria_id: int, nombre: str = None, 
                           descripcion: str = None, tasa_iva: float = None) -> bool:
        try:
            if not self.conectar():
                return False
            
            campos_actualizar = []
            valores = []
            
            if nombre is not None:
                campos_actualizar.append("nombre = ?")
                valores.append(nombre)
            
            if descripcion is not None:
                campos_actualizar.append("descripcion = ?")
                valores.append(descripcion)
            
            if tasa_iva is not None:
                campos_actualizar.append("tasa_iva = ?")
                valores.append(tasa_iva)
            
            if not campos_actualizar:
                return False
            
            valores.append(categoria_id)
            
            consulta = f"""
                UPDATE categorias 
                SET {', '.join(campos_actualizar)}
                WHERE id = ?
            """
            
            self.cursor.execute(consulta, valores)
            
            if self.cursor.rowcount == 0:
                print(f"No se encontró la categoría con ID {categoria_id}")
                return False
            
            self.conexion.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"Error al actualizar categoría: {e}")
            if self.conexion:
                self.conexion.rollback()
            return False
        finally:
            self.desconectar()
    
    def eliminar_producto(self, producto_id: int) -> bool:
        try:
            if not self.conectar():
                return False
            
            self.cursor.execute("SELECT COUNT(*) FROM transacciones WHERE producto_id = ?", (producto_id,))
            transacciones_asociadas = self.cursor.fetchone()[0]
            
            if transacciones_asociadas > 0:
                print(f"No se puede eliminar el producto. Tiene {transacciones_asociadas} transacciones asociadas.")
                return False
            
            self.cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
            
            if self.cursor.rowcount == 0:
                print(f"No se encontró el producto con ID {producto_id}")
                return False
            
            self.conexion.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"Error al eliminar producto: {e}")
            if self.conexion:
                self.conexion.rollback()
            return False
        finally:
            self.desconectar()
    
    def eliminar_categoria(self, categoria_id: int) -> bool:
        try:
            if not self.conectar():
                return False
            
            self.cursor.execute("SELECT COUNT(*) FROM productos WHERE categoria_id = ?", (categoria_id,))
            productos_asociados = self.cursor.fetchone()[0]
            
            if productos_asociados > 0:
                print(f"No se puede eliminar la categoría. Tiene {productos_asociados} productos asociados.")
                return False
            
            self.cursor.execute("DELETE FROM categorias WHERE id = ?", (categoria_id,))
            
            if self.cursor.rowcount == 0:
                print(f"No se encontró la categoría con ID {categoria_id}")
                return False
            
            self.conexion.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"Error al eliminar categoría: {e}")
            if self.conexion:
                self.conexion.rollback()
            return False
        finally:
            self.desconectar()
    
    def consultar_todos_productos(self) -> List[Dict]:
        try:
            if not self.conectar():
                return []
            
            self.cursor.execute("""
                SELECT p.id, p.nombre, p.descripcion, p.precio_base, 
                       p.estado, p.fecha_creacion, p.fecha_actualizacion,
                       c.nombre as categoria_nombre, c.tasa_iva
                FROM productos p
                JOIN categorias c ON p.categoria_id = c.id
                ORDER BY p.nombre
            """)
            
            columnas = [descripcion[0] for descripcion in self.cursor.description]
            productos = []
            
            for fila in self.cursor.fetchall():
                producto = dict(zip(columnas, fila))
                productos.append(producto)
            
            return productos
            
        except sqlite3.Error as e:
            print(f"Error al consultar productos: {e}")
            return []
        finally:
            self.desconectar()
    
    def consultar_producto_por_id(self, producto_id: int) -> Optional[Dict]:
        try:
            if not self.conectar():
                return None
            
            self.cursor.execute("""
                SELECT p.id, p.nombre, p.descripcion, p.precio_base, 
                       p.estado, p.fecha_creacion, p.fecha_actualizacion,
                       c.nombre as categoria_nombre, c.tasa_iva
                FROM productos p
                JOIN categorias c ON p.categoria_id = c.id
                WHERE p.id = ?
            """, (producto_id,))
            
            fila = self.cursor.fetchone()
            if fila:
                columnas = [descripcion[0] for descripcion in self.cursor.description]
                return dict(zip(columnas, fila))
            
            return None
            
        except sqlite3.Error as e:
            print(f"Error al consultar producto: {e}")
            return None
        finally:
            self.desconectar()
    
    def consultar_productos_por_categoria(self, categoria_id: int) -> List[Dict]:
        try:
            if not self.conectar():
                return []
            
            self.cursor.execute("""
                SELECT p.id, p.nombre, p.descripcion, p.precio_base, 
                       p.estado, p.fecha_creacion, p.fecha_actualizacion,
                       c.nombre as categoria_nombre, c.tasa_iva
                FROM productos p
                JOIN categorias c ON p.categoria_id = c.id
                WHERE p.categoria_id = ?
                ORDER BY p.nombre
            """, (categoria_id,))
            
            columnas = [descripcion[0] for descripcion in self.cursor.description]
            productos = []
            
            for fila in self.cursor.fetchall():
                producto = dict(zip(columnas, fila))
                productos.append(producto)
            
            return productos
            
        except sqlite3.Error as e:
            print(f"Error al consultar productos por categoría: {e}")
            return []
        finally:
            self.desconectar()
    
    def consultar_todas_categorias(self) -> List[Dict]:
        try:
            if not self.conectar():
                return []
            
            self.cursor.execute("""
                SELECT id, nombre, descripcion, tasa_iva, fecha_creacion
                FROM categorias
                ORDER BY nombre
            """)
            
            columnas = [descripcion[0] for descripcion in self.cursor.description]
            categorias = []
            
            for fila in self.cursor.fetchall():
                categoria = dict(zip(columnas, fila))
                categorias.append(categoria)
            
            return categorias
            
        except sqlite3.Error as e:
            print(f"Error al consultar categorías: {e}")
            return []
        finally:
            self.desconectar()
    
    def consultar_transacciones_recientes(self, limite: int = 10) -> List[Dict]:
        try:
            if not self.conectar():
                return []
            
            self.cursor.execute("""
                SELECT t.id, t.cantidad, t.precio_unitario, t.subtotal, 
                       t.total_impuestos, t.total_final, t.fecha_transaccion,
                       p.nombre as producto_nombre, c.nombre as categoria_nombre
                FROM transacciones t
                JOIN productos p ON t.producto_id = p.id
                JOIN categorias c ON p.categoria_id = c.id
                ORDER BY t.fecha_transaccion DESC
                LIMIT ?
            """, (limite,))
            
            columnas = [descripcion[0] for descripcion in self.cursor.description]
            transacciones = []
            
            for fila in self.cursor.fetchall():
                transaccion = dict(zip(columnas, fila))
                transacciones.append(transaccion)
            
            return transacciones
            
        except sqlite3.Error as e:
            print(f"Error al consultar transacciones: {e}")
            return []
        finally:
            self.desconectar()
    
    def obtener_estadisticas(self) -> Dict:
        try:
            if not self.conectar():
                return {}
            
            estadisticas = {}
            
            self.cursor.execute("""
                SELECT estado, COUNT(*) as cantidad
                FROM productos
                GROUP BY estado
            """)
            estadisticas['productos_por_estado'] = dict(self.cursor.fetchall())
            
            self.cursor.execute("SELECT COUNT(*) FROM categorias")
            estadisticas['total_categorias'] = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM productos")
            estadisticas['total_productos'] = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM transacciones")
            estadisticas['total_transacciones'] = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT SUM(total_final) FROM transacciones")
            resultado = self.cursor.fetchone()[0]
            estadisticas['valor_total_ventas'] = resultado if resultado else 0
            
            return estadisticas
            
        except sqlite3.Error as e:
            print(f"Error al obtener estadísticas: {e}")
            return {}
        finally:
            self.desconectar()
    
    def inicializar_datos_ejemplo(self) -> bool:
        try:
            categorias_existentes = self.consultar_todas_categorias()
            if len(categorias_existentes) > 0:
                return False
            
            categorias_ejemplo = [
                ("Alimentos Básicos", "Productos alimenticios básicos", 0.05),
                ("Licores", "Bebidas alcohólicas", 0.19),
                ("Bolsas Plásticas", "Bolsas plásticas desechables", 0.19),
                ("Combustibles", "Combustibles para vehículos", 0.19),
                ("Servicios Públicos", "Servicios públicos básicos", 0.0),
                ("Otros", "Otros productos y servicios", 0.19)
            ]
            
            for nombre, descripcion, tasa_iva in categorias_ejemplo:
                if not self.insertar_categoria(nombre, descripcion, tasa_iva):
                    return False
            
            categorias = self.consultar_todas_categorias()
            categoria_map = {cat['nombre']: cat['id'] for cat in categorias}
            
            productos_ejemplo = [
                ("Arroz 500g", "Arroz blanco de 500 gramos", 2500.0, "Alimentos Básicos", "Activo"),
                ("Cerveza Nacional", "Cerveza nacional 330ml", 3500.0, "Licores", "Activo"),
                ("Bolsas Plásticas", "Bolsas plásticas medianas", 100.0, "Bolsas Plásticas", "Activo"),
                ("Gasolina Regular", "Gasolina regular por galón", 12000.0, "Combustibles", "Activo"),
                ("Energía Eléctrica", "Servicio de energía eléctrica", 50000.0, "Servicios Públicos", "Activo"),
                ("Laptop", "Laptop para oficina", 1500000.0, "Otros", "Activo")
            ]
            
            for nombre, descripcion, precio, categoria_nombre, estado in productos_ejemplo:
                categoria_id = categoria_map.get(categoria_nombre)
                if categoria_id:
                    if not self.insertar_producto(nombre, precio, categoria_id, descripcion, estado):
                        return False
            
            impuestos_ejemplo = [
                ("Impuesto Nacional al Consumo", 0.08, "INC para combustibles", "Combustibles"),
                ("Impuesto de Rentas a los Licores", 0.25, "Impuesto especial para licores", "Licores"),
                ("Impuesto de Bolsas Plásticas", 0.20, "Impuesto ecológico para bolsas", "Bolsas Plásticas")
            ]
            
            for nombre, tasa, descripcion, categoria_nombre in impuestos_ejemplo:
                categoria_id = categoria_map.get(categoria_nombre)
                if categoria_id:
                    if not self.insertar_impuesto_adicional(nombre, tasa, descripcion, categoria_id):
                        return False
            
            return True
            
        except Exception as e:
            print(f"Error al inicializar datos de ejemplo: {e}")
            return False


