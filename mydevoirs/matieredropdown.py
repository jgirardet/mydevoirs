from kivy.properties import BooleanProperty, ColorProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

from mydevoirs.constants import MATIERES_TREE


class MatiereDropdown(DropDown):
    def on_select(self, button):
        if button.has_sub:
            a = MatiereDropdown(init=False)
            self._create_options(a, button.text)
            a.open(self.attach_to)
        else:
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


class MatiereOption(Button):
    color = ColorProperty(None)
    has_sub = BooleanProperty(False)
    dropdown = ObjectProperty()

    def on_release(self):
        self.dropdown.select(self)

    def __repr__(self):
        return f"MatiereOption: {self.text}, has_sub={self.has_sub}"
