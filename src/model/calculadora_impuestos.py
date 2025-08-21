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
        if valor_base <= 0:
            raise ValueError("El valor base debe ser mayor a 0")
        
        if categoria not in self.categorias_impuestos:
            raise ValueError(f"Categoría no válida: {categoria}")
        
        impuestos_aplicables = self.categorias_impuestos[categoria]
        desglose_impuestos = {}
        total_impuestos = 0
        
        for impuesto in impuestos_aplicables:
            if impuesto == TipoImpuesto.EXENTO:
                desglose_impuestos[impuesto.value] = 0
            else:
                tasa = self.tasas_impuestos[impuesto]
                valor_impuesto = valor_base * tasa
                desglose_impuestos[impuesto.value] = valor_impuesto
                total_impuestos += valor_impuesto
        
        valor_total = valor_base + total_impuestos
        
        return {
            "valor_base": valor_base,
            "categoria": categoria.value,
            "impuestos": desglose_impuestos,
            "total_impuestos": total_impuestos,
            "valor_total": valor_total
        }
    
    def obtener_categorias_disponibles(self) -> List[str]:
        """Retorna la lista de categorías disponibles"""
        return [cat.value for cat in CategoriaProducto]
    
    def obtener_impuestos_por_categoria(self, categoria: CategoriaProducto) -> List[str]:
        """Retorna los impuestos aplicables para una categoría específica"""
        if categoria not in self.categorias_impuestos:
            raise ValueError(f"Categoría no válida: {categoria}")
        
        return [imp.value for imp in self.categorias_impuestos[categoria]] 