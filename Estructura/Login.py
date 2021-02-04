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
#from kivy.garden.navigationdrawer import NavigationDrawer
from navigationdrawer import NavigationDrawer

from Sqlconexion import Sqlconexion, hash_password, verify_password
from Estructura.VistaEmergente.PopupContainer import PopUpContainer
from Estructura.Index import BoxIndex
kivy.require('1.9.0')


class BoxLogin(BoxLayout):
    def __init__(self, MainView, **kwargs):
        super(BoxLogin, self).__init__(**kwargs)
        self.__con = Sqlconexion()
        self.__conexion = self.__con.create_DataBase()

        self.MainPantalla = MainView

        usuarios = self.__con.sql_fetch('User', self.__conexion)

        if usuarios is None or usuarios == []:
            User = ['admin','Administrador', 1, 'admin', date.today()]
            self.__con.sql_insert(self.__conexion, User)
   
    def verificarUser(self, usuario, password, *arg):

        if (password != '' and password != None) and (usuario != '' and usuario != None):
            
            resultado = self.__con.fetch_one(self.__conexion, 'User', 'cedula', usuario)

            if not resultado:
                show = PopUpContainer(self)
                pop_up_window = Popup(title='Error Usuario Inexistente', content=show, size_hint=(None, None), size=(self.size[0]/1.4,self.size[1]/3))
                show.error_popup("Datos Erroneos","Por favor vuelva a intentar")
                if show.button_cerrar is not None:
                    show.button_cerrar.bind(on_release=lambda *arg: pop_up_window.dismiss())
                pop_up_window.open()
                return False
            else:

                if verify_password(resultado[0][4], password):
                    
                    index = BoxIndex()
                    pantallaIndex = Screen(name='Index')
                    pantallaIndex.add_widget(index)
                    self.MainPantalla.add_widget(pantallaIndex)
                    self.MainPantalla.current = 'Index'

                else:
                    return False
                
        else:

            #print(self.size[0]/1.2,self.size[1]/1.2)
            show = PopUpContainer(self)
            pop_up_window = Popup(title='Error Campos Vacios', content=show, size_hint=(None, None), size=(self.size[0]/1.5,self.size[1]/3))
            show.error_popup("Por favor Ingrese algun dato")
            if show.button_cerrar is not None:
                show.button_cerrar.bind(on_release=lambda *arg: pop_up_window.dismiss())
            pop_up_window.open()
            return False
    
    def __insert_user(self, conexion, User):
        self.__con.sql_insert(conexion, User)  
    
    def __insert_productos(self, conexion, producto):
        self.__con.sql_insert_producto(conexion, producto)  