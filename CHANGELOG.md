# Changelog - Calculadora de Impuestos de Venta

## Versión 2.0.0 - Interfaz Gráfica Moderna

### ✅ Completado

#### 🎨 Interfaz Gráfica (GUI con Kivy)
- **Interfaz moderna y amigable** implementada con Kivy
- **Pestañas organizadas**: Cálculo, Información, Historial, Ayuda
- **Validación en tiempo real** de datos de entrada
- **Mensajes de error amigables** con emojis y descripciones claras
- **Diseño responsivo** que se adapta al tamaño de ventana

#### 📊 Funcionalidades Extra
- **Historial de cálculos** con timestamp
- **Exportación de historial** a archivo JSON
- **Limpieza de historial** con confirmación
- **Visualización de últimos 10 cálculos**
- **Interfaz de pestañas** para mejor organización

#### 🛡️ Control de Excepciones
- **Validación robusta** de tipos de datos
- **Mensajes de error específicos** para cada tipo de problema
- **Manejo de valores límite** (muy pequeños, muy grandes)
- **Redondeo consistente** a 2 decimales
- **Validación de categorías** y valores de entrada

#### 🧹 Código Limpio
- **Documentación completa** con docstrings
- **Separación de responsabilidades** (Modelo, Vista, Controlador)
- **Constantes organizadas** en archivo de configuración
- **Manejo de errores consistente** en toda la aplicación
- **Comentarios explicativos** en código complejo

#### 🧪 Pruebas Unitarias
- **11 pruebas unitarias** que cubren casos normales, extraordinarios y de error
- **Todas las pruebas pasando** después de las mejoras
- **Cobertura completa** de la lógica de negocio
- **Validación de redondeo** y cálculos precisos

#### 📦 Ejecutable para Windows
- **Script de build automatizado** (`build_executable.py`)
- **Configuración de PyInstaller** optimizada
- **Instalador simple** con instrucciones
- **Dependencias incluidas** en el ejecutable
- **Archivos de documentación** incluidos

#### 📚 Documentación
- **README actualizado** con instrucciones completas
- **Instrucciones de instalación** para GUI y ejecutable
- **Información del equipo** de desarrollo
- **Ejemplos de uso** y características
- **Changelog detallado** de mejoras

### 🔧 Mejoras Técnicas

#### Arquitectura
- **Patrón MVC** implementado correctamente
- **Separación clara** entre lógica de negocio y presentación
- **Configuración centralizada** en `config.py`
- **Manejo de dependencias** con `requirements.txt`

#### Interfaz de Usuario
- **Diseño moderno** con colores y tipografía consistentes
- **Navegación intuitiva** con pestañas
- **Feedback visual** para acciones del usuario
- **Responsive design** que funciona en diferentes tamaños

#### Funcionalidad
- **Cálculos precisos** con redondeo consistente
- **Historial persistente** durante la sesión
- **Exportación de datos** para análisis posterior
- **Validación robusta** de entrada de datos

### 👥 Equipo de Desarrollo

#### Backend y Lógica de Negocio
- **Paull Harry Palacio Goez**
- **Andre Rivas Garcia**

#### Interfaz Gráfica
- **Juan Sebastián Villa Rodas**
- **David Taborda Noreña**

#### Testing y QA
- **Equipo completo**

### 🚀 Instrucciones de Uso

#### Interfaz de Consola
```bash
python main.py
```

#### Interfaz Gráfica
```bash
pip install kivy
python src/view/interfaz_gui.py
```

#### Generar Ejecutable
```bash
pip install pyinstaller
python build_executable.py
```

#### Ejecutar Pruebas
```bash
python test/test_calculadora_impuestos.py
```

### 📈 Próximas Mejoras Sugeridas

1. **Base de datos** para persistencia del historial
2. **Reportes en PDF** de los cálculos
3. **Configuración de impuestos** personalizable
4. **Temas visuales** adicionales
5. **Integración con APIs** de impuestos actualizados
6. **Versión web** de la aplicación
7. **Aplicación móvil** con KivyMD

---

**Fecha de Release**: Diciembre 2024  
**Versión**: 2.0.0  
**Estado**: ✅ Completado y Funcional
