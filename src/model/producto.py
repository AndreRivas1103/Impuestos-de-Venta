"""
Modelo de dominio para Producto
"""

from typing import Optional
from datetime import datetime


class Producto:
    """Clase que representa un producto en el sistema"""
    
    def __init__(self, id: Optional[int] = None, nombre: str = "", 
                 descripcion: str = "", precio_base: float = 0.0,
                 categoria_id: Optional[int] = None, 
                 categoria_nombre: Optional[str] = None,
                 tasa_iva: Optional[float] = None,
                 estado: str = "Activo",
                 fecha_creacion: Optional[str] = None,
                 fecha_actualizacion: Optional[str] = None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_base = precio_base
        self.categoria_id = categoria_id
        self.categoria_nombre = categoria_nombre
        self.tasa_iva = tasa_iva
        self.estado = estado
        self.fecha_creacion = fecha_creacion
        self.fecha_actualizacion = fecha_actualizacion
    
    def __repr__(self) -> str:
        return f"Producto(id={self.id}, nombre='{self.nombre}', precio_base={self.precio_base})"
    
    def __str__(self) -> str:
        return f"{self.nombre} - ${self.precio_base:,.2f}"
    
    @classmethod
    def desde_dict(cls, datos: dict) -> 'Producto':
        """Crea una instancia de Producto desde un diccionario"""
        return cls(
            id=datos.get('id'),
            nombre=datos.get('nombre', ''),
            descripcion=datos.get('descripcion', ''),
            precio_base=datos.get('precio_base', 0.0),
            categoria_id=datos.get('categoria_id'),
            categoria_nombre=datos.get('categoria_nombre'),
            tasa_iva=datos.get('tasa_iva'),
            estado=datos.get('estado', 'Activo'),
            fecha_creacion=datos.get('fecha_creacion'),
            fecha_actualizacion=datos.get('fecha_actualizacion')
        )
    
    def a_dict(self) -> dict:
        """Convierte la instancia a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio_base': self.precio_base,
            'categoria_id': self.categoria_id,
            'categoria_nombre': self.categoria_nombre,
            'tasa_iva': self.tasa_iva,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion,
            'fecha_actualizacion': self.fecha_actualizacion
        }
    
    def es_activo(self) -> bool:
        """Verifica si el producto está activo"""
        return self.estado == "Activo"
    
    def es_valido(self) -> bool:
        """Valida que el producto tenga los datos mínimos requeridos"""
        return (self.nombre and len(self.nombre.strip()) > 0 and 
                self.precio_base > 0 and 
                self.categoria_id is not None)

