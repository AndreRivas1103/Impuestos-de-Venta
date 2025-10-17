"""
Setup script para la Calculadora de Impuestos de Venta
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="calculadora-impuestos-venta",
    version="2.0.0",
    author="Paull Harry Palacio Goez, Andre Rivas Garcia, Juan Sebastián Villa Rodas, David Taborda Noreña",
    author_email="",
    description="Calculadora de impuestos de venta con interfaz gráfica moderna",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-repo/calculadora-impuestos-venta",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Accounting",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "calculadora-impuestos=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json"],
    },
)
