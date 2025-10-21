"""
Interfaz Gráfica para la Calculadora de Impuestos de Venta
Implementada con Kivy para una experiencia de usuario moderna y amigable
"""

import sys
import os
import json
import datetime
from typing import List, Dict

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.textinput import TextInput

from calculadora_impuestos import CalculadoraImpuestos, CategoriaProducto


class CalculadoraImpuestosGUI(App):
    """Aplicación principal de la interfaz gráfica"""
    
    def build(self):
        """Construye la interfaz principal"""
        self.title = "Calculadora de Impuestos de Venta v2.0"
        self.calculadora = CalculadoraImpuestos()
        self.historial_calculos = []  # Lista para almacenar el historial
        
        # Configurar tamaño de ventana
        Window.size = (900, 700)
        Window.minimum_width = 700
        Window.minimum_height = 500
        
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Título principal
        title_label = Label(
            text='[b]Calculadora de Impuestos de Venta[/b]',
            size_hint_y=None,
            height=dp(50),
            markup=True,
            font_size='24sp',
            color=(0.2, 0.4, 0.8, 1)
        )
        main_layout.add_widget(title_label)
        
        # Crear pestañas
        accordion = Accordion(orientation='horizontal')
        
        # Pestaña de cálculo
        calc_item = AccordionItem(title='[b]Calcular Impuestos[/b]')
        calc_item.add_widget(self.crear_panel_calculo())
        accordion.add_widget(calc_item)
        
        # Pestaña de información
        info_item = AccordionItem(title='[b]Información de Impuestos[/b]')
        info_item.add_widget(self.crear_panel_informacion())
        accordion.add_widget(info_item)
        
        # Pestaña de historial
        history_item = AccordionItem(title='[b]Historial[/b]')
        history_item.add_widget(self.crear_panel_historial())
        accordion.add_widget(history_item)
        
        # Pestaña de ayuda
        help_item = AccordionItem(title='[b]Ayuda[/b]')
        help_item.add_widget(self.crear_panel_ayuda())
        accordion.add_widget(help_item)
        
        main_layout.add_widget(accordion)
        
        # Panel de resultados
        self.resultado_label = Label(
            text='Ingrese los datos y presione "Calcular"',
            size_hint_y=None,
            height=dp(100),
            text_size=(None, None),
            halign='center',
            valign='middle',
            markup=True
        )
        main_layout.add_widget(self.resultado_label)
        
        return main_layout
    
    def crear_panel_calculo(self):
        """Crea el panel principal de cálculo"""
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Campo de valor base
        valor_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        valor_layout.add_widget(Label(text='Valor Base ($):', size_hint_x=0.3))
        self.valor_input = TextInput(
            hint_text='Ingrese el valor del producto',
            multiline=False,
            input_filter='float',
            size_hint_x=0.7
        )
        valor_layout.add_widget(self.valor_input)
        layout.add_widget(valor_layout)
        
        # Campo de categoría
        categoria_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        categoria_layout.add_widget(Label(text='Categoría:', size_hint_x=0.3))
        
        self.categoria_spinner = Spinner(
            text='Seleccione una categoría',
            values=self.calculadora.obtener_categorias_disponibles(),
            size_hint_x=0.7
        )
        categoria_layout.add_widget(self.categoria_spinner)
        layout.add_widget(categoria_layout)
        
        # Botones
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        
        calcular_btn = Button(
            text='[b]Calcular Impuestos[/b]',
            markup=True,
            background_color=(0.2, 0.7, 0.3, 1)
        )
        calcular_btn.bind(on_press=self.calcular_impuestos)
        button_layout.add_widget(calcular_btn)
        
        limpiar_btn = Button(
            text='[b]Limpiar[/b]',
            markup=True,
            background_color=(0.7, 0.2, 0.2, 1)
        )
        limpiar_btn.bind(on_press=self.limpiar_campos)
        button_layout.add_widget(limpiar_btn)
        
        layout.add_widget(button_layout)
        
        return layout
    
    def crear_panel_informacion(self):
        """Crea el panel de información sobre impuestos"""
        scroll = ScrollView()
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        # Información general
        info_label = Label(
            text='[b]Información sobre Impuestos[/b]\n\n'
                 'Esta aplicación calcula automáticamente los impuestos aplicables según la categoría del producto:\n\n'
                 '[b]• Alimentos Básicos:[/b] IVA 5%\n'
                 '[b]• Licores:[/b] IVA 19% + Impuesto de Rentas a los Licores (25%)\n'
                 '[b]• Bolsas Plásticas:[/b] IVA 19% + Impuesto de Bolsas Plásticas (20%)\n'
                 '[b]• Combustibles:[/b] IVA 19% + Impuesto Nacional al Consumo (8%)\n'
                 '[b]• Servicios Públicos:[/b] Exento de impuestos\n'
                 '[b]• Otros:[/b] IVA 19%\n\n'
                 '[b]Nota:[/b] Los impuestos se calculan sobre el valor base del producto.',
            text_size=(None, None),
            halign='left',
            valign='top',
            markup=True,
            size_hint_y=None
        )
        info_label.bind(texture_size=info_label.setter('size'))
        layout.add_widget(info_label)
        
        scroll.add_widget(layout)
        return scroll
    
    def crear_panel_ayuda(self):
        """Crea el panel de ayuda"""
        scroll = ScrollView()
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        ayuda_label = Label(
            text='[b]Guía de Uso[/b]\n\n'
                 '[b]1. Calcular Impuestos:[/b]\n'
                 '   • Ingrese el valor base del producto\n'
                 '   • Seleccione la categoría correspondiente\n'
                 '   • Presione "Calcular Impuestos"\n\n'
                 '[b]2. Interpretar Resultados:[/b]\n'
                 '   • El resultado muestra el desglose completo\n'
                 '   • Incluye cada impuesto aplicable\n'
                 '   • Muestra el valor total a pagar\n\n'
                 '[b]3. Funciones Adicionales:[/b]\n'
                 '   • Use "Limpiar" para borrar los campos\n'
                 '   • Consulte la pestaña "Información" para detalles\n\n'
                 '[b]Desarrollado por:[/b]\n'
                 'Juan Sebastián Villa Rodas\n'
                 'David Taborda Noreña',
            text_size=(None, None),
            halign='left',
            valign='top',
            markup=True,
            size_hint_y=None
        )
        ayuda_label.bind(texture_size=ayuda_label.setter('size'))
        layout.add_widget(ayuda_label)
        
        scroll.add_widget(layout)
        return scroll
    
    def crear_panel_historial(self):
        """Crea el panel de historial de cálculos"""
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Botones de control del historial
        control_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(10))
        
        exportar_btn = Button(
            text='[b]Exportar Historial[/b]',
            markup=True,
            background_color=(0.2, 0.5, 0.8, 1),
            size_hint_x=0.5
        )
        exportar_btn.bind(on_press=self.exportar_historial)
        control_layout.add_widget(exportar_btn)
        
        limpiar_historial_btn = Button(
            text='[b]Limpiar Historial[/b]',
            markup=True,
            background_color=(0.8, 0.2, 0.2, 1),
            size_hint_x=0.5
        )
        limpiar_historial_btn.bind(on_press=self.limpiar_historial)
        control_layout.add_widget(limpiar_historial_btn)
        
        layout.add_widget(control_layout)
        
        # Área de historial
        self.historial_scroll = ScrollView()
        self.historial_layout = BoxLayout(
            orientation='vertical', 
            padding=dp(10), 
            spacing=dp(5), 
            size_hint_y=None
        )
        self.historial_layout.bind(minimum_height=self.historial_layout.setter('height'))
        
        # Mensaje inicial
        self.historial_label = Label(
            text='[b]Historial de Cálculos[/b]\n\nNo hay cálculos realizados aún.',
            text_size=(None, None),
            halign='center',
            valign='top',
            markup=True,
            size_hint_y=None
        )
        self.historial_layout.add_widget(self.historial_label)
        
        self.historial_scroll.add_widget(self.historial_layout)
        layout.add_widget(self.historial_scroll)
        
        return layout
    
    def calcular_impuestos(self, instance):
        """Calcula los impuestos basado en los datos ingresados"""
        try:
            # Validar entrada
            if not self.valor_input.text.strip():
                self.mostrar_error("Por favor, ingrese un valor base")
                return
            
            if self.categoria_spinner.text == 'Seleccione una categoría':
                self.mostrar_error("Por favor, seleccione una categoría")
                return
            
            # Obtener datos
            valor_base = float(self.valor_input.text)
            categoria_nombre = self.categoria_spinner.text
            
            # Convertir nombre a enum
            categoria = None
            for cat in CategoriaProducto:
                if cat.value == categoria_nombre:
                    categoria = cat
                    break
            
            if categoria is None:
                self.mostrar_error("Categoría no válida")
                return
            
            # Calcular impuestos
            resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
            
            # Agregar al historial
            self.agregar_al_historial(resultado)
            
            # Mostrar resultados
            self.mostrar_resultados(resultado)
            
        except ValueError as e:
            self.mostrar_error(f"Error en los datos ingresados: {str(e)}")
        except Exception as e:
            self.mostrar_error(f"Error inesperado: {str(e)}")
    
    def mostrar_resultados(self, resultado):
        """Muestra los resultados del cálculo"""
        texto_resultado = f"[b]RESULTADOS DEL CÁLCULO[/b]\n\n"
        texto_resultado += f"[b]Valor Base:[/b] ${resultado['valor_base']:,.2f}\n"
        texto_resultado += f"[b]Categoría:[/b] {resultado['categoria']}\n\n"
        texto_resultado += f"[b]DESGLOSE DE IMPUESTOS:[/b]\n"
        
        impuestos = resultado['impuestos']
        if not any(impuestos.values()):
            texto_resultado += "• Exento de impuestos\n"
        else:
            for impuesto, valor in impuestos.items():
                if valor > 0:
                    texto_resultado += f"• {impuesto}: ${valor:,.2f}\n"
        
        texto_resultado += f"\n[b]Total Impuestos:[/b] ${resultado['total_impuestos']:,.2f}\n"
        texto_resultado += f"[b]VALOR TOTAL:[/b] ${resultado['valor_total']:,.2f}"
        
        self.resultado_label.text = texto_resultado
    
    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error en un popup"""
        popup = Popup(
            title='Error',
            content=Label(text=mensaje, text_size=(300, None), halign='center'),
            size_hint=(0.6, 0.4)
        )
        popup.open()
    
    def limpiar_campos(self, instance):
        """Limpia todos los campos de entrada"""
        self.valor_input.text = ''
        self.categoria_spinner.text = 'Seleccione una categoría'
        self.resultado_label.text = 'Ingrese los datos y presione "Calcular"'
    
    def agregar_al_historial(self, resultado: Dict):
        """Agrega un cálculo al historial"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entrada_historial = {
            'timestamp': timestamp,
            'resultado': resultado
        }
        self.historial_calculos.append(entrada_historial)
        self.actualizar_historial_display()
    
    def actualizar_historial_display(self):
        """Actualiza la visualización del historial"""
        # Limpiar el layout actual
        self.historial_layout.clear_widgets()
        
        if not self.historial_calculos:
            self.historial_label = Label(
                text='[b]Historial de Cálculos[/b]\n\nNo hay cálculos realizados aún.',
                text_size=(None, None),
                halign='center',
                valign='top',
                markup=True,
                size_hint_y=None
            )
            self.historial_layout.add_widget(self.historial_label)
            return
        
        # Título del historial
        titulo = Label(
            text=f'[b]Historial de Cálculos ({len(self.historial_calculos)} cálculos)[/b]',
            text_size=(None, None),
            halign='center',
            valign='top',
            markup=True,
            size_hint_y=None,
            height=dp(30)
        )
        self.historial_layout.add_widget(titulo)
        
        # Mostrar los últimos 10 cálculos
        for entrada in self.historial_calculos[-10:]:
            resultado = entrada['resultado']
            timestamp = entrada['timestamp']
            
            texto_historial = f"[b]{timestamp}[/b]\n"
            texto_historial += f"Valor Base: ${resultado['valor_base']:,.2f}\n"
            texto_historial += f"Categoría: {resultado['categoria']}\n"
            texto_historial += f"Total: ${resultado['valor_total']:,.2f}\n"
            texto_historial += "-" * 30
            
            label_historial = Label(
                text=texto_historial,
                text_size=(None, None),
                halign='left',
                valign='top',
                markup=True,
                size_hint_y=None,
                height=dp(80)
            )
            self.historial_layout.add_widget(label_historial)
    
    def exportar_historial(self, instance):
        """Exporta el historial a un archivo JSON"""
        if not self.historial_calculos:
            self.mostrar_error("No hay historial para exportar")
            return
        
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"historial_impuestos_{timestamp}.json"
            
            # Crear el contenido del archivo
            contenido = {
                'fecha_exportacion': datetime.datetime.now().isoformat(),
                'total_calculos': len(self.historial_calculos),
                'calculos': self.historial_calculos
            }
            
            # Escribir el archivo
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(contenido, f, indent=2, ensure_ascii=False)
            
            # Mostrar mensaje de éxito
            popup = Popup(
                title='Exportación Exitosa',
                content=Label(
                    text=f'Historial exportado exitosamente a:\n{filename}\n\nTotal de cálculos: {len(self.historial_calculos)}',
                    text_size=(300, None),
                    halign='center'
                ),
                size_hint=(0.6, 0.4)
            )
            popup.open()
            
        except Exception as e:
            self.mostrar_error(f"Error al exportar historial: {str(e)}")
    
    def limpiar_historial(self, instance):
        """Limpia todo el historial de cálculos"""
        if not self.historial_calculos:
            self.mostrar_error("El historial ya está vacío")
            return
        
        # Crear popup de confirmación
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        content.add_widget(Label(
            text=f'¿Está seguro de que desea eliminar\nlos {len(self.historial_calculos)} cálculos del historial?',
            text_size=(300, None),
            halign='center'
        ))
        
        button_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(40))
        
        confirm_btn = Button(text='Confirmar', background_color=(0.8, 0.2, 0.2, 1))
        cancel_btn = Button(text='Cancelar', background_color=(0.2, 0.7, 0.3, 1))
        
        button_layout.add_widget(confirm_btn)
        button_layout.add_widget(cancel_btn)
        content.add_widget(button_layout)
        
        popup = Popup(
            title='Confirmar Eliminación',
            content=content,
            size_hint=(0.6, 0.4)
        )
        
        def confirmar_limpieza(instance):
            self.historial_calculos.clear()
            self.actualizar_historial_display()
            popup.dismiss()
            self.mostrar_mensaje("Historial limpiado exitosamente")
        
        def cancelar_limpieza(instance):
            popup.dismiss()
        
        confirm_btn.bind(on_press=confirmar_limpieza)
        cancel_btn.bind(on_press=cancelar_limpieza)
        
        popup.open()
    
    def mostrar_mensaje(self, mensaje: str):
        """Muestra un mensaje informativo"""
        popup = Popup(
            title='Información',
            content=Label(text=mensaje, text_size=(300, None), halign='center'),
            size_hint=(0.6, 0.3)
        )
        popup.open()


def main():
    """Función principal para ejecutar la GUI"""
    try:
        CalculadoraImpuestosGUI().run()
    except Exception as e:
        print(f"Error al ejecutar la aplicación: {e}")


if __name__ == "__main__":
    main()
