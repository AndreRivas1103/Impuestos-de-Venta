import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.calculadora_impuestos import CalculadoraImpuestos, CategoriaProducto

# Constantes para las opciones del menú
OPCION_CALCULAR = "1"
OPCION_VER_CATEGORIAS = "2"
OPCION_VER_IMPUESTOS = "3"
OPCION_SALIR = "4"

class InterfazConsola:
    def __init__(self):
        self.calculadora = CalculadoraImpuestos()
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal de la aplicación"""
        print("\n" + "="*50)
        print("    CALCULADORA DE IMPUESTOS DE VENTA")
        print("="*50)
        print(f"{OPCION_CALCULAR}. Calcular impuestos")
        print(f"{OPCION_VER_CATEGORIAS}. Ver categorías disponibles")
        print(f"{OPCION_VER_IMPUESTOS}. Ver impuestos por categoría")
        print(f"{OPCION_SALIR}. Salir")
        print("-"*50)
    
    def mostrar_categorias(self):
        """Muestra las categorías disponibles"""
        print("\n" + "="*40)
        print("CATEGORÍAS DISPONIBLES:")
        print("="*40)
        categorias = self.calculadora.obtener_categorias_disponibles()
        for i, categoria in enumerate(categorias, 1):
            print(f"{i}. {categoria}")
        print("-"*40)
    
    def obtener_categoria_por_numero(self, numero: int) -> CategoriaProducto:
        """Convierte un número en la categoría correspondiente"""
        categorias = list(CategoriaProducto)
        if 1 <= numero <= len(categorias):
            return categorias[numero - 1]
        else:
            raise ValueError(f"Número de categoría inválido: {numero}")
    
    def solicitar_datos_producto(self):
        """Solicita los datos del producto al usuario"""
        print("\n" + "="*40)
        print("CALCULAR IMPUESTOS")
        print("="*40)
        
        self.mostrar_categorias()
        
        valor_base = float(input("Ingrese el valor base del producto: $"))
        num_categoria = int(input("Ingrese el número de la categoría: "))
        categoria = self.obtener_categoria_por_numero(num_categoria)
        
        return valor_base, categoria
    
    def calcular_impuestos(self, valor_base: float, categoria: CategoriaProducto):
        """Calcula los impuestos usando la calculadora"""
        return self.calculadora.calcular_impuestos(valor_base, categoria)
    
    def calcular_impuestos_interfaz(self):
        """Interfaz principal para calcular impuestos - Interactúa con el usuario, valida entrada, hace cálculo y muestra resultado."""
        try:
            valor_base, categoria = self.solicitar_datos_producto()
            resultado = self.calcular_impuestos(valor_base, categoria)
            self.mostrar_resultados(resultado)
            
        except ValueError as e:
            print(f"\n Error: {e}")
        except Exception as e:
            print(f"\n Error inesperado: {e}")
    
    def mostrar_resultados(self, resultado: dict):
        """Muestra los resultados del cálculo de impuestos"""
        print("\n" + "="*50)
        print("RESULTADOS DEL CÁLCULO")
        print("="*50)
        print(f"Valor Base: ${resultado['valor_base']:,.2f}")
        print(f"Categoría: {resultado['categoria']}")
        print("-"*50)
        print("DESGLOSE DE IMPUESTOS:")
        
        impuestos = resultado['impuestos']
        if not any(impuestos.values()):
            print("   • Exento de impuestos")
        else:
            for impuesto, valor in impuestos.items():
                if valor > 0:
                    print(f"   • {impuesto}: ${valor:,.2f}")
        
        print("-"*50)
        print(f"Total Impuestos: ${resultado['total_impuestos']:,.2f}")
        print(f"VALOR TOTAL: ${resultado['valor_total']:,.2f}")
        print("="*50)
    
    def ver_impuestos_por_categoria(self):
        """Muestra los impuestos aplicables por categoría"""
        print("\n" + "="*50)
        print("IMPUESTOS POR CATEGORÍA")
        print("="*50)
        
        self.mostrar_categorias()
        
        try:
            num_categoria = int(input("Ingrese el número de la categoría: "))
            categoria = self.obtener_categoria_por_numero(num_categoria)
            
            impuestos = self.calculadora.obtener_impuestos_por_categoria(categoria)
            
            print(f"\nImpuestos aplicables para '{categoria.value}':")
            print("-"*40)
            for i, impuesto in enumerate(impuestos, 1):
                print(f"{i}. {impuesto}")
            
        except ValueError as e:
            print(f"\n Error: {e}")
        except Exception as e:
            print(f"\n Error inesperado: {e}")
    
    def ejecutar(self):
        """Ejecuta la interfaz principal"""
        while True:
            self.mostrar_menu_principal()
            
            try:
                opcion = input(f"Seleccione una opción ({OPCION_CALCULAR}-{OPCION_SALIR}): ").strip()
                
                if opcion == OPCION_CALCULAR:
                    self.calcular_impuestos_interfaz()
                elif opcion == OPCION_VER_CATEGORIAS:
                    self.mostrar_categorias()
                elif opcion == OPCION_VER_IMPUESTOS:
                    self.ver_impuestos_por_categoria()
                elif opcion == OPCION_SALIR:
                    print("\n¡Gracias por usar la Calculadora de Impuestos!")
                    break
                else:
                    print(f"\n Opción no válida. Por favor, seleccione {OPCION_CALCULAR}-{OPCION_SALIR}.")
                    
            except KeyboardInterrupt:
                print("\n\n¡Hasta luego!")
                break
            except Exception as e:
                print(f"\n Error inesperado: {e}")

if __name__ == "__main__":
    interfaz = InterfazConsola()
    interfaz.ejecutar()
