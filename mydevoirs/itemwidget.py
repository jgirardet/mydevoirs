from pathlib import Path

from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import (
    StringProperty,
    ListProperty,
    BooleanProperty,
    ObjectProperty
)
from kivy.clock import Clock
from mydevoirs.database.database import db
from mydevoirs.utils import get_base_dir
from pony.orm import db_session
from functools import partial
from kivy.uix.popup import Popup


Builder.load_file(str(get_base_dir()/ "mydevoirs" / "itemwidget.kv"))



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
                print('called')
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
        print('debut relve')
        self.popup = EffacerPopup(item=self)
        print('remov enc ours')
        self.popup.open()
        print('fin remove')

    def remove_after_confirmation(self):
        with db_session:
            db.Item[self.entry].delete()
        self.parent.remove_widget(self)




class EffacerPopup(Popup):
    item = ObjectProperty()