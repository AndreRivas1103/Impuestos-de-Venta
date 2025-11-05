"""
Controlador para gestionar Transacciones
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from src.db.database import BaseDatos
from src.model.calculadora_impuestos import CalculadoraImpuestos, CategoriaProducto

transacciones_bp = Blueprint('transacciones', __name__)


@transacciones_bp.route('/')
def listar():
    """Listar transacciones recientes"""
    db = BaseDatos('calculadora_impuestos.db')
    limite = request.args.get('limite', 10, type=int)
    transacciones = db.consultar_transacciones_recientes(limite)
    return render_template('transacciones/listar.html', transacciones=transacciones, limite=limite)


@transacciones_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    """Registrar nueva transacción"""
    db = BaseDatos('calculadora_impuestos.db')
    calculadora = CalculadoraImpuestos()
    
    if request.method == 'POST':
        producto_id = request.form.get('producto_id')
        cantidad = request.form.get('cantidad')
        
        if not producto_id or not cantidad:
            flash('Todos los campos son requeridos', 'error')
            productos = db.consultar_todos_productos()
            productos_activos = [p for p in productos if p['estado'] == 'Activo']
            return render_template('transacciones/crear.html', productos=productos_activos)
        
        try:
            producto_id = int(producto_id)
            cantidad = int(cantidad)
            
            if cantidad <= 0:
                flash('La cantidad debe ser mayor a 0', 'error')
                productos = db.consultar_todos_productos()
                productos_activos = [p for p in productos if p['estado'] == 'Activo']
                return render_template('transacciones/crear.html', productos=productos_activos)
            
            producto = db.consultar_producto_por_id(producto_id)
            if not producto or producto['estado'] != 'Activo':
                flash('Producto no encontrado o no está activo', 'error')
                productos = db.consultar_todos_productos()
                productos_activos = [p for p in productos if p['estado'] == 'Activo']
                return render_template('transacciones/crear.html', productos=productos_activos)
            
            precio_unitario = producto['precio_base']
            subtotal = precio_unitario * cantidad
            
            # Mapear categoría a enum
            categoria_nombre = producto['categoria_nombre']
            mapeo_categoria = {
                "Alimentos Básicos": CategoriaProducto.ALIMENTOS_BASICOS,
                "Licores": CategoriaProducto.LICORES,
                "Bolsas Plásticas": CategoriaProducto.BOLSAS_PLASTICAS,
                "Combustibles": CategoriaProducto.COMBUSTIBLES,
                "Servicios Públicos": CategoriaProducto.SERVICIOS_PUBLICOS,
                "Otros": CategoriaProducto.OTROS
            }
            categoria_enum = mapeo_categoria.get(categoria_nombre)
            
            if categoria_enum:
                resultado_impuestos = calculadora.calcular_impuestos(precio_unitario, categoria_enum)
                total_impuestos = resultado_impuestos['total_impuestos'] * cantidad
                total_final = subtotal + total_impuestos
                
                if db.insertar_transaccion(producto_id, cantidad, precio_unitario,
                                         subtotal, total_impuestos, total_final):
                    flash('✅ Transacción registrada exitosamente', 'success')
                    return redirect(url_for('transacciones.listar'))
                else:
                    flash('❌ Error al registrar la transacción', 'error')
            else:
                flash('No se pudo calcular los impuestos para esta categoría', 'error')
                
        except ValueError:
            flash('Error en los datos ingresados', 'error')
    
    productos = db.consultar_todos_productos()
    productos_activos = [p for p in productos if p['estado'] == 'Activo']
    return render_template('transacciones/crear.html', productos=productos_activos)

