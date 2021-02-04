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
from navigationdrawer import NavigationDrawer
import re

from Sqlconexion import Sqlconexion, hash_password, verify_password
from Estructura.SubAcciones.BoxDetails import BoxDetails
from Estructura.Estetica.portada import ScreenContainer
from Estructura.VistaEmergente.PopupContainer import PopUpContainer
from Estructura.VistaEmergente.PopupContainer import FileBox
#from Estructura.Menu.Productos import BoxProductos
kivy.require('1.9.0')

#Contenido de las Tarjestas
class BoxCard(BoxLayout):

    def __init__(self, election_menu, BoxIndex, **kwargs):
        super(BoxCard, self).__init__(**kwargs)
        
        self.Menu = BoxIndex
        self.__section_menu = election_menu
        self.__contenido_detalles = None
  

    def set_carta_empleados(self, titulo, precio, cantidad, fecha, rol, detalles, img='img/perfil-empleado.jpg'):
        
        diccionario = {
            'id': detalles[0],
            'cedula': detalles[1],
            'nombre': detalles[2],
            'cargo': detalles[3],
            'fecha': detalles[5],
            'img': img
        }
        #Layout de la Imagen de la Carta
        img_card_box = ImgCardBox()
        img_card_box.set_imgCard(img)
        
        #Layout del Contenido de la Carta
        contenido_card_box = ContainerCardBox()
        contenido_card_box.set_containerCard(titulo,rol,precio, cantidad, fecha)
        
        #Button de Detalle de la Carta
        btnDetalles = Button(text='Detalles')
        btnDetalles.size_hint_max_x = 65
        btnDetalles.bind(on_release=lambda *arg: self.btn_details_screen(diccionario, 'Detalles'))
        
        self.add_widget(img_card_box)
        self.add_widget(contenido_card_box)
        self.add_widget(btnDetalles)
        
    def set_carta_Productos(self, titulo, precio, cantidad, fecha, rol, detalles, img='img/default-productos.jpg'):

        diccionario = {
            'id': detalles[0],
            'codigo':detalles[1],
            'nombre': detalles[2],
            'categoria': detalles[3],
            'cantidad': detalles[4],
            'precio': detalles[5],
            'peso': detalles[6],
            'img': detalles[7],
        }
        #Layout de la Imagen de la Carta
        img_card_box = ImgCardBox()
        img_card_box.set_imgCard(img)
        
        #Layout del Contenido de la Carta
        contenido_card_box = ContainerCardBox()
        contenido_card_box.set_containerCard(titulo,rol,precio, cantidad, fecha)

        #Button de Detalle de la Carta
        btnDetalles = Button(text='Detalles')
        btnDetalles.size_hint_max_x = 65
        btnDetalles.bind(on_release=lambda *arg: self.btn_details_screen(diccionario, 'Detalles'))
        
        self.add_widget(img_card_box)
        self.add_widget(contenido_card_box)
        self.add_widget(btnDetalles)

    def btn_details_screen(self, detalles, name_screen, *arg):
        
        pantalla_Contenedor_detalles = ScreenContainer()
        ScreenDetalles = Screen(name=name_screen)
        ScreenDetalles.add_widget(BoxDetails(self.Menu, detalles))

        pantalla_Contenedor_detalles.setScreenDetalles(ScreenDetalles)
        self.__section_menu.clear_widgets()
        self.__section_menu.add_widget(pantalla_Contenedor_detalles)

class ImgCardBox(BoxLayout):
    imgCard = StringProperty('')

    def set_imgCard(self,ruta):
        self.imgCard = ruta
class ContainerCardBox(BoxLayout):
    titulo = StringProperty('')
            
    def set_containerCard(self, titulo, rol, precio, cantidad, fecha):

        self.titulo = titulo
        self.rol = Label(text=rol)
        self.precio = Label(text=precio)
        self.cantidad = Label(text=cantidad)
        self.fecha = Label(text=fecha)

        if self.rol is not None or '':
            self.rol.color = [0,0,0,1]
            self.add_widget(self.rol)

        if self.precio is not None or '':
            self.precio.color = [0,0,0,1]
            self.add_widget(self.precio)

        if self.cantidad is not None or '':
            self.cantidad.color = [0,0,0,1]
            self.add_widget(self.cantidad)

        if self.fecha is not None or '':
            self.fecha.color = [0,0,0,1]
            self.add_widget(self.fecha)
#Contenido de las Tarjestas

#Estilo para el contenedor de Insertar Productos
class BoxInsertProducts(BoxLayout):
    codigo = StringProperty()
    nombre_categoria = StringProperty()
    show_popUp = None

    def __init__(self, data_produc, contenedor_padre, **kwargs):
        super(BoxInsertProducts, self).__init__(**kwargs)

        self.codigo = str(data_produc[0])
        self.nombre_categoria = str(data_produc[2])
        self.__contenedor_p = contenedor_padre
        

    def btn_insert_product(self, code, nombre_p, categoria_p, cantidad_p, precio_p, peso_p, img_p):

        code = self.codigo
        categoria_p = self.nombre_categoria
        #print(re.match(r'^[0-9]\.{0,1}[0-9]+', precio_p))
        #print(re.search(r'[a-zA-z]', precio_p))

        if self.show_popUp is not None : 
            print(self.show_popUp.get_ruta_imgSelec())
            img_p = self.show_popUp.get_ruta_imgSelec()

        error = []
        if code is None or code =='' or len(code)==0:
            error.append('Introdusca un codigo para el producto.')
        
        if nombre_p is None or nombre_p =='' or len(nombre_p)==0:
            error.append('Se requiere de un nombre de prod.')

        if categoria_p is None or categoria_p =='' or len(categoria_p)==0:
            error.append('Se requiere de una categoria Existente.')

        if cantidad_p is None or cantidad_p=='' or len(cantidad_p)==0 or re.match(r'^([\s\d]+)$', cantidad_p) is None:

            error.append('La cantidad debe ser mayor a 0.')
        
        if (precio_p is None or precio_p=='' or len(precio_p)==0 
        or re.search(r'[a-zA-z]', precio_p) is not None 
        or re.match(r'^[0-9]\.{0,1}[0-9]+', precio_p) is None):
            
            error.append('Formato incorrecto eje: 2.4')

        if (peso_p is not None and peso_p!='' and len(peso_p)!=0):
            
            if re.match(r'^([\s\d]+)$', peso_p) is None:
                error.append('El peso debe de ser mayor a 0.')

        if img_p is None or img_p =='' or len(img_p)==0:
            img_p = 'img/default-productos.jpg'

        
        print(error)
        if error == []:
            #Codigo para insertar producto
            print('insertar producto')
            con = Sqlconexion()
            conexion = con.create_DataBase()
            producto = (code, nombre_p, categoria_p, cantidad_p, precio_p, peso_p, img_p)
            con.sql_insert_detelles_productos(conexion,producto)
            con.close_db(conexion)

            show = PopUpContainer(self)
            pop_up_window = Popup(title='Producto Agregado', content=show, size_hint=(None, None), size=(self.size[0]/1.4,self.size[1]/3))
            show.error_popup('Proceso realizado con Exito.')
            if show.button_cerrar is not None:
                show.button_cerrar.bind(on_release=lambda *arg: self.volver_contenedor_padre(self.__contenedor_p, pop_up_window))
            pop_up_window.open()
        else:
            show = PopUpContainer(self)
            pop_up_window = Popup(title='Hubo un Error', content=show, size_hint=(None, None), size=(self.size[0]/1.4,self.size[1]/3))

            if len(error) > 2:
                show.error_popup(error[0],error[1])
            else:
                show.error_popup(error[0])
            if show.button_cerrar is not None:
                show.button_cerrar.bind(on_release=lambda *arg: pop_up_window.dismiss())
            pop_up_window.open()

    def volver_contenedor_padre(self, contenedor, popUp):
        popUp.dismiss()
        contenedor.regresar()
        print('Entro en el volver al menu principal')
        print(contenedor)
        #contenedor.regresar()

        #self.clear_widgets()
        #self.add_widget(contenedor)

    def btn_chooser_file_P(self):

        self.show_popUp = PopUpContainer(self)
        pop_up_window = Popup(title='Selecione Imagen', content=self.show_popUp, size_hint=(None, None), size=(self.size[0]/1.15,self.size[1]/1.3))
        self.show_popUp.btn_chooser_file_estandar()
        if self.show_popUp.button_cerrar is not None:
            self.show_popUp.button_cerrar.bind(on_release=lambda *arg: pop_up_window.dismiss())
        pop_up_window.open()      