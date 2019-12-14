from kivy.uix.popup import Popup
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.lang import Builder

KV = """
<ValidationButton@ToggleButton>:
    bold: True

<OuiNonPopupButtons>:
    orientation: 'horizontal'
    ValidationButton:
        text: "oui"
        id: oui
        state: "down"

    ValidationButton:
        id: non
        text: "non"

<OuiNonPopup>:
    size_hint: .5, .2
"""

Builder.load_string(KV)

class OuiNonPopup(Popup):

    auto_open=BooleanProperty(True)

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = OuiNonPopupButtons(popup=self)
        self.open()

    def oui(self,args):

        self.dismiss()

    def non(self,args):
        self.dismiss()


class OuiNonPopupButtons(FocusBehavior, BoxLayout):
    popup = ObjectProperty()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.oui.bind(on_press = self.popup.oui)
        self.ids.oui.bind(on_press = self.popup.non)
        self.focus = True


    def keyboard_on_key_down(self, window, keycode, text, modifier):
        if keycode[1] in ["left", "right"]:
            backup = self.ids.oui.state
            self.ids.oui.state = self.ids.non.state
            self.ids.non.state = backup

        elif keycode[1] == "enter":
            if self.ids.oui.state == "down":
                self.popup.oui()
            else:
                self.popup.non()
        else:
            return False
        return True


if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.widget import Widget

    class SettingsApp(App):

        def build(self):
            s = Widget()
            # s.bind(on_close=self.stop)
            OuiNonPopup(title="mokfzmofkfzemok pkm")
            return s

    SettingsApp().run()