from enum import Enum
from typing import Dict, List, Tuple

class TipoImpuesto(Enum):
    EXENTO = "Exento"
    IVA_5 = "IVA 5%"
    IVA_19 = "IVA 19%"
    INC = "Impuesto Nacional al Consumo"
    LICORES = "Impuesto de Rentas a los Licores"
    BOLSAS_PLASTICAS = "Impuesto de Bolsas Plásticas"

class CategoriaProducto(Enum):
    ALIMENTOS_BASICOS = "Alimentos Básicos"
    LICORES = "Licores"
    BOLSAS_PLASTICAS = "Bolsas Plásticas"
    COMBUSTIBLES = "Combustibles"
    SERVICIOS_PUBLICOS = "Servicios Públicos"
    OTROS = "Otros"

class CalculadoraImpuestos:
    def __init__(self):
        self.categorias_impuestos = {
            CategoriaProducto.ALIMENTOS_BASICOS: [TipoImpuesto.IVA_5],
            CategoriaProducto.LICORES: [TipoImpuesto.IVA_19, TipoImpuesto.LICORES],
            CategoriaProducto.BOLSAS_PLASTICAS: [TipoImpuesto.IVA_19, TipoImpuesto.BOLSAS_PLASTICAS],
            CategoriaProducto.COMBUSTIBLES: [TipoImpuesto.IVA_19, TipoImpuesto.INC],
            CategoriaProducto.SERVICIOS_PUBLICOS: [TipoImpuesto.EXENTO],
            CategoriaProducto.OTROS: [TipoImpuesto.IVA_19]
        }
        
        self.tasas_impuestos = {
            TipoImpuesto.IVA_5: 0.05,
            TipoImpuesto.IVA_19: 0.19,
            TipoImpuesto.INC: 0.08,
            TipoImpuesto.LICORES: 0.25,
            TipoImpuesto.BOLSAS_PLASTICAS: 0.20
        }
    
    def calcular_impuestos(self, valor_base: float, categoria: CategoriaProducto) -> Dict:
        """
        Calcula los impuestos aplicables para un producto
        
        Args:
            valor_base (float): Valor base del producto
            categoria (CategoriaProducto): Categoría del producto
            
        Returns:
            Dict: Diccionario con el desglose de impuestos
            
        Raises:
            ValueError: Si el valor base es inválido o la categoría no existe
            TypeError: Si los tipos de datos son incorrectos
        """
        try:
            # Validar tipos de datos
            if not isinstance(valor_base, (int, float)):
                raise TypeError("El valor base debe ser un número")
            
            if not isinstance(categoria, CategoriaProducto):
                raise TypeError("La categoría debe ser un valor válido de CategoriaProducto")
            
            # Validar valor base
            if valor_base <= 0:
                raise ValueError("El valor base debe ser mayor a 0")
            
            if valor_base > 999999999:  # Límite razonable para evitar overflow
                raise ValueError("El valor base es demasiado grande (máximo: $999,999,999)")
            
            # Validar categoría
            if categoria not in self.categorias_impuestos:
                raise ValueError(f"Categoría no válida: {categoria}")
            
            # Calcular impuestos
            impuestos_aplicables = self.categorias_impuestos[categoria]
            desglose_impuestos = {}
            total_impuestos = 0
            
            for impuesto in impuestos_aplicables:
                if impuesto == TipoImpuesto.EXENTO:
                    desglose_impuestos[impuesto.value] = 0
                else:
                    if impuesto not in self.tasas_impuestos:
                        raise ValueError(f"Tasa de impuesto no definida para: {impuesto}")
                    
                    tasa = self.tasas_impuestos[impuesto]
                    valor_impuesto = round(valor_base * tasa, 2)  # Redondear a 2 decimales
                    desglose_impuestos[impuesto.value] = valor_impuesto
                    total_impuestos += valor_impuesto
            
            # Redondear totales
            total_impuestos = round(total_impuestos, 2)
            valor_total = round(valor_base + total_impuestos, 2)
            
            return {
                "valor_base": valor_base,
                "categoria": categoria.value,
                "impuestos": desglose_impuestos,
                "total_impuestos": total_impuestos,
                "valor_total": valor_total
            }
            
        except (ValueError, TypeError) as e:
            # Re-lanzar errores de validación con mensajes más claros
            raise e
        except Exception as e:
            # Capturar cualquier error inesperado
            raise Exception(f"Error inesperado al calcular impuestos: {str(e)}")
    
    def obtener_categorias_disponibles(self) -> List[str]:
        """Retorna la lista de categorías disponibles"""
        return [cat.value for cat in CategoriaProducto]
    
    def obtener_impuestos_por_categoria(self, categoria: CategoriaProducto) -> List[str]:
        """Retorna los impuestos aplicables para una categoría específica"""
        if categoria not in self.categorias_impuestos:
            raise ValueError(f"Categoría no válida: {categoria}")
        
        return [imp.value for imp in self.categorias_impuestos[categoria]]
