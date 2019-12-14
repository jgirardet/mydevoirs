from kivy.uix.settings import SettingItem, SettingSpacer, SettingPath
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.filebrowser import FileBrowser
import os
from kivy.core.window import Window

from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy_garden.filebrowser import FileBrowser


"""
SettingsPath using  Filebrowser instead Filechooser
"""


class SettingFilePath(SettingPath):
    def _validate(self, instance):
        self._dismiss()
        value = self.textinput.filename
        if not value:
            return
        self.value = os.path.realpath(value)

    def _create_popup(self, instance):
        # create popup layout
        content = BoxLayout(orientation="vertical", spacing=5)
        self.popup = popup = Popup(
            title=self.title, content=content, size_hint=(1, 0.9)
        )

        # create the filechooser
        initial_path = self.value or os.getcwd()

        self.textinput = textinput = FileBrowser(
            path=initial_path, size_hint=(1, 1), dirselect=False, show_hidden=True
        )
        textinput.bind(on_success=self._validate)
        textinput.bind(on_submit=self._validate)
        textinput.bind(on_canceled=self._dismiss)

        # construct the content
        content.add_widget(textinput)
        popup.open()
