"""
Script para generar ejecutable de Windows usando PyInstaller
Calculadora de Impuestos de Venta
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def instalar_dependencias():
    """Instala las dependencias necesarias para el build"""
    print("📦 Instalando dependencias...")
    
    dependencias = [
        "pyinstaller",
        "kivy",
        "kivymd"  # Para mejor UI
    ]
    
    for dep in dependencias:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} instalado correctamente")
        except subprocess.CalledProcessError:
            print(f"❌ Error instalando {dep}")

def limpiar_builds_anteriores():
    """Limpia builds anteriores"""
    print("🧹 Limpiando builds anteriores...")
    
    carpetas_a_limpiar = ["build", "dist", "__pycache__"]
    archivos_a_limpiar = ["*.spec"]
    
    for carpeta in carpetas_a_limpiar:
        if os.path.exists(carpeta):
            shutil.rmtree(carpeta)
            print(f"🗑️ Eliminada carpeta: {carpeta}")
    
    # Limpiar archivos .spec
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"🗑️ Eliminado archivo: {spec_file}")

def crear_especificacion_pyinstaller():
    """Crea el archivo .spec para PyInstaller"""
    print("📝 Creando especificación de PyInstaller...")
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/ui/interfaz_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/model', 'src/model'),
        ('src/db', 'src/db'),
        ('src/ui', 'src/ui'),
        ('tests', 'tests'),
        ('docs', 'docs'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'kivy',
        'kivy.app',
        'kivy.uix',
        'kivy.core',
        'kivy.graphics',
        'kivy.metrics',
        'kivy.clock',
        'kivy.core.window',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CalculadoraImpuestos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin consola para la GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Puedes agregar un icono aquí
)
'''
    
    with open("CalculadoraImpuestos.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("✅ Especificación creada: CalculadoraImpuestos.spec")

def generar_ejecutable():
    """Genera el ejecutable usando PyInstaller"""
    print("🔨 Generando ejecutable...")
    
    try:
        # Usar el archivo .spec
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller", 
            "--clean", 
            "CalculadoraImpuestos.spec"
        ])
        print("✅ Ejecutable generado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generando ejecutable: {e}")
        return False

def crear_instalador():
    """Crea un instalador simple"""
    print("📦 Creando instalador...")
    
    # Crear carpeta de distribución
    dist_folder = Path("dist/CalculadoraImpuestos")
    if not dist_folder.exists():
        dist_folder.mkdir(parents=True)
    
    # Copiar archivos adicionales
    archivos_adicionales = [
        "README.md",
        "requirements.txt"
    ]
    
    for archivo in archivos_adicionales:
        if os.path.exists(archivo):
            shutil.copy2(archivo, dist_folder)
            print(f"📄 Copiado: {archivo}")
    
    # Crear script de instalación
    install_script = '''@echo off
echo Instalando Calculadora de Impuestos de Venta...
echo.
echo Este programa calcula impuestos de venta para diferentes categorias de productos.
echo.
echo Desarrollado por:
echo - Paull Harry Palacio Goez
echo - Andre Rivas Garcia
echo - Juan Sebastian Villa Rodas
echo - David Taborda Norena
echo.
echo Presione cualquier tecla para continuar...
pause > nul
echo.
echo Instalacion completada!
echo.
echo Para ejecutar el programa, haga doble clic en:
echo CalculadoraImpuestos.exe
echo.
pause
'''
    
    with open(dist_folder / "INSTALAR.bat", "w", encoding="utf-8") as f:
        f.write(install_script)
    
    print("✅ Instalador creado")

def main():
    """Función principal del script de build"""
    print("🚀 Iniciando proceso de build para Windows...")
    print("=" * 60)
    
    try:
        # Paso 1: Instalar dependencias
        instalar_dependencias()
        print()
        
        # Paso 2: Limpiar builds anteriores
        limpiar_builds_anteriores()
        print()
        
        # Paso 3: Crear especificación
        crear_especificacion_pyinstaller()
        print()
        
        # Paso 4: Generar ejecutable
        if generar_ejecutable():
            print()
            # Paso 5: Crear instalador
            crear_instalador()
            print()
            print("🎉 ¡Build completado exitosamente!")
            print("📁 El ejecutable se encuentra en: dist/CalculadoraImpuestos/")
            print("💡 Para distribuir, comprima la carpeta 'dist/CalculadoraImpuestos'")
        else:
            print("❌ Build falló. Revisa los errores anteriores.")
            
    except Exception as e:
        print(f"❌ Error durante el build: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
