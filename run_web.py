#!/usr/bin/env python
"""
Script para ejecutar la aplicación web Flask
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app_web import create_app

if __name__ == '__main__':
    app = create_app()
    
    # Configuración para desarrollo
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    app = create_app()

