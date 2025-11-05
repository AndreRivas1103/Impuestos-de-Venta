"""
Controlador para gestionar Productos (CRUD)
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from src.db.database import BaseDatos
from src.model.producto import Producto

productos_bp = Blueprint('productos', __name__)


@productos_bp.route('/')
def listar():
    """Listar todos los productos"""
    db = BaseDatos('calculadora_impuestos.db')
    productos = db.consultar_todos_productos()
    return render_template('productos/listar.html', productos=productos)


@productos_bp.route('/buscar', methods=['GET', 'POST'])
def buscar():
    """Buscar producto por ID"""
    if request.method == 'POST':
        producto_id = request.form.get('producto_id')
        if producto_id:
            try:
                db = BaseDatos('calculadora_impuestos.db')
                producto = db.consultar_producto_por_id(int(producto_id))
                if producto:
                    return render_template('productos/buscar.html', producto=producto, encontrado=True)
                else:
                    flash('Producto no encontrado', 'warning')
            except ValueError:
                flash('ID inválido', 'error')
    
    return render_template('productos/buscar.html', encontrado=False)


@productos_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    """Crear nuevo producto"""
    db = BaseDatos('calculadora_impuestos.db')
    
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        precio_base = request.form.get('precio_base')
        categoria_id = request.form.get('categoria_id')
        estado = request.form.get('estado', 'Activo')
        
        if not nombre or not precio_base or not categoria_id:
            flash('Todos los campos requeridos deben ser completados', 'error')
            categorias = db.consultar_todas_categorias()
            return render_template('productos/crear.html', categorias=categorias)
        
        try:
            precio_base = float(precio_base)
            categoria_id = int(categoria_id)
            
            if precio_base <= 0:
                flash('El precio debe ser mayor a 0', 'error')
                categorias = db.consultar_todas_categorias()
                return render_template('productos/crear.html', categorias=categorias)
            
            if db.insertar_producto(nombre, precio_base, categoria_id, descripcion, estado):
                flash('✅ Producto creado exitosamente', 'success')
                return redirect(url_for('productos.listar'))
            else:
                flash('❌ Error al crear el producto', 'error')
        except ValueError:
            flash('Error en los datos ingresados', 'error')
    
    categorias = db.consultar_todas_categorias()
    return render_template('productos/crear.html', categorias=categorias)


@productos_bp.route('/editar/<int:producto_id>', methods=['GET', 'POST'])
def editar(producto_id):
    """Editar producto existente"""
    db = BaseDatos('calculadora_impuestos.db')
    producto = db.consultar_producto_por_id(producto_id)
    
    if not producto:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('productos.listar'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        precio_base = request.form.get('precio_base')
        estado = request.form.get('estado')
        
        nuevo_nombre = nombre if nombre else None
        nueva_descripcion = descripcion if descripcion else None
        nuevo_precio = float(precio_base) if precio_base else None
        nuevo_estado = estado if estado else None
        
        if nuevo_precio and nuevo_precio <= 0:
            flash('El precio debe ser mayor a 0', 'error')
            categorias = db.consultar_todas_categorias()
            return render_template('productos/editar.html', producto=producto, categorias=categorias)
        
        if db.actualizar_producto(producto_id, nuevo_nombre, nuevo_precio, 
                                 None, nueva_descripcion, nuevo_estado):
            flash('✅ Producto actualizado exitosamente', 'success')
            return redirect(url_for('productos.listar'))
        else:
            flash('❌ Error al actualizar el producto', 'error')
    
    categorias = db.consultar_todas_categorias()
    return render_template('productos/editar.html', producto=producto, categorias=categorias)


@productos_bp.route('/eliminar/<int:producto_id>', methods=['POST'])
def eliminar(producto_id):
    """Eliminar producto"""
    db = BaseDatos('calculadora_impuestos.db')
    
    producto = db.consultar_producto_por_id(producto_id)
    if not producto:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('productos.listar'))
    
    if db.eliminar_producto(producto_id):
        flash('✅ Producto eliminado exitosamente', 'success')
    else:
        flash('❌ Error al eliminar el producto. Puede tener transacciones asociadas.', 'error')
    
    return redirect(url_for('productos.listar'))


@productos_bp.route('/por_categoria')
def por_categoria():
    """Listar productos agrupados por categoría"""
    db = BaseDatos('calculadora_impuestos.db')
    categorias = db.consultar_todas_categorias()
    
    productos_por_categoria = {}
    for categoria in categorias:
        productos = db.consultar_productos_por_categoria(categoria['id'])
        if productos:  # Solo agregar categorías que tengan productos
            productos_por_categoria[categoria['nombre']] = productos
    
    return render_template('productos/por_categoria.html', 
                         productos_por_categoria=productos_por_categoria)

