from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    NumericProperty,
    ObjectProperty,
)
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from pony.orm import db_session

from mydevoirs.database import db


class MatiereDropdown(FocusBehavior, DropDown):

    focused_index = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._create_options(self, None)
        self.last_focused = None
        self.focused_index = -1
        self.focus = True

    def on_select(self, button):
        self.attach_to.parent.update_matiere(button.matiere_id)

    @db_session
    def _create_options(self, widget, key):

        # collection = self.tree if key is None else self.tree[key]
        # for k, v in collection.items():
        #     has_sub = not isinstance(v, tuple)
        #     widget.add_widget(MatiereOption(text=k, has_sub=has_sub, dropdown=widget))
        for item in db.Matiere.select():
            widget.add_widget(
                MatiereOption(
                    text=item.nom,
                    dropdown=widget,
                    background_color=item.color,
                    matiere_id=item.id,
                )
            )

    def on_focused_index(self, instance, value):
        if self.last_focused:
            self.options[self.last_focused].toggle_focus()
        self.options[value].toggle_focus()

    @property
    def options(self):
        return self.children[0].children

    def keyboard_on_key_down(self, window, keycode, text, modifier):
        if keycode[1] == "down":  # down
            self.last_focused = self.focused_index
            if self.focused_index == -len(self.options):
                self.focused_index = -1
            else:
                self.focused_index = self.focused_index - 1

        elif keycode[1] == "up":  # up
            self.last_focused = self.focused_index
            if self.focused_index == -1:
                self.focused_index = -len(self.options)
            else:
                self.focused_index = self.focused_index + 1

        elif keycode[1] in ["enter", "right"]:  # right, Enter
            self.select(self.options[self.focused_index])
        else:
            return False
        return True


class MatiereOption(Button):
    dropdown = ObjectProperty()
    matiere_id = NumericProperty()

    def on_release(self):
        self.dropdown.select(self)

    def __repr__(self):
        return f"MatiereOption: {self.text}"

    def toggle_focus(self, *args):
        self.bold = not self.bold
