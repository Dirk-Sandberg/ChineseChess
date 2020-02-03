from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.properties import ColorProperty
from kivy.uix.image import Image

class AvailableMoveIndicator(Image):
    color = ColorProperty([0,1,0,1])
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
