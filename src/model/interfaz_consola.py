import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model.calculadora_impuestos import CalculadoraImpuestos, CategoriaProducto

class InterfazConsola:
    def __init__(self):
        self.calculadora = CalculadoraImpuestos()
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal de la aplicación"""
        print("\n" + "="*50)
        print("    CALCULADORA DE IMPUESTOS DE VENTA")
        print("="*50)
        print("1. Calcular impuestos")
        print("2. Ver categorías disponibles")
        print("3. Ver impuestos por categoría")
        print("4. Salir")
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
    
    def calcular_impuestos_interfaz(self):
        """Interfaz para calcular impuestos"""
        print("\n" + "="*40)
        print("CALCULAR IMPUESTOS")
        print("="*40)
        
        self.mostrar_categorias()
        
        try:
            valor_base = float(input("Ingrese el valor base del producto: $"))
            
            num_categoria = int(input("Ingrese el número de la categoría: "))
            categoria = self.obtener_categoria_por_numero(num_categoria)
            
            resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
            
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
                opcion = input("Seleccione una opción (1-4): ").strip()
                
                if opcion == "1":
                    self.calcular_impuestos_interfaz()
                elif opcion == "2":
                    self.mostrar_categorias()
                elif opcion == "3":
                    self.ver_impuestos_por_categoria()
                elif opcion == "4":
                    print("\n¡Gracias por usar la Calculadora de Impuestos!")
                    break
                else:
                    print("\n Opción no válida. Por favor, seleccione 1-4.")
                    
            except KeyboardInterrupt:
                print("\n\n¡Hasta luego!")
                break
            except Exception as e:
                print(f"\n Error inesperado: {e}")

if __name__ == "__main__":
    interfaz = InterfazConsola()
    interfaz.ejecutar() 