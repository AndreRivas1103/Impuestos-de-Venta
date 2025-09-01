
"""
Calculadora de Impuestos de Venta
Archivo principal para ejecutar la aplicación
"""

import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from view.interfaz_consola import InterfazConsola

def main():
    """Función principal que ejecuta la aplicación"""
    try:
        interfaz = InterfazConsola()
        interfaz.ejecutar()
    except KeyboardInterrupt:
        print("\n\n¡Hasta luego!")
    except Exception as e:
        print(f"\nError inesperado: {e}")

if __name__ == "__main__":
    main()
