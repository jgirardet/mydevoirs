from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

KV = """
<OuiNonButton@Button>:
    bold: True

<OuiNonPopupButtons>:
    orientation: 'horizontal'
    OuiNonButton:
        text: "oui"
        id: oui
        state: "down"

    OuiNonButton:
        id: non
        text: "non"

<OuiNonPopup>:
    size_hint: .5, .2
"""

Builder.load_string(KV)


class OuiNonPopup(Popup):

    auto_open = BooleanProperty(True)

    __events__ = ("on_oui", "on_non")  #', 'on_pre_dismiss', 'on_dismiss')

    def __init__(self, *args, **kwargs):
        # self.register_event_type("on_oui")
        super().__init__(*args, **kwargs)
        self.content = OuiNonPopupButtons(popup=self)
        if self.auto_open:
            self.open()

    def on_oui(self, *args, **kwargs):
        self.dismiss()

    def on_non(self, *args, **kwargs):
        self.dismiss()


class OuiNonPopupButtons(FocusBehavior, BoxLayout):
    popup = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.oui.bind(on_press=self._on_press_oui)
        self.ids.non.bind(on_press=self._on_press_non)
        self.focus = True

    def _on_press_oui(self, *args):
        self.ids.oui.state = "down"
        self.ids.non.state = "normal"
        self.popup.dispatch("on_oui")

    def _on_press_non(self, *args):
        self.ids.oui.state = "normal"
        self.ids.non.state = "down"
        self.popup.dispatch("on_non")

    def _toggle_state(self):
        backup = self.ids.oui.state
        self.ids.oui.state = self.ids.non.state
        self.ids.non.state = backup

    def keyboard_on_key_down(self, window, keycode, text, modifier):
        if keycode[1] in ["left", "right"]:
            self._toggle_state()

        elif keycode[1] == "enter":
            if self.ids.oui.state == "down":
                self.popup.dispatch("on_oui")
            else:
                self.popup.dispatch("on_non")
        else:
            return False
        return True


if __name__ == "__main__":
    from kivy.app import App
    from kivy.uix.widget import Widget

    class SettingsApp(App):
        def build(self):
            s = Widget()
            s.bind(on_close=self.stop)
            OuiNonPopup(title="mokfzmofkfzemok pkm", on_oui=self.stop)
            return s

    SettingsApp().run()
