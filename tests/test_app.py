import datetime
from pathlib import Path
from unittest.mock import MagicMock, call

from kivy.config import ConfigParser
from kivy.uix.settings import Settings

from mydevoirs.app import MyDevoirsApp
from mydevoirs.settings import DEFAULT_SETTINGS, SETTING_PANELS
from kivy.base import EventLoop
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
        assert self.app.sm.screen_names == ["agenda", "todo"]

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

    def test_go_agenda(self):
        self.app.sm.current = "todo"
        carousel = self.app.sm.get_screen("agenda").carousel
        self.actionbar.ids.go_agenda.trigger_action(0)
        assert self.app.sm.current == "agenda"
        assert self.app.sm.transition.direction == "up"
        assert id(carousel) != id(self.app.sm.current_screen.carousel)  # widget rebuild

    def test_go_previous(self):
        self.app.sm.current = "agenda"
        today = datetime.date.today()
        assert self.app.agenda.carousel.date == today

        def go(self, *args):  # workaround because test can't wait transition duration
            self.index = 0

        with patch("mydevoirs.agenda.Carousel.load_previous", go):
            self.actionbar.ids.previous.trigger_action(0)
        assert self.app.agenda.carousel.date == today - datetime.timedelta(days=7)
        self.app.go_agenda()  # reset

    def test_go_next(self):
        self.app.sm.current = "agenda"
        today = datetime.date.today()
        assert self.app.agenda.carousel.date == today

        def go(
            self, *args, mode=None
        ):  # workaround because test can't wait transition duration
            self.index = 2

        with patch("mydevoirs.agenda.Carousel.load_next", go):
            self.actionbar.ids.next.trigger_action(0)
        assert self.app.agenda.carousel.date == today + datetime.timedelta(days=7)
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
                if isinstance(v, bool):
                    assert config.getboolean(section, k) == v
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
        print(self.app.on_config_change_bla.call_arg)
        assert self.app.on_config_change_bla.call_args == call(c, *option)

    def test_on_config_change_agenda(self):
        backup = self.app.go_agenda
        self.app.go_agenda = MagicMock()
        self.app.on_config_change_agenda(*[1, 2, 3])
        assert self.app.go_agenda.called
        self.app.go_agenda = backup

    def test_get_application_config(self):
        platform_dispatcher(
            self.app.get_application_config(),
            str(Path.home() / ".config" / "MyDevoirs" / "settings.ini"),
            str(Path.home() / "AppData" / "Local" / "MyDevoirs" / "settings.ini"),
        )
