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
from Estructura.Menu.Ayuda import BoxAyuda
from Estructura.Menu.Configuracion import BoxConfiguracion
from Estructura.Menu.Registros import BoxRegistros
from Estructura.Menu.Empleados import BoxEmpleados
from Estructura.Menu.Productos import BoxProductos
from Estructura.Estetica.portada import BoxDefault
from Estructura.Estetica.EstiloMenu import BoxSlideMenu
kivy.require('1.9.0')


class BoxIndex(NavigationDrawer):
    
    def __init__(self):
        super(BoxIndex, self).__init__()

        #Estilos del menu Lateral
        self.anim_type = 'slide_above_anim'
        self.defaultContainer = BoxDefault(self)


        #Componentes del menu Lateral
        menuEmpleados = Button(text='Empleados')
        menuEmpleados.color = (1,1,1,1)
        menuEmpleados.size_hint_max_y = 70
        menuEmpleados.bind(on_release=lambda *arg: self.cambiar_container(1))

        menuProductos = Button(text='Productos')
        menuProductos.color = (1,1,1,1)
        menuProductos.size_hint_max_y = 70
        menuProductos.bind(on_release=lambda *arg: self.cambiar_container(2))

        menuRegistros = Button(text='Registros')
        menuRegistros.color = (1,1,1,1)
        menuRegistros.size_hint_max_y = 70
        menuRegistros.bind(on_release=lambda *arg: self.cambiar_container(3))

        menuConfiguracion = Button(text='Configuracion')
        menuConfiguracion.color = (1,1,1,1)
        menuConfiguracion.size_hint_max_y = 70
        menuConfiguracion.bind(on_release=lambda *arg: self.cambiar_container(4))

        menuAyuda = Button(text='Ayuda')
        menuAyuda.color = (1,1,1,1)
        menuAyuda.size_hint_max_y = 70
        menuAyuda.bind(on_release=lambda *arg: self.cambiar_container(5))

        

        side_panel = BoxSlideMenu()
        side_panel.add_widget(menuEmpleados)
        side_panel.add_widget(menuProductos)
        side_panel.add_widget(menuRegistros)
        side_panel.add_widget(menuConfiguracion)
        side_panel.add_widget(menuAyuda)
        side_panel.add_widget(BoxLayout())
        self.add_widget(side_panel)

        #Componentes de la Vista Principal
        
        self.add_widget(self.defaultContainer)

    def cambiar_container(self,selected=0, *arg):
        
        if selected == 0:
            self.remove_widget(self.defaultContainer)
            self.defaultContainer = BoxDefault(self)
            self.add_widget(BoxDefault(self))
        elif selected == 1:
            self.remove_widget(self.defaultContainer)
            self.defaultContainer = BoxEmpleados(self)
            self.add_widget(self.defaultContainer)
        elif selected == 2:
            self.remove_widget(self.defaultContainer)
            self.defaultContainer = BoxProductos(self)
            self.add_widget(self.defaultContainer)
        elif selected == 3:
            self.remove_widget(self.defaultContainer)
            self.defaultContainer = BoxRegistros(self)
            self.add_widget(self.defaultContainer)
        elif selected == 4:
            self.remove_widget(self.defaultContainer)
            self.defaultContainer = BoxConfiguracion(self)
            self.add_widget(self.defaultContainer)
        elif selected == 5:
            self.remove_widget(self.defaultContainer)
            self.defaultContainer = BoxAyuda(self)
            self.add_widget(self.defaultContainer)