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
from Estructura.VistaEmergente.PopupContainer import PopUpContainer
from Estructura.Estetica.EstiloBoxCard import BoxCard
from Estructura.Estetica.EstiloMenu import BoxContainer
from Estructura.Estetica.portada import ScreenContainer
kivy.require('1.9.0')

class BoxEmpleados(BoxLayout):
    def __init__(self, BoxIndex, **kwargs):
        super(BoxEmpleados, self).__init__(**kwargs)
        
        self.__con = Sqlconexion()
        self.__conexion = self.__con.create_DataBase()
        self.Menu = BoxIndex
        
        #Lista de usuarios
        self.fetch_empleados(self.__conexion)
        

    def fetch_empleados(self, conexion, *arg):
        
        lista_usaurios = self.__con.sql_fetch("User", conexion)
        container = BoxContainer()
        pantallaContainer = ScreenContainer()
        limitador = 5
        
        for usuario in lista_usaurios:
            
            if limitador >= 0:
                cargo = 'Empleado'
                if usuario[3] == 1:
                    cargo = 'Administrador'
                    
                tarjeta = BoxCard(self, self.Menu)
                tarjeta.set_carta_empleados(str(usuario[2]),'','',str(usuario[5]), cargo, usuario)
                container.add_widget(tarjeta)
                limitador-=1
        
        container.add_widget(BoxLayout())
        pantallaContainer.setScreenEmpleado(container)
        self.add_widget(pantallaContainer)
        pass