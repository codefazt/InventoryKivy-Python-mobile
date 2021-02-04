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
from kivy.uix.button import Button
from kivy.uix.actionbar import ActionBar
from kivy.uix.screenmanager import (CardTransition, FadeTransition,
                                    RiseInTransition, ScreenManager,
                                    WipeTransition, Screen)
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from navigationdrawer import NavigationDrawer
from Estructura.VistaEmergente.PopupContainer import PopUpContainer
from Sqlconexion import Sqlconexion, hash_password, verify_password
kivy.require('1.9.0')

class BoxDetails(BoxLayout):
    img_detalle = StringProperty('')
    
    def __init__(self, BoxIndex, informacion, **kwargs):
        super(BoxDetails, self).__init__(**kwargs)
        
        self.__con = Sqlconexion()
        self.__conexion = self.__con.create_DataBase()
        
        self.info = informacion
        self.img_detalle = self.info['img']
        self.Menu = BoxIndex
        print(self.info)

        contenedor_grid = self.ids.grid_contenedor_id

        self.organizador_grids('Producto: ', self.info['nombre'], self.ids.grid_contenedor_id)
        self.organizador_grids('Codigo: ', 'ART-' + self.info['codigo'], self.ids.grid_contenedor_id)
        self.organizador_grids('Categoria: ', self.info['categoria'], self.ids.grid_contenedor_id)

        if self.info['cantidad'] == '':
            self.organizador_grids('Peso: ', self.info['peso'], self.ids.grid_contenedor_id)
        
        if self.info['peso'] == '':
            self.organizador_grids('Cantidad: ', self.info['cantidad'], self.ids.grid_contenedor_id)
        
        self.organizador_grids('Precio Actual: ', self.info['precio'] + ' $', self.ids.grid_contenedor_id) 

        #Botones para actualizar  y Eliminar
        btn_actualizar_producto = Button()
        btn_actualizar_producto.text = 'Actualizar'
        btn_actualizar_producto.background_normal = './img/editar_productos.png'

        btn_actualizar_producto.bind(on_release=lambda *arg: print('Actualizar'))


    def btn_editar_producto(self):
        self.remove_widget(self.children[0])
        edit_p_layout = BoxInsertProductsDetails(self.info, self)
        self.add_widget(edit_p_layout)

        pass

    def select_contenido_detalle(self, informacion, conexion):
        
        if informacion is not None:
            if informacion['categoria'] is not None:
                
                codigo = informacion['codigo']
                query = 'SELECT * FROM detelles_productos WHERE categoria = {0} AND codigo = "{1}"'.format(informacion["categoria"], codigo)
                detalle_producto = self.__con.fetch_one_with_query(conexion, query)
    
    def organizador_grids(self, titular, descripcion, grid_layout):

        categoria = Label(text=titular)
        categoria.color = [0,0,0,1]

        elemento = Label(text=descripcion)
        elemento.color = [0,0,0,1]

        grid_layout.add_widget(categoria)
        grid_layout.add_widget(elemento)
        

#Estilo para el contenedor de Insertar Productos
class BoxInsertProductsDetails(BoxLayout):
    codigo = StringProperty()
    nombre_producto = StringProperty()
    nombre_categoria = StringProperty()
    cantidad = StringProperty()
    peso = StringProperty()
    precio = StringProperty()

    show_popUp = None

    def __init__(self, data_produc, contenedor_padre, **kwargs):
        super(BoxInsertProductsDetails, self).__init__(**kwargs)

        self.codigo = str(data_produc['id'])
        self.nombre_producto = data_produc['nombre']
        self.nombre_categoria = str(data_produc['categoria'])
        self.cantidad = data_produc['cantidad']
        self.peso = data_produc['peso']
        self.precio = str(data_produc['precio'])
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
            print('Actualizar producto')
            con = Sqlconexion()
            conexion = con.create_DataBase()
            producto = (code, nombre_p, categoria_p, cantidad_p, precio_p, peso_p, img_p)
            #con.sql_insert_detelles_productos(conexion,producto) Cambiar por update_detelles_productos
            con.close_db(conexion)

            show = PopUpContainer(self)
            pop_up_window = Popup(title='Producto Actualizado', content=show, size_hint=(None, None), size=(self.size[0]/1.4,self.size[1]/3))
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