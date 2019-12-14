from kivy.uix.popup import Popup
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.lang import Builder

KV = """
<OuiNonButton@ToggleButton>:
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

    auto_open=BooleanProperty(True)

    __events__ = ('on_oui', 'on_non') #', 'on_pre_dismiss', 'on_dismiss')

    def __init__(self,*args, **kwargs):
        # self.register_event_type("on_oui")
        super().__init__(*args, **kwargs)
        self.content = OuiNonPopupButtons(popup=self)
        if self.auto_open:
            self.open()


    def on_oui(self,*args, **kwargs):
        print('onoui', args, kwargs)
    # def on_oui(self,*args):
    #     print("base on_oui func")
        self.dismiss()

    def on_non(self,*args):
        print("on_non")
        self.dismiss()

from functools import partial

class OuiNonPopupButtons(FocusBehavior, BoxLayout):
    popup = ObjectProperty()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.oui.bind(on_press = self._on_press_oui)
        self.ids.non.bind(on_press = self._on_press_non)
        # self.ids.oui.bind(on_press = partial(self.popup.dispatch, "on_oui", *args, **kwargs))
        # self.ids.oui.bind(on_press = self.popup.on_non)
        self.focus = True

    def _on_press_oui(self,*args):
        self.popup.dispatch('on_oui')

    def _on_press_non(self,*args):
        self.popup.dispatch('on_non')

    def keyboard_on_key_down(self, window, keycode, text, modifier):
        if keycode[1] in ["left", "right"]:
            backup = self.ids.oui.state
            self.ids.oui.state = self.ids.non.state
            self.ids.non.state = backup

        elif keycode[1] == "enter":
            if self.ids.oui.state == "down":
                self.popup.dispatch('on_oui')
            else:
                self.popup.dispatch('on_non')
        else:
            return False
        return True


if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.widget import Widget

    class SettingsApp(App):

        def build(self):
            s = Widget()
            s.bind(on_close=self.stop)
            p = OuiNonPopup(title="mokfzmofkfzemok pkm", on_oui=self.bla)
            # p.bind(on_oui=self.bla)
            # p.open()
            return s

        def bla(self,*args,**kwargs):
            print('bla', args, kwargs)

    SettingsApp().run()