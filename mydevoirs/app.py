from pathlib import Path

from kivy.app import App
from kivy.core.window import Window
from kivy.modules import inspector
from kivy.properties import ObjectProperty
from kivy.uix.actionbar import ActionBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, SlideTransition

from mydevoirs.agenda import Agenda
from mydevoirs.settings import DEFAULT_SETTINGS, SETTING_PANELS
from mydevoirs.todo import Todo
from mydevoirs.utils import get_dir, datas

class MyDevoirsApp(App):

    use_kivy_settings = False

    carousel = ObjectProperty()

    title = "MyDevoirs"

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
        self.sm.transition.direction = "down"
        self.sm.current = "todo"
        self.sm.current_screen.reload()

    def go_agenda(self):
        self.sm.transition.direction = "up"
        self.sm.current = "agenda"
        self.sm.current_screen.go_date()

    def build_config(self, config):
        for section, values in DEFAULT_SETTINGS.items():
            config.setdefaults(section, values)

    def build_settings(self, settings):
        for pan in SETTING_PANELS:
            settings.add_json_panel(pan[0], self.config, data=pan[1])

    def on_config_change(self, config, *args):
        getattr(self, "on_config_change_" + args[0])(config, *args)

    def on_config_change_agenda(self, config, *args):
        self.go_agenda()

    def get_application_config(self):
        return super().get_application_config(
            str(Path(get_dir("config"), "settings.ini").absolute())
        )
