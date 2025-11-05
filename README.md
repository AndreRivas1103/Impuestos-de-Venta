# Impuestos de Venta

## Descripción
Aplicación para gestionar productos, categorías, transacciones y calcular impuestos de venta. Incluye interfaz web con Flask y utilitarios de consola. Base de datos por defecto: SQLite.

## Requisitos
- Python 3.11 (ver `runtime.txt`)
- pip para instalar dependencias

## Instalación
```bash
pip install -r requirements.txt
```

## Ejecución (desarrollo)
```bash
python run_web.py
# URL: http://localhost:5000
```

## Pruebas
```bash
python -m unittest tests/test_calculadora_impuestos.py
```

## Estructura del proyecto
```
Impuestos-de-Venta/
├── app_web/                      # App web Flask (MVC)
│   ├── controllers/              # Blueprints
│   ├── views/                    # Templates Jinja2
│   ├── static/                   # CSS/JS
│   └── __init__.py               # Factory de Flask
├── src/
│   ├── app/                      # Entradas CLI
│   ├── db/                       # Capa de datos (SQLite)
│   └── model/                    # Lógica de dominio
├── tests/                        # Pruebas unitarias
├── run_web.py                    # Arranque local
├── requirements.txt              # Dependencias
├── Procfile                      # Arranque producción (gunicorn)
└── runtime.txt                   # Versión de Python
```


## Funcionalidades
- CRUD de productos y categorías
- Registro de transacciones
- Calculadora de impuestos (IVA, INC, bolsas plásticas, licores)
- Estadísticas básicas

## Créditos
Proyecto académico desarrollado por el equipo indicado en el historial del repositorio.
