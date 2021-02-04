from kivy.clock import Clock
import kivy
from kivy.uix.boxlayout import BoxLayout
kivy.require('1.9.0')


#Side Bar Menu y Contenido
class BoxContainer(BoxLayout):
    def __init__(self, **kwargs):
        super(BoxContainer, self).__init__(**kwargs)
        
class BoxSlideMenu(BoxLayout):
    pass