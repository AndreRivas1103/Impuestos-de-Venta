"""
Entrada principal para la app con base de datos.
"""

from src.ui.interfaz_database import InterfazDatabase


def main():
    try:
        print("Iniciando Calculadora de Impuestos de Venta con Base de Datos...")
        print("-" * 70)
        interfaz = InterfazDatabase()
        interfaz.ejecutar()
    except KeyboardInterrupt:
        print("\n\n¡Hasta luego! Gracias por usar la Calculadora de Impuestos.")
    except ImportError as e:
        print(f"\nError de importación: {e}")
        print("Asegúrese de que todas las dependencias estén instaladas correctamente.")
        print("Ejecute: pip install -r requirements.txt")
    except Exception as e:
        print(f"\nError inesperado: {e}")
        print("Por favor, contacte al soporte técnico si el problema persiste.")
        print("Información del error para el soporte:")
        print(f"   - Tipo: {type(e).__name__}")
        print(f"   - Mensaje: {str(e)}")


if __name__ == "__main__":
    main()


