from kivy.uix.settings import SettingItem, SettingSpacer
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.filebrowser import FileBrowser
import os
from kivy.core.window import Window

from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.button import Button

"""
Filechooser tweaked to permit new filenames
"""


class MyFileBrowser(FileBrowser):
    pass
    # def on_success(self, *args, **kwargs):
    #     # print(*args)
    #     # print(**kwargs)
    #     print("dans on succes", self.filename)
    #     # print(self.path)
    #     super().on_success(*args, **kwargs)


class SettingFilePath(SettingItem):
    """Implementation of a Path setting on top of a :class:`SettingItem`.
    It is visualized with a :class:`~kivy.uix.label.Label` widget that, when
    clicked, will open a :class:`~kivy.uix.popup.Popup` with a
    :class:`~kivy.uix.filechooser.FileChooserListView` so the user can enter
    a custom value.
    .. versionadded:: 1.1.0
    """

    popup = ObjectProperty(None, allownone=True)
    """(internal) Used to store the current popup when it is shown.
    :attr:`popup` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    """

    textinput = ObjectProperty(None)
    """(internal) Used to store the current textinput from the popup and
    to listen for changes.
    :attr:`textinput` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.
    """

    show_hidden = BooleanProperty(False)
    """Whether to show 'hidden' filenames. What that means is
    operating-system-dependent.
    :attr:`show_hidden` is an :class:`~kivy.properties.BooleanProperty` and
    defaults to False.
    .. versionadded:: 1.10.0
    """

    dirselect = BooleanProperty(True)
    """Whether to allow selection of directories.
    :attr:`dirselect` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to True.
    .. versionadded:: 1.10.0
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("init", self.value)
    def on_panel(self, instance, value):
        print(instance, value)
        if value is None:
            return
        self.fbind("on_release", self._create_popup)

    def _dismiss(self, *largs):
        if self.textinput:
            self.textinput.focus = False
        if self.popup:
            self.popup.dismiss()
        self.popup = None

    def _validate(self, instance):
        self._dismiss()
        print("_validate", self.textinput.filename)
        value = self.textinput.filename

        if not value:
            return

        self.value = os.path.realpath(value)
        print(self.value)

    def _create_popup(self, instance):
        # create popup layout
        content = BoxLayout(orientation="vertical", spacing=5)
        popup_width = min(0.95 * Window.width, dp(500))
        self.popup = popup = Popup(
            title=self.title, content=content
        )  # size_hint=(None, 0.9), width=popup_width
        # )

        # create the filechooser
        initial_path = self.value or os.getcwd()
        self.textinput = textinput = MyFileBrowser(
            path=initial_path,
            size_hint=(1, 1),
            dirselect=self.dirselect,
            show_hidden=self.show_hidden,
        )
        textinput.bind(on_success=self._validate)
        textinput.bind(on_submit=self._validate)

        # construct the content
        content.add_widget(textinput)
        content.add_widget(SettingSpacer())
        popup.open()
