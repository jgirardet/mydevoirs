import os
import platform
import subprocess
import sys
from configparser import ConfigParser
from pathlib import Path

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.actionbar import ActionBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from pony.orm import OperationalError
from mydevoirs.constants import THEMES

import mydevoirs.database

# from mydevoirs.constants import BASE_DIR
from mydevoirs.custom_setting import (
    SettingCustomConfigFilePath,
    SettingFilePath,
    SettingLabel,
)
from mydevoirs.database import init_database
from mydevoirs.settings import DEFAULT_SETTINGS, SETTING_PANELS
from mydevoirs.utils import get_config, get_dir
import logging

LOG = logging.getLogger(__name__)


class MyDevoirsApp(App):

    use_kivy_settings = False

    carousel = ObjectProperty()

    title = "MyDevoirs"

    theme = THEMES["standard"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.avertissement = None

    def init_database(self):
        path = self.load_config()["ddb"]["path"]
        try:
            mydevoirs.database.db = init_database(filename=path, create_db=True)
        except OperationalError as err:
            LOG.error("Echec de création de la base de données")
            raise err

    def build(self):
        if self.avertissement:
            return self.avertissement
        else:
            return self.build_full_app()

    def build_full_app(self):
        from mydevoirs.agenda import Agenda
        from mydevoirs.colorchooser import ColorChooser
        from mydevoirs.todo import Todo

        self.load_theme()
        self.sm = ScreenManager(transition=SlideTransition(direction="up"))
        self.agenda = Agenda(name="agenda")
        self.todo = Todo(name="todo")
        self.colorchooser = ColorChooser(name="colorchooser")
        self.sm.add_widget(self.agenda)
        self.sm.add_widget(self.todo)
        self.sm.add_widget(self.colorchooser)
        self.sm.current = "agenda"

        self.box = BoxLayout(orientation="vertical")
        self.box.add_widget(ActionBar())
        self.box.add_widget(self.sm)

        return self.box

    def go_todo(self):
        self.sm.transition.direction = "down"
        self.sm.current = "todo"
        self.sm.current_screen.reload()

    def go_colorchooser(self):
        self.sm.transition.direction = "right"
        self.sm.current = "colorchooser"
        self.sm.current_screen.reload()

    def go_agenda(self):
        self.sm.transition.direction = "up"
        self.sm.current = "agenda"
        self.sm.current_screen.go_date()

    def build_config(self, config):
        for section, values in DEFAULT_SETTINGS.items():
            config.setdefaults(section, values)

    def build_settings(self, settings):
        settings.register_type("filepath", SettingFilePath)
        settings.register_type("configfilepath", SettingCustomConfigFilePath)
        settings.register_type("label", SettingLabel)
        for pan in SETTING_PANELS:
            settings.add_json_panel(pan[0], self.config, data=pan[1])

    def on_config_change(self, config, *args):
        getattr(self, "on_config_change_" + args[0])(config, *args)

    def on_config_change_agenda(self, config, *args):
        self.go_agenda()

    def on_config_change_ddb(self, config, section, key, value):
        self._reload_app()

    def on_config_change_theme(self, config, section, key, value):
        self._reload_app()

    def on_config_change_aide(self, config, section, key, value):
        pass  # pragma: no cover_all

    def get_application_config(self, disable_debug=None):
        return super().get_application_config(
            str(
                Path(
                    get_dir("config", disable_debug=disable_debug), "settings.ini"
                ).absolute()
            )
        )

    def _reload_app(self):
        if os.environ.get("MYDEVOIRS_DEBUG", None):  # pragma: no cover_all
            startupinfo = None
            if platform.system() == "Windows":  # pragma: no cover_linux
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            subprocess.run(  # pragma: no cover
                [sys.executable, "run.py", "dev"],
                cwd=os.getcwd(),
                startupinfo=startupinfo,
            )
        elif platform.system() == "Linux":
            appimage = os.environ["APPIMAGE"]
            subprocess.run([appimage])
        elif platform.system() == "Windows":  # pragma: no branch
            subprocess.run([sys.executable, "-m", "mydevoirs"], cwd=os.getcwd())
        self.stop()

    def load_theme(self):
        theme = get_config("theme", "theme", str)
        self.theme = THEMES.get(theme, THEMES["standard"])
