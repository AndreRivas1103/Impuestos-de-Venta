"""
Controlador para gestionar Categorías (CRUD)
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from src.db.database import BaseDatos

categorias_bp = Blueprint('categorias', __name__)


@categorias_bp.route('/')
def listar():
    """Listar todas las categorías"""
    db = BaseDatos('calculadora_impuestos.db')
    categorias = db.consultar_todas_categorias()
    return render_template('categorias/listar.html', categorias=categorias)


@categorias_bp.route('/buscar', methods=['GET', 'POST'])
def buscar():
    """Buscar categoría por ID"""
    if request.method == 'POST':
        categoria_id = request.form.get('categoria_id')
        if categoria_id:
            try:
                db = BaseDatos('calculadora_impuestos.db')
                categorias = db.consultar_todas_categorias()
                categoria = next((cat for cat in categorias if cat['id'] == int(categoria_id)), None)
                if categoria:
                    return render_template('categorias/buscar.html', categoria=categoria, encontrada=True)
                else:
                    flash('Categoría no encontrada', 'warning')
            except ValueError:
                flash('ID inválido', 'error')
    
    return render_template('categorias/buscar.html', encontrada=False)


@categorias_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    """Crear nueva categoría"""
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        tasa_iva = request.form.get('tasa_iva', '0.19')
        
        if not nombre:
            flash('El nombre es obligatorio', 'error')
            return render_template('categorias/crear.html')
        
        try:
            tasa_iva = float(tasa_iva)
            if tasa_iva < 0 or tasa_iva > 1:
                flash('La tasa de IVA debe estar entre 0.0 y 1.0', 'error')
                return render_template('categorias/crear.html')
            
            db = BaseDatos('calculadora_impuestos.db')
            if db.insertar_categoria(nombre, descripcion, tasa_iva):
                flash('✅ Categoría creada exitosamente', 'success')
                return redirect(url_for('categorias.listar'))
            else:
                flash('❌ Error al crear la categoría', 'error')
        except ValueError:
            flash('Error en los datos ingresados', 'error')
    
    return render_template('categorias/crear.html')


@categorias_bp.route('/editar/<int:categoria_id>', methods=['GET', 'POST'])
def editar(categoria_id):
    """Editar categoría existente"""
    db = BaseDatos('calculadora_impuestos.db')
    categorias = db.consultar_todas_categorias()
    categoria = next((cat for cat in categorias if cat['id'] == categoria_id), None)
    
    if not categoria:
        flash('Categoría no encontrada', 'error')
        return redirect(url_for('categorias.listar'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        tasa_iva = request.form.get('tasa_iva')
        
        nuevo_nombre = nombre if nombre else None
        nueva_descripcion = descripcion if descripcion else None
        nueva_tasa = None
        
        if tasa_iva:
            try:
                nueva_tasa = float(tasa_iva) / 100 if float(tasa_iva) > 1 else float(tasa_iva)
                if nueva_tasa < 0 or nueva_tasa > 1:
                    flash('La tasa debe estar entre 0% y 100%', 'error')
                    return render_template('categorias/editar.html', categoria=categoria)
            except ValueError:
                flash('Tasa de IVA inválida', 'error')
                return render_template('categorias/editar.html', categoria=categoria)
        
        if db.actualizar_categoria(categoria_id, nuevo_nombre, nueva_descripcion, nueva_tasa):
            flash('✅ Categoría actualizada exitosamente', 'success')
            return redirect(url_for('categorias.listar'))
        else:
            flash('❌ Error al actualizar la categoría', 'error')
    
    return render_template('categorias/editar.html', categoria=categoria)


@categorias_bp.route('/eliminar/<int:categoria_id>', methods=['POST'])
def eliminar(categoria_id):
    """Eliminar categoría"""
    db = BaseDatos('calculadora_impuestos.db')
    categorias = db.consultar_todas_categorias()
    categoria = next((cat for cat in categorias if cat['id'] == categoria_id), None)
    
    if not categoria:
        flash('Categoría no encontrada', 'error')
        return redirect(url_for('categorias.listar'))
    
    if db.eliminar_categoria(categoria_id):
        flash('✅ Categoría eliminada exitosamente', 'success')
    else:
        flash('❌ Error al eliminar la categoría. Puede tener productos asociados.', 'error')
    
    return redirect(url_for('categorias.listar'))

