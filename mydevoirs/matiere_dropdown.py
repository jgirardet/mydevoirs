from kivy.lang import Builder
from kivy.properties import ColorProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.utils import rgba

from mydevoirs.constants import MATIERES, MATIERES_TREE
from mydevoirs.utils import gmc

kvoption = """
#: import MATIERES_TREE mydevoirs.constants.MATIERES_TREE
#: import MATIERES mydevoirs.constants.MATIERES
#: import gmc mydevoirs.utils.gmc

<MatiereOption>:
    size_hint_y: None
    height: dp(20)
    background_color: gmc(self.text)
    background_normal: ''
    color: (0,0,0)

    # background_normal: ''
    # canvas.before:
    #     Color:
    #         rgb: MATIERES[self.text]
    #     Rectangle:
    #         pos: self.pos
    #         size: self.size

<MatiereDropdown>:
    auto_width: False
    size_hint_x: None
    width: dp(200)
    # canvas.before:
    #     Color:
    #         rgb: (0.2,0.4,0,0.1)
    #     Rectangle:
    #         pos: self.pos
    #         size: self.size

"""
Builder.load_string(kvoption)


class MatiereDropdown(DropDown):

    base = ObjectProperty()

    def on_select(self, button):
        if button.has_sub:
            a = MatiereDropdown(init=False)
            self._create_options(a, button.text)

            a.open(self.attach_to)
        else:
            self.attach_to.parent.update_matiere(button.text)

    def _create_options(self, widget, key):
        collection = MATIERES_TREE[key] if key else MATIERES_TREE
        for k, v in collection.items():
            has_sub = not isinstance(v, tuple)
            widget.add_widget(MatiereOption(text=k, has_sub=has_sub))

    def __init__(self, init=True, **kwargs):
        super().__init__(**kwargs)
        if init:
            self._create_options(self, None)


class MatiereOption(Button):
    color = ColorProperty(None)

    def __init__(self, has_sub=False, **kwargs):
        super().__init__(**kwargs)
        self.has_sub = has_sub

    def on_release(self):
        self.parent.parent.select(self)
