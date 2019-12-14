from pathlib import Path

from kivy.app import App
from kivy.core.window import Window
from kivy.modules import inspector
from kivy.properties import ObjectProperty
from kivy.uix.actionbar import ActionBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, SlideTransition


from mydevoirs.database import init_database
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from mydevoirs.settings import DEFAULT_SETTINGS, SETTING_PANELS
from mydevoirs.utils import get_dir
import sys
import subprocess
import mydevoirs.database
import os
import platform
from mydevoirs.filepath_setting import SettingFilePath
from mydevoirs.ouinonpopup import OuiNonPopup


class MyDevoirsApp(App):

    use_kivy_settings = False

    carousel = ObjectProperty()

    title = "MyDevoirs"

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)


        # Window.maximize()

    def init_database(self):
        path = self.load_config()["ddb"]["path"]
        mydevoirs.database.db = init_database(filename=path, create_db=True)

    def build(self):
        from mydevoirs.agenda import Agenda
        from mydevoirs.todo import Todo

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
        settings.register_type('filepath', SettingFilePath)
        for pan in SETTING_PANELS:
            settings.add_json_panel(pan[0], self.config, data=pan[1])

    def on_config_change(self, config, *args):
        getattr(self, "on_config_change_" + args[0])(config, *args)

    def on_config_change_agenda(self, config, *args):
        self.go_agenda()

    def on_config_change_ddb(self, config, section, key, value):
        self._reload_app()

    def get_application_config(self):
        return super().get_application_config(
            str(Path(get_dir("config"), "settings.ini").absolute())
        )

    def _reload_app(self):
        exec_app = [sys.executable]
        if not hasattr(sys, "frozen") or not hasattr(sys, "_MEIPASS"):
            main_path = Path(os.environ["MYDEVOIRS_BASE_DIR"], sys.argv[0])
            exec_app.append(str(main_path))

        startupinfo = None
        if platform.system() == "Windows":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        subprocess.Popen(exec_app, startupinfo=startupinfo)
        self.stop()
