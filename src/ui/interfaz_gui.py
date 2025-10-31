"""
Interfaz Gráfica para la Calculadora de Impuestos de Venta
Implementada con Kivy
"""

import json
import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.core.window import Window
from kivy.metrics import dp

from src.model.calculadora_impuestos import CalculadoraImpuestos, CategoriaProducto


class CalculadoraImpuestosGUI(App):
    def build(self):
        self.title = "Calculadora de Impuestos de Venta v2.0"
        self.calculadora = CalculadoraImpuestos()
        self.historial_calculos = []
        
        Window.size = (900, 700)
        Window.minimum_width = 700
        Window.minimum_height = 500
        
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        title_label = Label(
            text='[b]Calculadora de Impuestos de Venta[/b]',
            size_hint_y=None,
            height=dp(50),
            markup=True,
            font_size='24sp',
            color=(0.2, 0.4, 0.8, 1)
        )
        main_layout.add_widget(title_label)
        
        accordion = Accordion(orientation='horizontal')
        
        calc_item = AccordionItem(title='[b]Calcular Impuestos[/b]')
        calc_item.add_widget(self.crear_panel_calculo())
        accordion.add_widget(calc_item)
        
        info_item = AccordionItem(title='[b]Información de Impuestos[/b]')
        info_item.add_widget(self.crear_panel_informacion())
        accordion.add_widget(info_item)
        
        history_item = AccordionItem(title='[b]Historial[/b]')
        history_item.add_widget(self.crear_panel_historial())
        accordion.add_widget(history_item)
        
        help_item = AccordionItem(title='[b]Ayuda[/b]')
        help_item.add_widget(self.crear_panel_ayuda())
        accordion.add_widget(help_item)
        
        main_layout.add_widget(accordion)
        
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
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        valor_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        valor_layout.add_widget(Label(text='Valor Base ($):', size_hint_x=0.3))
        self.valor_input = __import__('kivy.uix.textinput', fromlist=['TextInput']).TextInput(
            hint_text='Ingrese el valor del producto',
            multiline=False,
            input_filter='float',
            size_hint_x=0.7
        )
        valor_layout.add_widget(self.valor_input)
        layout.add_widget(valor_layout)
        
        categoria_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        categoria_layout.add_widget(Label(text='Categoría:', size_hint_x=0.3))
        
        self.categoria_spinner = Spinner(
            text='Seleccione una categoría',
            values=self.calculadora.obtener_categorias_disponibles(),
            size_hint_x=0.7
        )
        categoria_layout.add_widget(self.categoria_spinner)
        layout.add_widget(categoria_layout)
        
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
        scroll = ScrollView()
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
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
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
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
        
        self.historial_scroll = ScrollView()
        self.historial_layout = BoxLayout(
            orientation='vertical', 
            padding=dp(10), 
            spacing=dp(5), 
            size_hint_y=None
        )
        self.historial_layout.bind(minimum_height=self.historial_layout.setter('height'))
        
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
        try:
            if not self.valor_input.text.strip():
                self.mostrar_error("Por favor, ingrese un valor base")
                return
            
            if self.categoria_spinner.text == 'Seleccione una categoría':
                self.mostrar_error("Por favor, seleccione una categoría")
                return
            
            valor_base = float(self.valor_input.text)
            categoria_nombre = self.categoria_spinner.text
            
            categoria = None
            for cat in CategoriaProducto:
                if cat.value == categoria_nombre:
                    categoria = cat
                    break
            
            if categoria is None:
                self.mostrar_error("Categoría no válida")
                return
            
            resultado = self.calculadora.calcular_impuestos(valor_base, categoria)
            self.agregar_al_historial(resultado)
            self.mostrar_resultados(resultado)
            
        except ValueError as e:
            self.mostrar_error(f"Error en los datos ingresados: {str(e)}")
        except Exception as e:
            self.mostrar_error(f"Error inesperado: {str(e)}")
    
    def mostrar_resultados(self, resultado):
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
        popup = Popup(
            title='Error',
            content=Label(text=mensaje, text_size=(300, None), halign='center'),
            size_hint=(0.6, 0.4)
        )
        popup.open()
    
    def limpiar_campos(self, instance):
        self.valor_input.text = ''
        self.categoria_spinner.text = 'Seleccione una categoría'
        self.resultado_label.text = 'Ingrese los datos y presione "Calcular"'
    
    def agregar_al_historial(self, resultado):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entrada_historial = {
            'timestamp': timestamp,
            'resultado': resultado
        }
        self.historial_calculos.append(entrada_historial)
        self.actualizar_historial_display()
    
    def actualizar_historial_display(self):
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
        if not self.historial_calculos:
            self.mostrar_error("No hay historial para exportar")
            return
        
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"historial_impuestos_{timestamp}.json"
            
            contenido = {
                'fecha_exportacion': datetime.datetime.now().isoformat(),
                'total_calculos': len(self.historial_calculos),
                'calculos': self.historial_calculos
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(contenido, f, indent=2, ensure_ascii=False)
            
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
        if not self.historial_calculos:
            self.mostrar_error("El historial ya está vacío")
            return
        
        self.historial_calculos.clear()
        self.actualizar_historial_display()
        self.mostrar_mensaje("Historial limpiado exitosamente")
    
    def mostrar_mensaje(self, mensaje: str):
        popup = Popup(
            title='Información',
            content=Label(text=mensaje, text_size=(300, None), halign='center'),
            size_hint=(0.6, 0.3)
        )
        popup.open()


def main():
    try:
        CalculadoraImpuestosGUI().run()
    except Exception as e:
        print(f"Error al ejecutar la aplicación: {e}")


if __name__ == "__main__":
    main()


