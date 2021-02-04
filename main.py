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
from Estructura.Login import BoxLogin
from Estructura.Estetica.portada import BoxLogoPrincipal
kivy.require('1.9.0')


#Vista Principal de Aplicacion
class MainView(ScreenManager):
    
    user = StringProperty('')
    password = StringProperty('')

    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)
        self.transition = RiseInTransition()

        self.ScreenLogoPrincipal = Screen(name='LogoPrincipal')
        self.ScreenLogoPrincipal.add_widget(BoxLogoPrincipal())
        self.add_widget(self.ScreenLogoPrincipal)

        self.ScreenLogoPrincipal.bind(on_touch_down=self.Go_login)

    def Go_login(self, *arg):

        self.ScreenLogin = Screen(name='Login')
        self.Login = BoxLogin(self)
        self.ScreenLogin.add_widget(self.Login)
        self.add_widget(self.ScreenLogin)
        self.current = 'Login'

class Inventario(App):

    def build(self):

        con = Sqlconexion()
        conexion = con.create_DataBase()
        con.create_Table(conexion)
        con.close_db(conexion)

        return MainView()

if __name__ == "__main__":
    Inventario().run()
