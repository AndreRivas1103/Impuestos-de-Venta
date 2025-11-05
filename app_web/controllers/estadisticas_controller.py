"""
Controlador para Estadísticas y Consultas Avanzadas
"""

from flask import Blueprint, render_template
from src.db.database import BaseDatos

estadisticas_bp = Blueprint('estadisticas', __name__)


@estadisticas_bp.route('/')
def index():
    """Página principal de estadísticas"""
    db = BaseDatos('calculadora_impuestos.db')
    estadisticas = db.obtener_estadisticas()
    return render_template('estadisticas/index.html', estadisticas=estadisticas)


@estadisticas_bp.route('/productos_mas_caros')
def productos_mas_caros():
    """Top 5 productos más caros"""
    db = BaseDatos('calculadora_impuestos.db')
    productos = db.consultar_todos_productos()
    productos_ordenados = sorted(productos, key=lambda x: x['precio_base'], reverse=True)
    return render_template('estadisticas/productos_mas_caros.html', 
                         productos=productos_ordenados[:5])


@estadisticas_bp.route('/productos_mas_baratos')
def productos_mas_baratos():
    """Top 5 productos más baratos"""
    db = BaseDatos('calculadora_impuestos.db')
    productos = db.consultar_todos_productos()
    productos_ordenados = sorted(productos, key=lambda x: x['precio_base'])
    return render_template('estadisticas/productos_mas_baratos.html', 
                         productos=productos_ordenados[:5])


@estadisticas_bp.route('/ventas_por_categoria')
def ventas_por_categoria():
    """Ventas agrupadas por categoría"""
    db = BaseDatos('calculadora_impuestos.db')
    transacciones = db.consultar_transacciones_recientes(1000)
    
    ventas_por_categoria = {}
    for trans in transacciones:
        categoria = trans['categoria_nombre']
        if categoria not in ventas_por_categoria:
            ventas_por_categoria[categoria] = {'cantidad': 0, 'total': 0}
        ventas_por_categoria[categoria]['cantidad'] += trans['cantidad']
        ventas_por_categoria[categoria]['total'] += trans['total_final']
    
    return render_template('estadisticas/ventas_por_categoria.html', 
                         ventas_por_categoria=ventas_por_categoria)


@estadisticas_bp.route('/productos_por_estado')
def productos_por_estado():
    """Productos agrupados por estado"""
    db = BaseDatos('calculadora_impuestos.db')
    productos = db.consultar_todos_productos()
    
    productos_por_estado = {}
    for producto in productos:
        estado = producto['estado']
        if estado not in productos_por_estado:
            productos_por_estado[estado] = []
        productos_por_estado[estado].append(producto)
    
    return render_template('estadisticas/productos_por_estado.html', 
                         productos_por_estado=productos_por_estado)

