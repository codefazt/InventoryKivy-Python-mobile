import sqlite3
from datetime import date
from kivy.clock import Clock
import kivy
from kivy.app import App

from kivy.properties import NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.actionbar import ActionBar
from kivy.uix.screenmanager import (CardTransition, FadeTransition,
                                    RiseInTransition, ScreenManager,
                                    WipeTransition, Screen)
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from Sqlconexion import Sqlconexion, hash_password, verify_password
from Estructura.VistaEmergente.PopupContainer import PopUpContainer
from Estructura.Estetica.EstiloBoxCard import BoxCard
from Estructura.Estetica.EstiloBoxCard import BoxInsertProducts
from Estructura.Estetica.EstiloMenu import BoxContainer
kivy.require('1.9.0')

class BoxProductos(BoxLayout):

    __eleccion = 0
    Menu = None
    def __init__(self, BoxIndex, **kwargs):
        super(BoxProductos, self).__init__(**kwargs)
        self.Menu = BoxIndex
        self.__con = Sqlconexion()
        self.__conexion = self.__con.create_DataBase()

        #Seleccion del tipo de productos        
        self.__caja_botones = BoxLayout()
        
        #configuracion de la Caja_botones
        self.__caja_botones.padding = 15
        self.__caja_botones.spacing = 10
        self.__caja_botones.orientation = 'vertical'
        #configuracion de la Caja_botones
        
        self.btnAlimentos = Button(text='Lista de Alimentos')
        self.btnAlimentos.background_normal = 'img/categoria_alimentos.jpg'
        self.btnAlimentos.bind(on_release=lambda *arg: self.show_pop_up(self.__conexion, '0'))
        
        self.btnRopa = Button(text='Prendas disponibles')
        self.btnRopa.background_normal = 'img/categoria_ropa.png'
        self.btnRopa.bind(on_release=lambda *arg: self.show_pop_up(self.__conexion, '1'))
        
        self.__caja_botones.add_widget(self.btnAlimentos)
        self.__caja_botones.add_widget(self.btnRopa)
        self.add_widget(self.__caja_botones)


    def show_pop_up(self, conexion, categoria, *arg):
        
        eleccion = int(categoria)
        lista_productos = self.__con.sql_fetch_with_param('categorias', conexion, 'categoria', eleccion)
               
        if lista_productos == [] or lista_productos is None:
            #Crea un Popup para insertar la categoria
            show = PopUpContainer(self)
            pop_up_window = Popup(title='Insertar Producto', content=show, size_hint=(None, None), size=(self.size[0]/1.15,self.size[1]/1.3))
            show.insert_categoria(conexion, eleccion)
            show.pop_up = pop_up_window
            pop_up_window.open()
        
        else:
            #Crea un Popup para listar las categorias
            show = PopUpContainer(self)
            pop_up_window = Popup(title='Lista de Productos', content=show, size_hint=(None, None), size=(self.size[0]/1.15,self.size[1]/1.3))
            show.fetch_categorias(conexion, categoria)
            show.pop_up = pop_up_window
            pop_up_window.open()   
             
    def fetch_productos(self, conexion, categoria, contenedor=None, *arg):
        
        self.__eleccion = categoria
        #lista_productos = self.__con.sql_fetch_with_param("productos", conexion, 'categoria', self.__eleccion)
        lista_productos = self.__con.sql_fetch_with_param("detelles_productos", conexion, 'codigo', self.__eleccion)
        container = BoxContainer()
        limitador = 4
        
        if lista_productos is not None and lista_productos != []:

            for producto in lista_productos:
                
                if limitador >= 0:
                        
                    tarjeta = BoxCard(self, self.Menu)
                    tarjeta.set_carta_Productos('ART-' + str(producto[0]), producto[3], producto[2], producto[4], str(producto[5])+'$', producto, producto[7])
                    container.add_widget(tarjeta)
                    limitador-=1

            container.add_widget(BoxLayout())
        else:
            Layout_not_found = BoxLayout()
            Layout_not_found.add_widget(Label(text='No hay Resultados.'))
            
            container.add_widget(Layout_not_found)

        self.add_widget(container)

    def regresar(self):
        self.remove_widget(self.children[0])
        
        self.__con = Sqlconexion()
        self.__conexion = self.__con.create_DataBase()
        self.__eleccion = 0
        #Seleccion del tipo de productos        
        self.__caja_botones = BoxLayout()
        
        #configuracion de la Caja_botones
        self.__caja_botones.padding = 15
        self.__caja_botones.spacing = 10
        self.__caja_botones.orientation = 'vertical'
        #configuracion de la Caja_botones
        
        self.btnAlimentos = Button(text='Lista de Alimentos')
        self.btnAlimentos.background_normal = 'img/categoria_alimentos.jpg'
        self.btnAlimentos.bind(on_release=lambda *arg: self.show_pop_up(self.__conexion, '0'))
        
        self.btnRopa = Button(text='Prendas disponibles')
        self.btnRopa.background_normal = 'img/categoria_ropa.png'
        self.btnRopa.bind(on_release=lambda *arg: self.show_pop_up(self.__conexion, '1'))
        
        self.__caja_botones.add_widget(self.btnAlimentos)
        self.__caja_botones.add_widget(self.btnRopa)
        self.add_widget(self.__caja_botones)

    def incluir_producto(self):

        if self.__eleccion is not None and self.__eleccion > 0:
            self.remove_widget(self.children[0])

            categoria_selected = self.__con.sql_fetch_with_param('categorias',self.__conexion,'id', self.__eleccion)
            #Contenedor para Introducir productos
            contenedor_Insert_product = BoxInsertProducts(categoria_selected[0], self)
            self.add_widget(contenedor_Insert_product)
            #self.ids.btn_incluir.text = 'Incluir'
            print(self.ids)
        else:
            print('Seleccione una Categoria')
        
class ModelProducto():

    id=None
    codigo=''
    nombre=''
    categoria=''
    cantidad=0
    peso=0
    foto=''
    