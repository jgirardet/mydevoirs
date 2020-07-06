from functools import partial

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from pony.orm import db_session

from mydevoirs.constants import BASE_DIR
from mydevoirs.database import db

Builder.load_file(str(BASE_DIR/"itemwidget.kv"))


class ItemWidget(BoxLayout):
    content = StringProperty()
    done = BooleanProperty()
    matiere_nom = StringProperty()
    matiere_color = ListProperty()

    def __init__(self, **entry):
        self.loaded_flag = False
        self.job = None

        self.entry = entry.pop("id")
        self.date = entry.pop("date")
        entry.pop("jour")
        super().__init__(**entry)

    def __repr__(self):
        return f"{self.date} : {self.matiere_nom} --- \
            {self.content[:10]}  {'X' if self.done else 'O'}"

    def on_kv_post(self, *args):
        self.loaded_flag = True

    def update_matiere(self, text):
        if text != self.matiere_nom:
            with db_session:
                a = db.Item[self.entry]
                a.matiere = text
                self.matiere_color = a.matiere.color
                self.matiere_nom = text
        content = self.ids.textinput
        content.focus = True
        content.do_cursor_movement("cursor_end")

    def on_content(self, _, text):
        if self.loaded_flag:
            if self.job:
                if self.job.is_triggered:
                    self.job.cancel()
            self.job = Clock.schedule_once(partial(self._set_content, text), 0.5)

    def _set_content(self, content, *args):
        with db_session:
            db.Item[self.entry].content = content

    def on_done(self, *args):
        if self.loaded_flag:
            with db_session:
                db.Item[self.entry].toggle()

    def remove(self):
        popup = EffacerPopup(content=ValidationPopup(item=self))
        popup.open()

    def remove_after_confirmation(self):
        with db_session:
            db.Item[self.entry].delete()
        self.parent.remove_widget(self)


class ContentTextInput(TextInput):
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        super().keyboard_on_key_down(window, keycode, text, modifiers)
        is_agenda = App.get_running_app().sm.current == "agenda"

        # ctrl + n == nouveau
        if is_agenda and keycode[1] == "n" and "ctrl" in modifiers:
            self.parent.jour_widget.add_item()

        # ctrl + d == duplicate
        elif is_agenda and keycode[1] == "d" and "ctrl" in modifiers:
            self.parent.jour_widget.ids.add_button.trigger_action(0)
            dropdown = window.window.children[0]
            window.window.remove_widget(dropdown)
            self.parent.jour_widget.items[0].update_matiere(self.parent.matiere_nom)

        # ctrl + m = matiere ?
        elif keycode[1] == "m" and "ctrl" in modifiers:
            self.parent.ids.spinner.trigger_action(0)

        # ctrl + e == effacer
        elif keycode[1] == "e" and "ctrl" in modifiers:
            self.parent.remove()
        else:
            return False
        return True


class EffacerPopup(Popup):
    pass


class ValidationPopup(FocusBehavior, BoxLayout):
    item = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.focus = True

    def oui(self):
        self.item.remove_after_confirmation()
        self.parent.parent.parent.dismiss()

    def non(self):
        self.parent.parent.parent.dismiss()
        self.item.ids.textinput.focus = True

    def keyboard_on_key_down(self, window, keycode, text, modifier):
        if keycode[1] in ["left", "right"]:
            backup = self.ids.oui.state
            self.ids.oui.state = self.ids.non.state
            self.ids.non.state = backup

        elif keycode[1] == "enter":
            if self.ids.oui.state == "down":
                self.oui()
            else:
                self.non()
        else:
            return False
        return True
