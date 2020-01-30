from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.properties import ColorProperty

class AvailableMoveIndicator(Widget):
    color = ColorProperty([0,1,0,1])
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.start_animation()

    def start_animation(self, *args):
        anim = Animation(color = [0,1,0,1])
        anim.bind(on_complete=self.reset_anim)
        anim.start(self)

    def reset_anim(self, *args):
        anim = Animation(color = [1,0,0,1])
        anim.bind(on_complete=self.start_animation)
        anim.start(self)
