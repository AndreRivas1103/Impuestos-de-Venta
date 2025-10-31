"""
Entrada principal CLI para la Calculadora de Impuestos.
"""

from src.ui.interfaz_consola import InterfazConsola


def main():
    try:
        print("Iniciando Calculadora de Impuestos de Venta...")
        print("-" * 60)
        interfaz = InterfazConsola()
        interfaz.ejecutar()
    except KeyboardInterrupt:
        print("\n\n¡Hasta luego! Gracias por usar la Calculadora de Impuestos.")
    except ImportError as e:
        print(f"\nError de importación: {e}")
        print("Asegúrese de que todas las dependencias estén instaladas correctamente.")
    except Exception as e:
        print(f"\nError inesperado: {e}")
        print("Por favor, contacte al soporte técnico si el problema persiste.")


if __name__ == "__main__":
    main()


