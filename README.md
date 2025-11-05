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
├── app_web/                         # Aplicación Web Flask (MVC)
│   ├── controllers/                 # Controladores (Blueprints)
│   │   ├── home_controller.py
│   │   ├── productos_controller.py
│   │   ├── categorias_controller.py
│   │   ├── transacciones_controller.py
│   │   ├── calculadora_controller.py
│   │   └── estadisticas_controller.py
│   ├── views/                       # Templates HTML
│   │   ├── base.html
│   │   ├── home/
│   │   ├── productos/
│   │   ├── categorias/
│   │   ├── transacciones/
│   │   ├── calculadora/
│   │   └── estadisticas/
│   ├── static/                      # Archivos estáticos (CSS, JS)
│   │   └── css/
│   └── __init__.py                  # Factory de Flask
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
│   │   ├── calculadora_impuestos.py
│   │   ├── producto.py
│   │   ├── categoria.py
│   │   └── transaccion.py
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
├── run_web.py                       # Script para ejecutar la app web
├── setup.py
└── README.md
```


### Pasos para ejecutar

## 🌐 Aplicación Web (Flask)

La aplicación web proporciona todas las funcionalidades de gestión de productos, categorías, transacciones y cálculo de impuestos a través de una interfaz web moderna.

#### Requisitos Previos
1. Python 3.7 o superior
2. Base de datos SQLite (se crea automáticamente)

#### Instalación y Ejecución

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar la aplicación web:**
   ```bash
   python run_web.py
   ```

3. **Abrir en el navegador:**
   - La aplicación estará disponible en: `http://localhost:5000`
   - O en: `http://127.0.0.1:5000`

#### Configuración Inicial de la Base de Datos

Si es la primera vez que ejecuta la aplicación o necesita una base de datos en blanco:

1. Acceda a la página principal en `http://localhost:5000`
2. En el menú de inicio, encontrará la sección "Configuración de Base de Datos"
3. Haga clic en **"Crear Tablas"** para crear todas las tablas necesarias
4. (Opcional) Haga clic en **"Inicializar Datos de Ejemplo"** para cargar datos de prueba

#### Funcionalidades Web Disponibles

- **Menú de Inicio**: Acceso a todas las funcionalidades y configuración de BD
- **Gestión de Productos**: 
  - ✅ Listar todos los productos
  - ✅ Buscar producto por ID
  - ✅ Crear nuevo producto
  - ✅ Modificar producto existente
  - ✅ Eliminar producto
- **Gestión de Categorías**:
  - ✅ Listar todas las categorías
  - ✅ Buscar categoría por ID
  - ✅ Crear nueva categoría
  - ✅ Modificar categoría existente
  - ✅ Eliminar categoría
- **Transacciones**:
  - ✅ Listar transacciones recientes
  - ✅ Registrar nueva transacción de venta
- **Calculadora de Impuestos**: Cálculo interactivo de impuestos
- **Estadísticas y Consultas Avanzadas**:
  - Productos más caros
  - Productos más baratos
  - Ventas por categoría
  - Productos por estado

#### Estructura MVC

La aplicación web sigue el patrón **Model-View-Controller (MVC)** con Blueprints de Flask:

- **Model**: `src/model/` - Clases de dominio (Producto, Categoria, Transaccion, CalculadoraImpuestos)
- **View**: `app_web/views/` - Templates HTML (Jinja2)
- **Controller**: `app_web/controllers/` - Blueprints de Flask que manejan las rutas

#### Despliegue en Producción

Para desplegar la aplicación web en plataformas como Heroku, Railway, Render, o cualquier servidor:

1. **Instalar gunicorn para producción:**
   ```bash
   pip install gunicorn
   ```

2. **Crear un archivo `Procfile` (para Heroku/Railway):**
   ```
   web: gunicorn run_web:app --bind 0.0.0.0:$PORT
   ```
   
   O para ejecutar directamente con Python:
   ```
   web: python run_web.py
   ```

3. **Variables de entorno (opcional):**
   - `FLASK_ENV`: `production` o `development`
   - `PORT`: Puerto donde correrá la aplicación (algunas plataformas lo asignan automáticamente)

4. **Base de datos:**
   - La aplicación usa SQLite por defecto (`calculadora_impuestos.db`)
   - Para producción, considere usar PostgreSQL o MySQL para mejor rendimiento
   - Asegúrese de que el archivo de BD tenga permisos de escritura

5. **Ejemplo de despliegue en Railway:**
   - Conecte su repositorio GitHub
   - Railway detectará automáticamente Python
   - Configure el comando de inicio: `python run_web.py`
   - La aplicación estará disponible en la URL proporcionada por Railway

6. **Ejemplo de despliegue en Render:**
   - Conecte su repositorio
   - Configure el servicio como "Web Service"
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python run_web.py`

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

### Ejecutar pruebas unitarias
```bash
python -m unittest tests/test_calculadora_impuestos.py
```

**Nota**: Las pruebas unitarias no tienen llamados directos a la base de datos ni instrucciones SQL, solo prueban la lógica de negocio de la calculadora de impuestos.

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
