"""
Controlador para el Home/Menú Principal
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from src.db.database import BaseDatos

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
    """Página principal con menú de opciones"""
    return render_template('home/index.html')


@home_bp.route('/crear_tablas', methods=['POST'])
def crear_tablas():
    """Crear las tablas de la base de datos"""
    try:
        db = BaseDatos('calculadora_impuestos.db')
        if db.crear_tablas():
            flash('✅ Tablas creadas exitosamente', 'success')
        else:
            flash('❌ Error al crear las tablas', 'error')
    except Exception as e:
        flash(f'❌ Error: {str(e)}', 'error')
    
    return redirect(url_for('home.index'))


@home_bp.route('/inicializar_datos', methods=['POST'])
def inicializar_datos():
    """Inicializar datos de ejemplo"""
    try:
        db = BaseDatos('calculadora_impuestos.db')
        
        # Verificar si ya hay datos
        categorias_existentes = db.consultar_todas_categorias()
        if len(categorias_existentes) > 0:
            flash('ℹ️ Las tablas ya contienen datos. Si desea reinicializar, primero elimine los datos existentes.', 'info')
        else:
            # Intentar inicializar solo si no hay datos
            if db.inicializar_datos_ejemplo():
                flash('✅ Datos de ejemplo inicializados exitosamente', 'success')
            else:
                flash('❌ Error al inicializar los datos de ejemplo', 'error')
    except Exception as e:
        flash(f'❌ Error: {str(e)}', 'error')
    
    return redirect(url_for('home.index'))

