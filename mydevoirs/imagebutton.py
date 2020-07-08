from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image


class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(state=self.update_color)

    def update_color(self, _, state):
        if state == "down":
            self.color = (1, 1, 1, 0.5)
        else:
            self.color = (1, 1, 1, 1)
