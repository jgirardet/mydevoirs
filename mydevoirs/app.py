from pathlib import Path

from kivy.app import App
from kivy.properties import ObjectProperty
from mydevoirs.constants import APP_NAME
from mydevoirs.agenda import Agenda
from mydevoirs.todo import Todo
from mydevoirs.utils import get_dir
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.actionbar import ActionBar
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window
from kivy.modules import inspector

from mydevoirs.database.database import db_init

from mydevoirs.settings import settings_json


class MyDevoirsApp(App):

    carousel = ObjectProperty()

    def __init__(self):
        db_init()
        super().__init__()

        assert self.get_application_name() == APP_NAME

    def build(self):
        self.sm = ScreenManager(transition=SlideTransition(direction="up"))
        self.agenda = Agenda(name="agenda")
        self.todo = Todo(name="todo")
        self.sm.add_widget(self.agenda)
        self.sm.add_widget(self.todo)
        self.sm.current = "agenda"

        self.box = BoxLayout(orientation="vertical")
        self.box.add_widget(ActionBar())
        self.box.add_widget(self.sm)
        inspector.create_inspector(Window, self.sm)

        return self.box

    def go_todo(self):
        self.sm.current = "todo"
        self.sm.current_screen.reload()

    def go_agenda(self):
        self.sm.current = "agenda"
        self.sm.current_screen.go_date()

    def build_config(self, config):
        config.setdefaults(
            "agenda",
            {
                "lundi": True,
                "mardi": True,
                "mercredi": False,
                "jeudi": True,
                "vendredi": True,
                "samedi": False,
                "dimanche": False,
            },
        )

    def build_settings(self, settings):
        settings.add_json_panel("agenda", self.config, data=settings_json)

    def on_config_change(self, config, *args):
        self.go_date()

    def get_application_config(self):
        return super().get_application_config(
            str(Path(get_dir("config"), "settings.ini").absolute())
        )
