import datetime
from pathlib import Path
from unittest.mock import MagicMock, call

import pytest
from kivy.config import ConfigParser
from kivy.uix.settings import Settings

from mydevoirs.agenda import CarouselWidget
from mydevoirs.app import MyDevoirsApp
from mydevoirs.settings import DEFAULT_SETTINGS, SETTING_PANELS

from .fixtures import *


class TestMyDevoirsApp(MyDevoirsTestCase):
    @classmethod
    def setUpClass(self):
        # super().setUp()
        self.app = MyDevoirsApp()
        self.app.build()
        self.actionbar = self.app.box.children[1]

    def test_init_super(self):
        self.check_super_init("App", MyDevoirsApp)
        assert self.app.get_application_name() == APP_NAME

    def test_sm(self):

        assert self.app.sm.current == "agenda"
        assert self.app.sm.screen_names == ["agenda", "todo", "colorchooser"]

    def test_change(self):
        assert self.app.sm.current == "agenda"
        self.app.sm.current = "todo"
        assert self.app.sm.current == "todo"

    def test_go_aatodo(self):
        self.app.sm.current = "agenda"
        todolist = self.app.sm.get_screen("todo").todolist
        self.actionbar.ids.go_todo.trigger_action(0)
        assert self.app.sm.current == "todo"
        assert self.app.sm.transition.direction == "down"
        assert id(todolist) != id(self.app.sm.current_screen.todolist)  # widget rebuild

    def test_go_colorchooser(self):
        self.app.sm.current = "agenda"
        assert not hasattr(self.app.sm.get_screen("colorchooser"), "colorlist")
        self.actionbar.ids.go_colorchooser.trigger_action(0)
        assert self.app.sm.current == "colorchooser"
        assert self.app.sm.transition.direction == "right"
        assert self.app.sm.current_screen.colorlist  # reload called

    def test_go_agenda(self):
        self.app.sm.current = "todo"
        carousel = self.app.sm.get_screen("agenda").carousel
        self.actionbar.ids.go_agenda.trigger_action(0)
        assert self.app.sm.current == "agenda"
        assert self.app.sm.transition.direction == "up"
        assert id(carousel) != id(self.app.sm.current_screen.carousel)  # widget rebuild

    def test_go_previous(self):
        self.app.sm.current = "agenda"
        self.app.agenda.carousel = CarouselWidget(day=datetime.datetime(2020, 7, 10))

        def go(self, *args):  # workaround because test can't wait transition duration
            self.index = 0

        with patch("mydevoirs.agenda.Carousel.load_previous", go):
            self.actionbar.ids.previous.trigger_action(0)
        assert self.app.agenda.carousel.date == datetime.datetime(2020, 7, 3)
        self.app.go_agenda()  # reset

    def test_go_next(self):
        self.app.sm.current = "agenda"
        self.app.sm.current = "agenda"
        self.app.agenda.carousel = CarouselWidget(day=datetime.datetime(2020, 7, 10))

        def go(
            self, *args, mode=None
        ):  # workaround because test can't wait transition duration
            self.index = 2

        with patch("mydevoirs.agenda.Carousel.load_next", go):
            self.actionbar.ids.next.trigger_action(0)
        assert self.app.agenda.carousel.date == datetime.datetime(2020, 7, 17)
        self.app.go_agenda()  # reset

    def test_go_settings(self):

        with patch.object(self.app, "open_settings") as m:
            self.actionbar.ids.params.trigger_action(0)
            assert m.called

    def test_build_config(self):
        config = ConfigParser()
        self.app.build_config(config)

        for section, values in DEFAULT_SETTINGS.items():
            for k, v in values.items():
                if isinstance(v, int):
                    assert config.getboolean(section, k) == v
                elif isinstance(v, str):
                    assert config.get(section, k) == v
                else:
                    assert False, "un cas est manquant"

    def test_build_settings(self):
        config = ConfigParser()
        self.app.build_config(config)
        reglages = Settings()
        self.app.build_settings(reglages)
        panels = reglages.children[0].content.panels
        for panel in SETTING_PANELS:
            assert any(p.title == panel[0] for p in panels.values())

    def test_on_change_section_exists(self):
        for section in DEFAULT_SETTINGS:
            assert hasattr(self.app, "on_config_change_" + section)

    def test_on_config_change_calls_func(self):
        self.app.on_config_change_bla = MagicMock()
        c = ConfigParser()
        option = ["bla", "cle", "value"]
        self.app.on_config_change(c, *option)
        assert self.app.on_config_change_bla.called
        assert self.app.on_config_change_bla.call_args == call(c, *option)

    def test_on_config_change_agenda(self):
        backup = self.app.go_agenda
        self.app.go_agenda = MagicMock()
        self.app.on_config_change_agenda(*[1, 2, 3])
        assert self.app.go_agenda.called
        self.app.go_agenda = backup

    def test_on_config_change_ddb(self):
        backup = self.app._reload_app
        self.app._reload_app = MagicMock()
        self.app.on_config_change_ddb(*[1, 2, 3, 4])
        assert self.app._reload_app.called
        self.app._reload_app = backup

    def test_get_application_config(self):

        platform_dispatcher(
            self.app.get_application_config(disable_debug=True),
            str(Path.home() / ".config" / "MyDevoirs" / "settings.ini"),
            str(Path.home() / "AppData" / "Local" / "MyDevoirs" / "settings.ini"),
        )

    def test_homepage_as_url(self):
        a = ConfigParser()
        self.app.build_config(a)
        assert a.get("aide", "aide") == "https://jgirardet.github.io/mydevoirs"

    def test_reset_database(self):
        app = MyDevoirsApp()
        with tempfile.NamedTemporaryFile() as t:
            t.close()  # windows need it**********************
            app.get_application_config = lambda: t.name
            text = """[agenda]
    lundi = 0
    mardi = 1
    mercredi = 0
    jeudi = 1
    vendredi = 1
    samedi = 0
    dimanche = 1

    [ddb]
    path = /mauvais/repo

    """
            Path(t.name).write_text(text)
            cp = ConfigParser()
            cp.read(t.name)
            assert cp.sections() == ["agenda", "ddb"]
            assert cp["ddb"]["path"] == "/mauvais/repo"
            app._reset_database()
            cp = ConfigParser()
            cp.read(t.name)
            assert cp["ddb"]["path"] == DEFAULT_SETTINGS["ddb"]["path"]
            assert app.config["ddb"]["path"] == DEFAULT_SETTINGS["ddb"]["path"]
            assert cp["agenda"]["lundi"] == app.config["agenda"]["lundi"]

    def test_init_database(self):
        app = MyDevoirsApp()
        app.load_config = lambda: {"ddb": {"path": str(Path.home())}}
        app._reset_database = MagicMock()

        app.init_database()
        assert app._reset_database.call_args_list == (call())

    @pytest.mark.skipif(platform.system() != "Linux", reason="Linux test")
    @patch("mydevoirs.app.subprocess.Popen")
    def test_reload_app_script_linux(self, popen):
        app = MyDevoirsApp()
        app.stop = MagicMock()
        app._reload_app()
        args = popen.call_args_list[0]
        assert app.stop.called
        # assert args[0][0][0].endswith("python")
        assert len(args[0][0]) == 2
        assert args[1]["startupinfo"] is None

    @pytest.mark.skipif(platform.system() != "Windows", reason="windows test")
    @patch("mydevoirs.app.subprocess.Popen")
    def test_reload_app_script_windows(self, popen):
        from mydevoirs.app import subprocess as sb

        sb.STARTUPINFO = MagicMock()
        app = MyDevoirsApp()
        app.stop = MagicMock()
        app._reload_app()
        args = popen.call_args_list[0]
        print(args)
        assert app.stop.called
        assert args[0][0][0].endswith("python.exe")
        assert len(args[0][0]) == 2
        assert args[1]["startupinfo"] is not None
