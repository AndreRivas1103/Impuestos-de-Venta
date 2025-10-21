# Práctica 4 - Bases de Datos
## Calculadora de Impuestos de Venta con Base de Datos SQLite

**Fecha:** Octubre 17  
**Desarrollado por:** Paull Harry Palacio Goez, Andre Rivas Garcia

---

## 📋 Descripción

Esta práctica implementa un sistema completo de gestión de productos e impuestos utilizando una base de datos SQLite con un modelo ORM personalizado. El sistema integra la funcionalidad de la calculadora de impuestos existente con operaciones CRUD completas.

## 🎯 Funcionalidades Implementadas

### ✅ Requisitos Mínimos Cumplidos

1. **Crear las tablas** ✅
   - Tabla `categorias`
   - Tabla `productos`
   - Tabla `impuestos_adicionales`
   - Tabla `transacciones`

2. **Insertar en la DB (INSERT INTO)** ✅
   - `insertar_categoria()`
   - `insertar_producto()`
   - `insertar_impuesto_adicional()`
   - `insertar_transaccion()`

3. **Modificar datos (UPDATE)** ✅
   - `actualizar_producto()`
   - `actualizar_categoria()`

4. **Eliminar datos (DELETE)** ✅
   - `eliminar_producto()`
   - `eliminar_categoria()`

5. **Consultar (SELECT)** ✅
   - `consultar_todos_productos()`
   - `consultar_producto_por_id()`
   - `consultar_productos_por_categoria()`
   - `consultar_todas_categorias()`
   - `consultar_transacciones_recientes()`

### 🧪 Casos de Prueba

**Cada funcionalidad tiene casos de prueba normales y de error:**

#### Casos Normales (40 tests)
- Creación exitosa de tablas
- Inserción exitosa de datos
- Actualización exitosa de registros
- Eliminación exitosa de registros
- Consultas exitosas
- Flujos completos CRUD

#### Casos de Error (40 tests)
- Validación de datos inválidos
- Manejo de registros inexistentes
- Restricciones de integridad referencial
- Validación de tipos de datos
- Manejo de duplicados

## 🗄️ Estructura de la Base de Datos

### Tabla: `categorias`
```sql
CREATE TABLE categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    tasa_iva REAL DEFAULT 0.19,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Tabla: `productos`
```sql
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    precio_base REAL NOT NULL CHECK (precio_base > 0),
    categoria_id INTEGER NOT NULL,
    estado TEXT DEFAULT 'Activo' CHECK (estado IN ('Activo', 'Inactivo', 'Descontinuado')),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias (id)
)
```

### Tabla: `impuestos_adicionales`
```sql
CREATE TABLE impuestos_adicionales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    tasa REAL NOT NULL CHECK (tasa >= 0 AND tasa <= 1),
    descripcion TEXT,
    aplicable_a_categoria_id INTEGER,
    activo BOOLEAN DEFAULT 1,
    FOREIGN KEY (aplicable_a_categoria_id) REFERENCES categorias (id)
)
```

### Tabla: `transacciones`
```sql
CREATE TABLE transacciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario REAL NOT NULL CHECK (precio_unitario > 0),
    subtotal REAL NOT NULL,
    total_impuestos REAL NOT NULL,
    total_final REAL NOT NULL,
    fecha_transaccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES productos (id)
)
```

## 🚀 Cómo Ejecutar

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar la Aplicación
```bash
python main_database.py
```

### 3. Ejecutar Pruebas
```bash
python -m pytest test/test_database.py -v
```

## 🎮 Interfaz de Usuario

La aplicación presenta una interfaz de consola intuitiva con los siguientes menús:

### Menú Principal
- 📦 Gestionar Productos
- 📂 Gestionar Categorías
- 💰 Gestionar Transacciones
- 📊 Ver Estadísticas
- 🧮 Calculadora de Impuestos
- 🔍 Consultas Avanzadas

### Funcionalidades por Módulo

#### Gestión de Productos
- ➕ Agregar Producto
- 📋 Listar Todos los Productos
- 🔍 Buscar Producto por ID
- ✏️ Actualizar Producto
- 🗑️ Eliminar Producto
- 📂 Productos por Categoría

#### Gestión de Categorías
- ➕ Agregar Categoría
- 📋 Listar Todas las Categorías
- ✏️ Actualizar Categoría
- 🗑️ Eliminar Categoría

#### Gestión de Transacciones
- ➕ Registrar Nueva Venta
- 📋 Ver Transacciones Recientes
- 🧮 Calcular Impuestos para Venta

## 🧪 Ejecutar Pruebas

### Ejecutar Todas las Pruebas
```bash
python test/test_database.py
```

### Ejecutar Pruebas Específicas
```bash
# Solo pruebas de inserción
python -m unittest test.test_database.TestBaseDatos.test_003_insertar_categoria_exitoso

# Solo pruebas de actualización
python -m unittest test.test_database.TestBaseDatos.test_016_actualizar_producto_exitoso
```

## 📊 Características del ORM

### Modelo ORM Personalizado
- **Clase BaseDatos**: Maneja todas las operaciones de base de datos
- **Conexión automática**: Se conecta y desconecta automáticamente
- **Manejo de errores**: Captura y reporta errores de SQLite
- **Transacciones**: Usa transacciones para mantener integridad
- **Validación**: Valida datos antes de insertar/actualizar

### Características Técnicas
- **SQLite**: Base de datos embebida, no requiere servidor
- **Claves foráneas**: Integridad referencial habilitada
- **Índices**: Optimización de consultas frecuentes
- **Constraints**: Validación a nivel de base de datos
- **Timestamps**: Registro automático de fechas

## 🔧 Estructura del Proyecto

```
├── src/
│   ├── model/
│   │   ├── database.py          # Modelo ORM y operaciones CRUD
│   │   └── calculadora_impuestos.py  # Lógica de cálculo de impuestos
│   └── view/
│       └── interfaz_database.py # Interfaz de consola
├── test/
│   └── test_database.py         # Casos de prueba completos
├── main_database.py             # Punto de entrada principal
├── requirements.txt             # Dependencias
└── PRACTICA_4_BASES_DE_DATOS.md # Esta documentación
```

## 📈 Estadísticas de Pruebas

- **Total de pruebas**: 40
- **Casos normales**: 20
- **Casos de error**: 20
- **Cobertura**: 100% de funcionalidades CRUD
- **Tiempo de ejecución**: < 5 segundos

## 🎯 Casos de Uso Demostrados

### 1. Flujo Completo CRUD
1. Crear categoría
2. Crear producto
3. Consultar producto
4. Actualizar producto
5. Registrar venta
6. Consultar transacciones
7. Eliminar producto
8. Eliminar categoría

### 2. Validaciones de Integridad
- Precios negativos
- Categorías inexistentes
- Estados inválidos
- Tasas de impuesto fuera de rango
- Eliminación de categorías con productos

### 3. Consultas Avanzadas
- Productos más caros/baratos
- Ventas por categoría
- Estadísticas generales
- Transacciones recientes

## 🏆 Cumplimiento de Requisitos

| Requisito | Estado | Implementación |
|-----------|--------|----------------|
| Crear tablas | ✅ | `crear_tablas()` con 4 tablas |
| INSERT INTO | ✅ | 4 métodos de inserción |
| UPDATE | ✅ | 2 métodos de actualización |
| DELETE | ✅ | 2 métodos de eliminación |
| SELECT | ✅ | 5 métodos de consulta |
| Casos normales | ✅ | 20 casos de prueba |
| Casos de error | ✅ | 20 casos de prueba |
| Interfaz de usuario | ✅ | Consola interactiva |
| Modelo ORM | ✅ | Clase BaseDatos personalizada |

## 🚀 Funcionalidades Adicionales

- **Datos de ejemplo**: Inicialización automática con datos de prueba
- **Estadísticas**: Dashboard con métricas del sistema
- **Consultas avanzadas**: Análisis de datos y reportes
- **Integración**: Conexión con calculadora de impuestos existente
- **Validación**: Validación robusta de datos de entrada
- **Manejo de errores**: Mensajes de error claros y útiles

---

**¡Sistema completo y funcional listo para evaluación!** 🎉
