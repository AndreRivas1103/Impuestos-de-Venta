"""
Aplicación Flask para Calculadora de Impuestos
Patrón MVC con Blueprints
"""

from flask import Flask
from src.db.database import BaseDatos


def create_app(config_name='development'):
    """Factory para crear la aplicación Flask"""
    import os
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'views')
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    app.config['DATABASE'] = 'calculadora_impuestos.db'
    
    # Inicializar base de datos
    db = BaseDatos(app.config['DATABASE'])
    app.db = db
    
    # Registrar Blueprints
    from app_web.controllers.home_controller import home_bp
    from app_web.controllers.productos_controller import productos_bp
    from app_web.controllers.categorias_controller import categorias_bp
    from app_web.controllers.transacciones_controller import transacciones_bp
    from app_web.controllers.calculadora_controller import calculadora_bp
    from app_web.controllers.estadisticas_controller import estadisticas_bp
    
    app.register_blueprint(home_bp)
    app.register_blueprint(productos_bp, url_prefix='/productos')
    app.register_blueprint(categorias_bp, url_prefix='/categorias')
    app.register_blueprint(transacciones_bp, url_prefix='/transacciones')
    app.register_blueprint(calculadora_bp, url_prefix='/calculadora')
    app.register_blueprint(estadisticas_bp, url_prefix='/estadisticas')
    
    return app

