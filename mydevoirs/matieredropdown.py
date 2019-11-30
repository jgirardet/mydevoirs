from kivy.properties import BooleanProperty, ColorProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.behaviors import FocusBehavior


from mydevoirs.constants import MATIERES_TREE


class MatiereDropdown(FocusBehavior, DropDown):
    def on_select(self, button):
        if button.has_sub:
            a = MatiereDropdown(init=False)
            self._create_options(a, button.text)
            a.open(self.attach_to)
            self.attach_to.parent.update_matiere(button.text)

    def _create_options(self, widget, key):
        collection = self.tree[key] if key else self.tree
        for k, v in collection.items():
            has_sub = not isinstance(v, tuple)
            widget.add_widget(MatiereOption(text=k, has_sub=has_sub, dropdown=widget))

    def __init__(self, init=True, tree=MATIERES_TREE, **kwargs):
        super().__init__(**kwargs)
        self.tree = tree
        if init:
            self._create_options(self, None)
        self.children[0].children[-1].focus = True
        print(self, self.focus, self.keyboard_mode)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        print(window, keycode, text, modifiers)

class MatiereOption(FocusBehavior, Button):
    color = ColorProperty(None)
    has_sub = BooleanProperty(False)
    dropdown = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.focus)
        direction_keys = {276:'left', 273: 'up', 274:'down', 275:  'up'}
        if self.focus:
            self.border = [50,50,50,50]

    def on_release(self):
        self.dropdown.select(self)

    def __repr__(self):
        return f"MatiereOption: {self.text}, has_sub={self.has_sub}"

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        print('dans option', self.text)
        print(window, keycode, text, modifiers)
        self.focus = True

