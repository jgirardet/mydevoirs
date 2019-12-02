from functools import partial

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    ObjectProperty,
    StringProperty,
    NumericProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from pony.orm import db_session
from kivy.uix.textinput import TextInput
from kivy.base import EventLoop

from mydevoirs.database.database import db
from mydevoirs.utils import get_base_dir

Builder.load_file(str(get_base_dir() / "mydevoirs" / "itemwidget.kv"))


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

        # if keycode[1] == "n" and "ctrl" in modifiers:
        #     self.parent.jour_widget.add_item()
        # dropdown = EventLoop.window.children[0]

        # self.parent.jour_widget.items[0].ids.textinput.focus = True


class EffacerPopup(Popup):
    pass


class EffacerPopup(Popup):
    pass


class ValidationPopup(BoxLayout):
    item = ObjectProperty()
