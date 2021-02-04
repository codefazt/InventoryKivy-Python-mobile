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
from Sqlconexion import Sqlconexion, hash_password, verify_password
kivy.require('1.9.0')

class PopUpContainer(FloatLayout):
    
    ventana_file = None
    pop_up = None
    button_cerrar = Button()

    def __init__(self, contenedor_padre, **kwargs):
        super(PopUpContainer, self).__init__(**kwargs)
        
        self.contenedor_p = contenedor_padre
        self.__con = Sqlconexion()
        self.__conexion = self.__con.create_DataBase()
    
    def insert_categoria(self, conexion, categoria_selected):
    
        self.clear_widgets()
        #Etiqueta
        label_txt = Label(text='Ingrese Categoria:')
        label_txt.size_hint = (1, 0.2)
        label_txt.pos_hint = {"x":0, "top": 0.9}

        #Input para agregar Categoria
        self.__txt_new_produc = TextInput()
        self.__txt_new_produc.multiline = False
        self.__txt_new_produc.size_hint = (0.8, 0.15)
        self.__txt_new_produc.pos_hint = {"x":0.1, "top": 0.65}
        self.__txt_new_produc.font_size = 30

        #Boton para guardar Categoria
        btn_categoria = Button(text='Crear')
        btn_categoria.size_hint = (0.8, 0.15)
        btn_categoria.pos_hint = {"x":0.1, "top": 0.48}
        btn_categoria.bind(on_release=lambda *arg: self.btn_insert_categoria(categoria_selected))

        #Boton seleccion de archivo
        btn_select_file = Button(text='Agregar Imagen')
        btn_select_file.size_hint = (0.8, 0.15)
        btn_select_file.pos_hint = {"x":0.1, "top": 0.28}
        btn_select_file.bind(on_release=lambda *arg: self.btn_chooser_file())

        self.add_widget(label_txt)
        self.add_widget(self.__txt_new_produc)
        self.add_widget(btn_categoria)
        self.add_widget(btn_select_file)
        pass
          
    def btn_insert_categoria(self, categoria_selected, *arg):

        if ((self.__txt_new_produc and self.ventana_file) is not None and 
        (self.__txt_new_produc and self.ventana_file) != ''):
            img = ''

            if self.ventana_file is not None:
                img = self.ventana_file.get_img()

            categoria = (self.__txt_new_produc.text, categoria_selected, img)
            self.__con.sql_insert_categoria(self.__conexion, categoria)
            self.__txt_new_produc.text = ''

            self.fetch_categorias(self.__conexion, categoria_selected)
            #Cerrar este Pop y abrir el de fetch_categorias
        else:
            show = PopUpContainer(self)
            pop_up_window = Popup(title='Advertencia Categoria', content=show, size_hint=(None, None), size=(self.size[0]/1.3,self.size[1]/2))
            show.error_popup("*Nombre la Categoria.", '*Seleccione una Img de fondo')
            if show.button_cerrar is not None:
                show.button_cerrar.bind(on_release=lambda *arg: pop_up_window.dismiss())
            pop_up_window.open()

    #Boton para Abrir Archivo de Productos
    def btn_chooser_file(self):
        self.ventana_file = FileBox()
        self.ventana_file.size_hint = (1, 1)
        self.ventana_file.pos_hint = {"x":0, "top": 1}
        self.add_widget(self.ventana_file)

    #Boton para Abrir Archivo Generico
    def btn_chooser_file_estandar(self):
        self.ventana_file = FileBox()
        self.ventana_file.btn_generar(self.button_cerrar)
        self.ventana_file.size_hint = (1, 1)
        self.ventana_file.pos_hint = {"x":0, "top": 1}
        self.add_widget(self.ventana_file)

    def fetch_categorias(self, conexion, categoria):
        self.clear_widgets()
        #Etiqueta de Lista de Categorias
        label_txt = Label(text='Categorias disponibles:')
        label_txt.size_hint = (1, 0.1)
        label_txt.pos_hint = {"x":0, "top": 1}

        #consulta a la base de datos para buscar la lista segun la categoria Alimneto o Ropas
        lista_categorias = self.__con.fetch_one_with_query(conexion,'SELECT id, nombre, img FROM categorias WHERE categoria={0}'.format(int(categoria)))
        #Creacion de El GridLayout para posicionar la lista
        self._contenedor_categorias = BoxCategoria(cols=2)
        self._contenedor_categorias.size_hint = (1,0.8)
        self._contenedor_categorias.pos_hint = {"x":0, "y": 0.10}
        self._contenedor_categorias.spacing = 10

        self._pag_inicial = 0
        self._pag_max = 3
        self._len_Lista_max = 1
        self.listar_categoria(lista_categorias, categoria)
        
        #botones para la paginacion
        paginacion_layout = BoxLayout()
        paginacion_layout.size_hint = (1,0.07)
        paginacion_layout.pos_hint = {"x":0, "y": 0}

        btn_pag_atras = Button(text='Atras')
        btn_pag_atras.bind(on_release=lambda *arg: self.paginacion_accion(lista_categorias, categoria, len(lista_categorias), 0))

        btn_pag_Sig = Button(text='Siguiente')
        btn_pag_Sig.bind(on_release=lambda *arg: self.paginacion_accion(lista_categorias, categoria, len(lista_categorias), 3))

        paginacion_layout.add_widget(btn_pag_atras)
        paginacion_layout.add_widget(btn_pag_Sig)

        self.add_widget(label_txt)
        self.add_widget(self._contenedor_categorias)
        self.add_widget(paginacion_layout)
    
    def id_categotia_select(self, id_categoria, *arg):

        self.pop_up.dismiss()
        self.contenedor_p.remove_widget(self.contenedor_p.children[0])
        self.contenedor_p.fetch_productos(self.__conexion, id_categoria)
        

    
    def listar_categoria(self, lista_categorias, tipo_categoria):

        contador = self._pag_inicial
        btn_categoria = None
        inicio = 0
        for item in lista_categorias:

            if self._pag_inicial <= inicio:
                
                if contador < self._pag_max :
                    btn_categoria = Button(text=item[1])
                    btn_categoria.background_color = (1,1,1,1)
                    btn_categoria.color = (0.2, 0.2, 0.2, 1)
                    btn_categoria.background_normal = item[2]
                    btn_categoria.border = (26,26,26,26)
                    btn_categoria.bind(on_press=lambda x, id=item[0]: self.id_categotia_select(id))
                    self._contenedor_categorias.add_widget(btn_categoria)
                    contador+=1

                    if contador == self._pag_max:
                        continue

            inicio += 1

        #boton para agregar mas categorias
        btn_add_categoria = Button(text='+')
        btn_add_categoria.font_size = 50
        btn_add_categoria.bind(on_release=lambda *arg: self.insert_categoria(self.__conexion, tipo_categoria))
        self._contenedor_categorias.add_widget(btn_add_categoria)

    def paginacion_accion(self, lista_categorias, tipo_categoria, len_lista, pag_final):
        self._contenedor_categorias.clear_widgets()

        if pag_final == 3 :

            if len_lista/3 > self._len_Lista_max:
                self._pag_inicial = self._pag_max
                self._pag_max += pag_final
                self._len_Lista_max += 1
        
        elif pag_final == 0 and self._pag_inicial == 0:
            self._pag_inicial = 0
            self._pag_max = 3
        
        elif pag_final == 0 and self._pag_inicial != 0:
            self._pag_inicial -= 3
            self._pag_max -= 3
            self._len_Lista_max -= 1



        self.listar_categoria(lista_categorias, tipo_categoria)
        
    def get_ruta_imgSelec(self):
        return self.ventana_file.get_img()


    #Ventana de Error
    def error_popup(self, texto_error, texto_auxilar=None):

        self.clear_widgets()

        #Etiqueta
        label_txt = Label(text=texto_error)
        label_txt.size_hint = (1, 0.2)
        label_txt.pos_hint = {"x":0, "top": 0.9}
        #Boton para guardar Categoria
        btn_categoria = Button(text='Cerrar')
        btn_categoria.size_hint = (0.8, 0.35)
        btn_categoria.pos_hint = {"x":0.1, "top": 0.45}
        self.button_cerrar = btn_categoria
        
        self.add_widget(label_txt)
        if texto_auxilar is not None:
            #Etiqueta
            label_txt_aux = Label(text=texto_auxilar)
            label_txt_aux.size_hint = (1, 0.2)
            label_txt_aux.pos_hint = {"x":0, "top": 0.7}
            self.add_widget(label_txt_aux)

        self.add_widget(self.button_cerrar)
        pass

# Seccion de Estilos
class BoxCategoria(GridLayout):
    pass
# Box para Files
class FileBox(BoxLayout):
    
    __ruta_img = ''
    __img = ''

    def __init__(self, **kwargs):
        super(FileBox, self).__init__(**kwargs)

        self.__btn_guardar_img = Button()
        self.__btn_guardar_img.text = 'Guardar Imagen'
        self.__btn_guardar_img.size_hint = (1, 0.15)
        self.__btn_guardar_img.bind(on_release=lambda *arg: self.guardar_img(self.__img))
        self.add_widget(self.__btn_guardar_img)

    def selected(self,filename):

        if filename is not None and filename != []:
            self.__img = filename[0]
            self.ids.image.source = filename[0]
    
    def guardar_img(self, img):
        
        self.__ruta_img = img
        self.clear_widgets()    
        self.size_hint_y = 0

    def btn_generar(self,button):

        self.remove_widget(self.__btn_guardar_img)
        self.__btn_guardar_img = Button()
        self.__btn_guardar_img.text = 'Guardar Imagen'
        self.__btn_guardar_img.size_hint = (1, 0.15)
        self.__btn_guardar_img.bind(on_release=lambda *arg: self.guardar_y_cerrar_img(self.__img, button))
        self.add_widget(self.__btn_guardar_img)

    def guardar_y_cerrar_img(self, img, button):
        
        self.__ruta_img = img
        self.remove_widget(self.__btn_guardar_img)
        button.text = 'Cerrar'
        button.size_hint = (1, 0.15)
        self.add_widget(button)
        

    def get_img(self):
        return self.__ruta_img