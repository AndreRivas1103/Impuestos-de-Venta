# Impuestos de Venta

## Descripción
Esta aplicacion permite al usuario calcular los impuestos que debe pagar segun su compra, cuando este realice una compra pueda saber cuanto es el impuesto que debe a menos que este excepto de impuestos, y este debera calcular y mostrar de acuerdo si es por bolsas plasticas, renta a los licores, INC o el IVA.
La aplicacion devolvera los calculos de estos y mostrar el valor total a pagar esperado

### Requisitos
- Asegurate de tener Python 3.6 o superior (si no lo tienes descargalo aquí: [Python.org](https://www.python.org/downloads/))


## Estructura del Proyecto

```
Impuestos-de-Venta/
│
├── docs/
│   └── Libro de excel - Casos de prueba - Andre y Paull.xlsx
│
├── src/
│   ├── app/
│   │   ├── main.py                 # Entrada CLI (consola)
│   │   └── main_database.py        # Entrada CLI con base de datos
│   ├── config/
│   │   └── config.py               # Configuración global
│   ├── db/
│   │   └── database.py             # Capa de acceso a datos (SQLite)
│   ├── model/
│   │   └── calculadora_impuestos.py
│   └── ui/
│       ├── interfaz_consola.py     # Interfaz de consola
│       ├── interfaz_database.py    # Interfaz de consola para BD
│       └── interfaz_gui.py         # Interfaz gráfica (Kivy)
│
├── tests/
│   ├── __init__.py
│   └── test_calculadora_impuestos.py
│
├── build_executable.py
├── setup.py
└── README.md
```


### Pasos para ejecutar

#### Interfaz de Consola (sin base de datos)
1. Descargar o clonar el proyecto
2. Abrir una terminal en la carpeta del proyecto
3. Ejecutar:
   ```bash
   python src/app/main.py
   ```

#### Interfaz de Consola con Base de Datos
```bash
python src/app/main_database.py
```

#### Interfaz Gráfica (GUI con Kivy)
1. Instalar dependencias mínimas:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecutar la GUI:
   ```bash
   python src/ui/interfaz_gui.py
   ```

### Ejecutar pruebas
```bash
python -m unittest tests/test_calculadora_impuestos.py
```

### Generar Ejecutable para Windows
Para crear un ejecutable independiente de Windows:

1. Instalar PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Ejecutar el script de build:
   ```bash
   python build_executable.py
   ```

3. El ejecutable se generará en la carpeta `dist/CalculadoraImpuestos/`

## Características

- Cálculo automático de impuestos según la categoría del producto
- Múltiples tipos de impuestos:
  - Exento o Excluido (no paga ningún impuesto)
  - IVA (5% o 19%)
  - Impuesto Nacional al Consumo (INC)
  - Impuesto de Rentas a los Licores
  - Impuesto de Bolsas Plásticas
- Interfaz de consola 
- Interfaz gráfica moderna con Kivy
- Pruebas unitarias
- Control de excepciones y mensajes de error amigables
- Código limpio y bien documentado 


## Autores
Este proyecto esta siendo realizado por: 
- Paull Harry Palacio Goez 
- Andre Rivas Garcia

Interfaz gráfica realizada por:
- Juan Sebastián Villa Rodas
- David Taborda Noreña


## Link de Audio Explicativo sobre el tema

[Audio Google Drive](https://drive.google.com/drive/folders/1fSU6wTmUQqWg4ZMv37Z1zxNohdVUYFGI?usp=drive_link)

## Codigos

1. [Interfaz de Consola](src/ui/interfaz_consola.py)
2. [Interfaz de Base de Datos](src/ui/interfaz_database.py)
3. [Interfaz Gráfica Kivy](src/ui/interfaz_gui.py)
4. [Calculadora de Impuestos](src/model/calculadora_impuestos.py)
5. [Pruebas](tests/test_calculadora_impuestos.py)

---

## Práctica 4 - Bases de Datos (SQLite)

### Descripción
Sistema completo de gestión de productos e impuestos utilizando SQLite con un modelo ORM simple. Integra la calculadora de impuestos con operaciones CRUD completas y un flujo de ventas.

### Funcionalidades implementadas
- **Crear tablas**: `categorias`, `productos`, `impuestos_adicionales`, `transacciones`.
- **INSERT**: `insertar_categoria`, `insertar_producto`, `insertar_impuesto_adicional`, `insertar_transaccion`.
- **UPDATE**: `actualizar_producto`, `actualizar_categoria`.
- **DELETE**: `eliminar_producto`, `eliminar_categoria`.
- **SELECT**: `consultar_todos_productos`, `consultar_producto_por_id`, `consultar_productos_por_categoria`, `consultar_todas_categorias`, `consultar_transacciones_recientes`.

### Estructura de la base de datos
- Tabla `categorias(id, nombre UNIQUE, descripcion, tasa_iva, fecha_creacion)`
- Tabla `productos(id, nombre, descripcion, precio_base>0, categoria_id FK, estado, fechas)`
- Tabla `impuestos_adicionales(id, nombre UNIQUE, tasa[0..1], descripcion, aplicable_a_categoria_id FK, activo)`
- Tabla `transacciones(id, producto_id FK, cantidad>0, precio_unitario>0, subtotal, total_impuestos, total_final, fecha)`

### Ejecutar la app con base de datos
```bash
python src/app/main_database.py
```

### Ejecutar pruebas de base de datos
```bash
python -m unittest test_database.py -v
```

### Interfaz de usuario (consola BD)
-  Gestionar Productos (agregar, listar, buscar, actualizar, eliminar, por categoría)
-  Gestionar Categorías (agregar, listar, actualizar, eliminar)
-  Gestionar Transacciones (registrar venta, ver recientes, calcular impuestos para venta)
-  Ver Estadísticas (resumen y agregados)
-  Calculadora de Impuestos (standalone)

### Características del ORM
- Clase `BaseDatos` centraliza conexión, operaciones y manejo de errores
- Integridad referencial habilitada (PRAGMA foreign_keys = ON)
- Índices para consultas frecuentes y constraints para validación
- Conexión/desconexión segura por operación y transacciones con rollback en error

### Estructura (módulos BD)
```
src/
  ├── db/
  │   └── database.py                # ORM y operaciones CRUD
  ├── ui/
  │   └── interfaz_database.py       # Interfaz de consola para BD
  └── app/
      └── main_database.py           # Entrada principal BD
test_database.py                      # Pruebas CRUD y de flujo
```
