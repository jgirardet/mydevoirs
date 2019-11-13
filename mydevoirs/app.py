from mydevoirs.widgets import CarouselWidget
from kivy.app import App
from kivy.properties import (
    StringProperty,
    ObjectProperty,
    ListProperty,
    NumericProperty,
    BooleanProperty,
    DictProperty,
)
from mydevoirs.constants import APP_NAME
from pathlib import Path
from mydevoirs.utils import get_dir
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.actionbar import ActionBar

from kivy.core.window import Window
from kivy.modules import inspector

from mydevoirs.database.database import db_init

from mydevoirs.settings import settings_json
from mydevoirs.slide_item import SettingSlider


class MyDevoirsApp(App):

    carousel = ObjectProperty()

    def __init__(self):
        db_init()
        super().__init__()

        assert self.get_application_name() == APP_NAME

    def build(self):
        self.carousel = CarouselWidget()
        self.box = BoxLayout(orientation="vertical")
        self.box.add_widget(ActionBar())
        self.box.add_widget(self.carousel)
        inspector.create_inspector(Window, self.carousel)

        return self.box

    def go_date(self, date=None):
        self.box.remove_widget(self.carousel)

        self.carousel = CarouselWidget(date)

        self.box.add_widget(self.carousel)

    def build_config(self, config):
        config.setdefaults(
            "agenda",
            {
                "nbjour": 5,
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
        settings.register_type("slider", SettingSlider)
        settings.add_json_panel("agenda", self.config, data=settings_json)

    def on_config_change(self, config, *args):
        print(args)
        self.go_date()

    def get_application_config(self):
        return super().get_application_config(
            Path(get_dir("config"), "settings.ini").absolute()
        )
