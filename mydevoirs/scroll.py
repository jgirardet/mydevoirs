import kivy

kivy.require("1.0.8")

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout


class BaseGrid(GridLayout):
    pass


class Bouton(BoxLayout):
    pass


class ScrollApp(App):
    def build(self):

        # create a default grid layout with custom width/height
        layout = BaseGrid()

        # when we add children to the grid layout, its size doesn't change at
        # all. we need to ensure that the height will be the minimum required
        # to contain all the childs. (otherwise, we'll child outside the
        # bounding box of the childs)
        layout.bind(minimum_height=layout.setter("height"))

        # add button into that grid
        for i in range(30):
            btn = Bouton()
            layout.add_widget(btn)

        # create a scroll view, with a size < size of the grid
        root = ScrollView(
            size_hint=(None, None),
            size=(500, 320),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            do_scroll_x=False,
        )
        root.add_widget(layout)

        return root


if __name__ == "__main__":

    ScrollApp().run()
