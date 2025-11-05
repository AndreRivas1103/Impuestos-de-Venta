"""
Modelo de dominio para Transaccion
"""

from typing import Optional
from datetime import datetime


class Transaccion:
    """Clase que representa una transacción de venta"""
    
    def __init__(self, id: Optional[int] = None, producto_id: int = 0,
                 producto_nombre: Optional[str] = None,
                 categoria_nombre: Optional[str] = None,
                 cantidad: int = 0, precio_unitario: float = 0.0,
                 subtotal: float = 0.0, total_impuestos: float = 0.0,
                 total_final: float = 0.0,
                 fecha_transaccion: Optional[str] = None):
        self.id = id
        self.producto_id = producto_id
        self.producto_nombre = producto_nombre
        self.categoria_nombre = categoria_nombre
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = subtotal
        self.total_impuestos = total_impuestos
        self.total_final = total_final
        self.fecha_transaccion = fecha_transaccion
    
    def __repr__(self) -> str:
        return f"Transaccion(id={self.id}, producto_id={self.producto_id}, total_final={self.total_final})"
    
    def __str__(self) -> str:
        producto = self.producto_nombre or f"Producto {self.producto_id}"
        return f"{producto} - Cantidad: {self.cantidad} - Total: ${self.total_final:,.2f}"
    
    @classmethod
    def desde_dict(cls, datos: dict) -> 'Transaccion':
        """Crea una instancia de Transaccion desde un diccionario"""
        return cls(
            id=datos.get('id'),
            producto_id=datos.get('producto_id', 0),
            producto_nombre=datos.get('producto_nombre'),
            categoria_nombre=datos.get('categoria_nombre'),
            cantidad=datos.get('cantidad', 0),
            precio_unitario=datos.get('precio_unitario', 0.0),
            subtotal=datos.get('subtotal', 0.0),
            total_impuestos=datos.get('total_impuestos', 0.0),
            total_final=datos.get('total_final', 0.0),
            fecha_transaccion=datos.get('fecha_transaccion')
        )
    
    def a_dict(self) -> dict:
        """Convierte la instancia a diccionario"""
        return {
            'id': self.id,
            'producto_id': self.producto_id,
            'producto_nombre': self.producto_nombre,
            'categoria_nombre': self.categoria_nombre,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            'subtotal': self.subtotal,
            'total_impuestos': self.total_impuestos,
            'total_final': self.total_final,
            'fecha_transaccion': self.fecha_transaccion
        }
    
    def calcular_totales(self) -> None:
        """Calcula subtotal, impuestos y total final basándose en cantidad y precio"""
        self.subtotal = self.precio_unitario * self.cantidad
        # Nota: total_impuestos debe calcularse externamente usando la calculadora
        self.total_final = self.subtotal + self.total_impuestos
    
    def es_valida(self) -> bool:
        """Valida que la transacción tenga los datos mínimos requeridos"""
        return (self.producto_id > 0 and 
                self.cantidad > 0 and 
                self.precio_unitario > 0 and
                self.total_final >= 0)

