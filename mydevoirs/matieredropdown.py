from kivy.properties import BooleanProperty, ColorProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.behaviors import FocusBehavior


from mydevoirs.constants import MATIERES_TREE


class MatiereDropdown( DropDown):
# class MatiereDropdown(FocusBehavior, DropDown):
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

    @property
    def options(self):
        return self.children[0].children

    # def keyboard_on_key_down(self, window, keycode, text, modifiers):
    #     print(window, keycode, text, modifiers)

    def set_option_focus(self, index):
        option = self.options[index]
        # self.dismiss()
        option.text = option.text.upper()
        but = self.attach_to
        print(but)
        self.open(but)
        # text, has_sub = option.text, option.has_sub
        # self.remove_widget(option)
        # self.add_widget(MatiereOption(text=text, has_sub=has_sub, focus=True))


class MatiereOption(Button):
# class MatiereOption(FocusBehavior, Button):
    color = ColorProperty(None)
    has_sub = BooleanProperty(False)
    dropdown = ObjectProperty()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # if self.focus:
    #     # self.text=self.text.upper()
    #     direction_keys = {276: "left", 273: "up", 274: "down", 275: "up"}

    def on_release(self):
        self.dropdown.select(self)

    def __repr__(self):
        return f"MatiereOption: {self.text}, has_sub={self.has_sub}"

    # def keyboard_on_key_down(self, window, keycode, text, modifiers):
    #     print("dans option", self.text)
    #     print(window, keycode, text, modifiers)
    #     self.focus = True
