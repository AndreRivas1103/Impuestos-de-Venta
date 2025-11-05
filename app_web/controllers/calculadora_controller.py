"""
Controlador para la Calculadora de Impuestos
"""

from flask import Blueprint, render_template, request, jsonify
from src.model.calculadora_impuestos import CalculadoraImpuestos, CategoriaProducto

calculadora_bp = Blueprint('calculadora', __name__)


@calculadora_bp.route('/')
def index():
    """Página principal de la calculadora"""
    calculadora = CalculadoraImpuestos()
    categorias = calculadora.obtener_categorias_disponibles()
    return render_template('calculadora/index.html', categorias=categorias)


@calculadora_bp.route('/calcular', methods=['POST'])
def calcular():
    """Calcular impuestos (AJAX)"""
    try:
        valor_base = float(request.form.get('valor_base', 0))
        categoria_nombre = request.form.get('categoria', '')
        
        if valor_base <= 0:
            return jsonify({'error': 'El valor base debe ser mayor a 0'}), 400
        
        # Mapear categoría
        mapeo_categoria = {
            "Alimentos Básicos": CategoriaProducto.ALIMENTOS_BASICOS,
            "Licores": CategoriaProducto.LICORES,
            "Bolsas Plásticas": CategoriaProducto.BOLSAS_PLASTICAS,
            "Combustibles": CategoriaProducto.COMBUSTIBLES,
            "Servicios Públicos": CategoriaProducto.SERVICIOS_PUBLICOS,
            "Otros": CategoriaProducto.OTROS
        }
        
        categoria_enum = mapeo_categoria.get(categoria_nombre)
        if not categoria_enum:
            return jsonify({'error': 'Categoría no válida'}), 400
        
        calculadora = CalculadoraImpuestos()
        resultado = calculadora.calcular_impuestos(valor_base, categoria_enum)
        
        return jsonify(resultado)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

