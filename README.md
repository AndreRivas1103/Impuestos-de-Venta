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
│   ├── controller/                            
│   ├── model/                                 
│   │   └── calculadora_impuestos.py           
│   └── view/                                  
│       └── interfaz_consola.py                
│
├── test/                                      
│   └── test_calculadora_impuestos.py          
│
├── main.py                                    
└── README.md                                  
```


### Pasos para ejecutar

#### Interfaz de Consola
1. Descargar o clonar el proyecto
2. Abrir una terminal(Bash, Simbolo del Sistema, etc.) en la carpeta del proyecto
3. Ejecutar el programa principal:
   ```bash
   python main.py
   ```
   
   O alternativamente:
   ```bash
   python src/view/interfaz_consola.py
   ```

#### Interfaz Gráfica (GUI con Kivy)
1. Instalar las dependencias necesarias:
   ```bash
   pip install kivy
   ```
   
2. Ejecutar la interfaz gráfica:
   ```bash
   python src/view/interfaz_gui.py
   ```

### Ejecutar pruebas
```bash
python test/test_calculadora_impuestos.py
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

## Equipo de Desarrollo
- **Backend y Lógica de Negocio**: Paull Harry Palacio Goez, Andre Rivas Garcia
- **Interfaz Gráfica**: Juan Sebastián Villa Rodas, David Taborda Noreña
- **Testing y QA**: Equipo completo


## Link de Audio Explicativo sobre el tema

[Audio Google Drive](https://drive.google.com/drive/folders/1fSU6wTmUQqWg4ZMv37Z1zxNohdVUYFGI?usp=drive_link)

## Codigos

1. [Interfaz de Consola](src/view/interfaz_consola.py)
2. [Calculadora de Impuestos](src/model/calculadora_impuestos.py)
3. [Test Calculadora de Impuestos de Venta](test/test_calculadora_impuestos.py)
