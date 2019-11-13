#!python
#!/usr/bin/env python
from kivy.app import App
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import BooleanProperty
from kivy.uix.widget import Widget

from mydevoirs.constants import MATIERES_TREE

Builder.load_string(
    """
<FirstMenu>:
    orientation: "vertical"


<ChoixOption>:
    size_hint_y: None
    height: dp(20)
"""
)


class ChoixOption(BubbleButton):
    has_sub = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.has_sub=has_subb

    def on_release(self, *args):
        print("relase", args)
        self.parent.parent.option_clicked(self.text,self.has_sub)


class BaseBouton(BubbleButton):
    # size_hint = (0.1, 0.1)
    # text = "matiere"
    id = "basebouton"

    def on_release(self, *args):
        print(*args)

        self.add_widget(FirstMenu(pos=(self.pos[0]/2, self.pos[1])))
        # self.parent.remove_widget(self)


class FirstMenu(Bubble):

    def __init__(self, nom=None, **kwargs):
        super().__init__(**kwargs)
        if not nom:
            for m in MATIERES_TREE.keys():
                self.add_widget(ChoixOption(text=m))

    def option_clicked(self, text, has_sub):
        if has_sub:
            self.parent.do_sub(text)
        else:
            self.parent.selected(text)


class MenuMatiere(BoxLayout):
    # pass
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        b = BaseBouton(text="début")
        self.add_widget(b)

    def selected(self, text):
        print("update database§matiere")
        self.clear_widgets()
        self.add_widget(BaseBouton(text=text))

    def do_sub(self, text):
        self.clear_widgets()
        print("do sub")


if __name__ == "__main__":

    class MyApp(App):
        def build(self):
            a =BoxLayout(height=50, size_hint_y=None, pos=(0, 300))
            a.add_widget(MenuMatiere())
            return a
    MyApp().run()
