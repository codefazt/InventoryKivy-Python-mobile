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

class BoxLogoPrincipal(BoxLayout):
    pass

class BoxDefault(BoxLayout):
    def __init__(self, BoxIndex, **kwargs):
        super(BoxDefault, self).__init__(**kwargs)

        self.index = BoxIndex

class ScreenContainer(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenContainer, self).__init__(**kwargs)
        self.transition = RiseInTransition()
        
    def setScreenEmpleado(self, contentLayout, *arg):
        ScreenBoxEmpleados = Screen(name='BoxEmpleados')
        ScreenBoxEmpleados.add_widget(contentLayout)
        self.add_widget(ScreenBoxEmpleados)
        
    
    def setScreenProductos(self, contentLayout, *arg):
        ScreenBoxProductos = Screen(name='BoxProductos')
        ScreenBoxProductos.add_widget(contentLayout)
        self.add_widget(ScreenBoxProductos)
        
    def setScreenDetalles(self, contentLayout, *arg):
        ScreenBoxDetalles = Screen(name='Detalles')
        ScreenBoxDetalles.add_widget(contentLayout)
        self.add_widget(ScreenBoxDetalles)