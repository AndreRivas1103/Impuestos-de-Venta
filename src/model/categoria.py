"""
Modelo de dominio para Categoria
"""

from typing import Optional


class Categoria:
    """Clase que representa una categoría de productos"""
    
    def __init__(self, id: Optional[int] = None, nombre: str = "",
                 descripcion: str = "", tasa_iva: float = 0.19,
                 fecha_creacion: Optional[str] = None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.tasa_iva = tasa_iva
        self.fecha_creacion = fecha_creacion
    
    def __repr__(self) -> str:
        return f"Categoria(id={self.id}, nombre='{self.nombre}', tasa_iva={self.tasa_iva})"
    
    def __str__(self) -> str:
        return f"{self.nombre} (IVA: {self.tasa_iva*100:.0f}%)"
    
    @classmethod
    def desde_dict(cls, datos: dict) -> 'Categoria':
        """Crea una instancia de Categoria desde un diccionario"""
        return cls(
            id=datos.get('id'),
            nombre=datos.get('nombre', ''),
            descripcion=datos.get('descripcion', ''),
            tasa_iva=datos.get('tasa_iva', 0.19),
            fecha_creacion=datos.get('fecha_creacion')
        )
    
    def a_dict(self) -> dict:
        """Convierte la instancia a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'tasa_iva': self.tasa_iva,
            'fecha_creacion': self.fecha_creacion
        }
    
    def es_valida(self) -> bool:
        """Valida que la categoría tenga los datos mínimos requeridos"""
        return (self.nombre and len(self.nombre.strip()) > 0 and 
                0.0 <= self.tasa_iva <= 1.0)

