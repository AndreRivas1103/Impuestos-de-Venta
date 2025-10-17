"""
Configuración global para la Calculadora de Impuestos de Venta
"""

# Información de la aplicación
APP_NAME = "Calculadora de Impuestos de Venta"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "Aplicación para calcular impuestos de venta con interfaz gráfica moderna"

# Información del equipo
TEAM_MEMBERS = {
    "backend": ["Paull Harry Palacio Goez", "Andre Rivas Garcia"],
    "frontend": ["Juan Sebastián Villa Rodas", "David Taborda Noreña"],
    "testing": "Equipo completo"
}

# Configuración de la GUI
GUI_CONFIG = {
    "window_size": (900, 700),
    "min_window_size": (700, 500),
    "title": f"{APP_NAME} v{APP_VERSION}",
    "theme_colors": {
        "primary": (0.2, 0.4, 0.8, 1),
        "success": (0.2, 0.7, 0.3, 1),
        "error": (0.8, 0.2, 0.2, 1),
        "warning": (0.9, 0.6, 0.1, 1),
        "info": (0.2, 0.5, 0.8, 1)
    }
}

# Configuración de archivos
FILE_CONFIG = {
    "historial_filename": "historial_impuestos_{timestamp}.json",
    "max_historial_display": 10,
    "encoding": "utf-8"
}

# Configuración de validación
VALIDATION_CONFIG = {
    "max_value": 999999999,
    "min_value": 0.01,
    "decimal_places": 2
}

# Mensajes de la aplicación
MESSAGES = {
    "welcome": "🚀 Iniciando Calculadora de Impuestos de Venta...",
    "version": f"📋 Versión: {APP_VERSION} - Con Interfaz Gráfica",
    "team": "👥 Desarrollado por: Paull Harry Palacio Goez, Andre Rivas Garcia",
    "gui_team": "🎨 GUI por: Juan Sebastián Villa Rodas, David Taborda Noreña",
    "goodbye": "👋 ¡Hasta luego! Gracias por usar la Calculadora de Impuestos.",
    "error_import": "❌ Error de importación",
    "error_unexpected": "❌ Error inesperado",
    "error_validation": "❌ Error de validación",
    "error_type": "❌ Error de tipo de datos"
}
