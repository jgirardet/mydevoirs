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



class MyDevoirsApp(App):

    carousel = ObjectProperty()

    def __init__(self):
        super().__init__()

        assert self.get_application_name() == APP_NAME

    def build(self):
        self.carousel = CarouselWidget()
        self.box = BoxLayout(orientation="vertical")
        self.box.add_widget(ActionBar())
        self.box.add_widget(self.carousel)
        return self.box

    def go_date(self, date=None):
        self.box.remove_widget(self.carousel)

        self.carousel = CarouselWidget(date)

        self.box.add_widget(self.carousel)

    def build_config(self, config):
        config.setdefaults("agenda", {"nbjour": 5})

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