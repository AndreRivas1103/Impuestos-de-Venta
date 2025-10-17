
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
        print("🚀 Iniciando Calculadora de Impuestos de Venta...")
        print("📋 Versión: 2.0 - Con Interfaz Gráfica")
        print("👥 Desarrollado por: Paull Harry Palacio Goez, Andre Rivas Garcia")
        print("🎨 GUI por: Juan Sebastián Villa Rodas, David Taborda Noreña")
        print("-" * 60)
        
        interfaz = InterfazConsola()
        interfaz.ejecutar()
        
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego! Gracias por usar la Calculadora de Impuestos.")
    except ImportError as e:
        print(f"\n❌ Error de importación: {e}")
        print("💡 Asegúrese de que todas las dependencias estén instaladas correctamente.")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("🔧 Por favor, contacte al soporte técnico si el problema persiste.")
        print("📧 Información del error para el soporte:")
        print(f"   - Tipo: {type(e).__name__}")
        print(f"   - Mensaje: {str(e)}")

if __name__ == "__main__":
    main()
