import os
import webbrowser
from pathlib import Path

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.settings import SettingPath, SettingString
from kivy_garden.filebrowser import FileBrowser

from mydevoirs.ouinonpopup import OuiNonPopup


"""
SettingsPath using  Filebrowser instead Filechooser
"""


class SettingFilePath(SettingPath):
    def _validate(self, instance):
        self._dismiss()
        value = self.textinput.filename
        if not value:
            return
        self.new_value = os.path.realpath(value)
        if self.new_value == self.value:
            return

        OuiNonPopup(
            title="Copier le contenu de l'ancienne base de donnée vers la nouvelle ?",
            on_oui=self._copy_ddb,
            on_non=self._update_value,
        )

    def _copy_ddb(self, *args):
        def write(*args):
            new.write_bytes(old.read_bytes())
            self._update_value()

        old = Path(self.value)
        new = Path(self.new_value)
        if new.exists():
            OuiNonPopup(
                title=f"Confirmez le remplacement du contenu de {str(new)} par {str(old)}",
                on_oui=write,
                on_non=self._dismiss,
            )
        else:
            write()
            self._update_value()

    def _update_value(self, *args):
        self.value = self.new_value

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


class SettingLabel(SettingString):
    def on_panel(self, instance, value):
        self.fbind("on_release", self.open_url)

    def open_url(self, *args):
        webbrowser.open_new(self.value)

    def _dismiss(self, *largs):  # pragma: no cover_all
        pass

    def _validate(self, instance):  # pragma: no cover_all
        pass

    def _create_popup(self, instance):  # pragma: no cover_all
        pass
