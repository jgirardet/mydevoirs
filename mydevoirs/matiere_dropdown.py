from kivy.uix.dropdown import DropDown
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, ColorProperty

from mydevoirs.constants import MATIERES_TREE


kvoption = """
<MatiereOption>:
    size_hint_y: None
    height: dp(20)
    background_color: self.color
    # canvas.before:
    #     Color:
    #         rgb: self.color
    #     Rectangle:
    #         pos: self.pos
    #         size: self.size

<MatiereDropdown>:
    border: (0,0,0)
    canvas.before:
        Color:
            rgb: (0,0,0)
        Rectangle:
            pos: self.pos
            size: self.size

"""
Builder.load_string(kvoption)


class MatiereDropdown(DropDown):

    base = ObjectProperty()

    def on_select(self, button):
        if button.has_sub:
            a = MatiereDropdown(init=False)
            for k, v in MATIERES_TREE[button.text].items():
                a.add_widget(MatiereOption(text=k, has_sub=False, color=v))

            a.open(self.attach_to)
        else:
            self.attach_to.parent.update_matiere(button.text)

    def __init__(self, init=True, **kwargs):
        super().__init__(**kwargs)
        if init:
            for k, v in MATIERES_TREE.items():
                has_sub = False
                color = v
                if not isinstance(v, tuple):
                    has_sub = True
                    color = list(v.values())[0]

                self.add_widget(MatiereOption(has_sub=has_sub, text=k, color=color))


class MatiereOption(Button):
    color = ColorProperty(None)

    def __init__(self, has_sub=False, **kwargs):
        super().__init__(**kwargs)
        self.has_sub = has_sub

    def on_release(self):
        self.parent.parent.select(self)
