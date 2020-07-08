from kivy.app import App
from kivy.clock import Clock
from kivy.properties import (
    BooleanProperty,
    DictProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
    ColorProperty,
)
from kivy.uix.behaviors import DragBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.utils import rgba
from kivy.uix.image import Image
from pony.orm import db_session
from kivy.graphics import Rectangle, Color
from mydevoirs.database import db
from mydevoirs.itemwidget import ValidationPopup
from mydevoirs.ouinonpopup import OuiNonPopup
from mydevoirs.utils import datas


class ColorPopup(Popup):
    color = ColorProperty()
    cp = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = False
        self.size = (500, 500)
        self.size_hint = (None, None)
        self.cp = ColorPicker(size_hint=(1, 0.9), color=self.color)
        self.title_align = "center"
        self.title_color = [0, 0, 0, 1]
        self.background = ""
        self.separator_height = 0
        # self.background_color = self.color
        self.cp.bind(color=self.setter("background_color"))
        box = BoxLayout(orientation="vertical")
        box.add_widget(self.cp)
        self.ok_button = Button(text="Ok", on_press=self.on_choosed, size_hint=(1, 1))
        self.cancel_button = Button(
            text="Annuler", on_press=self.dismiss, size_hint=(1, 1)
        )
        button_box = BoxLayout(orientation="horizontal", size_hint=(1, 0.1))
        button_box.add_widget(self.ok_button)
        button_box.add_widget(self.cancel_button)
        box.add_widget(button_box)
        self.content = box

    def on_choosed(self, button):
        self.color = self.cp.color
        self.dismiss()


class ColorChooser(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def reload(self):
        # if hasattr(self, "colorlist"):
        #     self.remove_widget(self.colorlist)
        self.clear_widgets()
        self.colorlist = ColorList(size_hint_y=None)
        self.colorlist.bind(minimum_height=self.colorlist.setter("height"))
        sc = ScrollView(do_scroll_x=False)
        sc.add_widget(self.colorlist)
        self.add_widget(sc)


class RemoveButton(Button):
    text = "X"
    background_normal = ""

    def on_release(self):
        self.parent.remove()


class MoveButton(Label):
    text = "M"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            parent = self.parent
            grid = parent.grid

            initial_y = parent.y
            parent.diff_y = initial_y - touch.y
            # breakpoint()
            touch.grab(parent)
            grid.grabbed = parent
            parent_index = grid.children.index(parent)
            grid.last_hovered = grid.children[parent_index - 1]
            grid.remove_widget(parent)
            grid.add_widget(parent)
            Clock.schedule_once(lambda dt: grid.setup_on_drag(initial_y))
            return True

    # def on_touch_move(self, touch):
    #     if not self.collide_point(*touch.pos):
    #         return

    # def on_touch_up(self, touch):
    #
    #     if not self.collide_point(*touch.pos):
    #         return
    #     if current := self.parent.grid.grabbed:
    #         if current != self:
    #             actual_index = self.parent.grid.children.index(self.parent)
    #             parent = current.parent
    #
    #             self.parent.grid.remove_widget(parent)
    #             self.parent.grid.bind(children=self.parent.grid.reorder)
    #             self.parent.grid.add_widget(parent, actual_index)
    #             for it in self.parent.grid.children:
    #                 it.opacity = 1
    # self.parent.grid.bind(children=self.parent.grid.reorder)


class MatiereItem(BoxLayout):

    bgColor = ColorProperty()
    texte = ObjectProperty()

    def __init__(self, data, grid, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.data = data
        self.grid = grid
        self.height = 30
        self.size_hint_y = None
        self.texte = MatiereInput(size_hint_x=0.8)
        self.bind(bgColor=self.texte.setter("background_color"))
        self.add_widget(self.texte)
        remove = RemoveButton(size_hint_x=0.2)
        self.bind(bgColor=remove.setter("background_color"))
        self.add_widget(remove)
        self.add_widget(MoveButton(size_hint_x=0.2))
        self.bgColor = data["color"]

    def remove(self):
        pop = OuiNonPopup(
            title=f"""Effacer {self.data['nom']} ?
Ceci effacera TOUTES les lignes de devoirs de cette matiere
""",
            on_oui=self.remove_entry,
        )
        pop.open()

    @db_session
    def remove_entry(self, *args):
        db.Matiere[self.data["id"]].delete()
        App.get_running_app().colorchooser.reload()

    def on_touch_move(self, touch):

        if grabbed := self.grid.grabbed:

            if self.collide_point(touch.x, touch.y) and self != grabbed:
                self.opacity = 1
                self.grid.last_hovered = self
            else:
                self.opacity = 0.5
        else:
            return

        # super().on_touch_move(touch)


class MatiereInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_parent(self, instance, parent):
        # print(parent, self.parent)
        self.background_color = parent.data["color"]
        self.text = parent.data["nom"]
        self.background_normal = ""
        self.foreground_color = [0, 0, 0, 1]
        self.bind(text=self.on_text_changed)

    def on_touch_down(self, touch):
        if not self.collide_point(touch.x, touch.y):
            return
        if touch.button == "left":
            super().on_touch_down(touch)

        elif touch.button == "right":
            self.colorpopup = ColorPopup(
                title=f"Couleur pour {self.parent.data['nom']}",
                color=self.background_color,
                # on_color=self.update_color,
            )
            self.colorpopup.bind(color=self.update_color)
            self.colorpopup.open()

    @db_session
    def update_color(self, popup, color):
        self.parent.bgColor = color
        db.Matiere[self.parent.data["id"]].color = color

    @db_session
    def on_text_changed(self, instance, text):
        if not text:
            return
        db.Matiere[self.parent.data["id"]].nom = text


class ColorList(BoxLayout):

    grabbed = None
    last_hovered = None
    orientation = "vertical"
    spacing = 5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_items()

    @db_session
    def load_items(self):
        for it in db.Matiere.get_ordered():
            self.add_widget(MatiereItem(it, self))

    def on_touch_move(self, touch):

        if grabbed := self.grabbed:
            grabbed.pos = (0, touch.y + grabbed.diff_y)
        super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if grabbed := self.grabbed:
            actual_index = self.children.index(self.last_hovered)
            grabbed.texte.halign = "left"
            self.remove_widget(grabbed)
            self.bind(children=self.reorder)
            self.add_widget(grabbed, actual_index)
            for it in self.children:
                it.opacity = 1
            self.grabbed = None
            self.last_hovered = None

        super().on_touch_up(touch)

    def reorder(self, *args):
        self.unbind(children=self.reorder)
        items_index = [x.data["id"] for x in self.children]
        with db_session:
            ordre = db.Ordre.get_or_create(nom="Matiere")
            ordre.ordre = list(reversed(items_index))

    def setup_on_drag(self, initial_y, *args):
        grabbed = self.grabbed
        grabbed.y = initial_y
        grabbed.texte.halign = "center"
        grabbed.opacity = 0.3
        for it in self.children:
            if not it.collide_widget(self.grabbed):
                it.opacity = 0.5
