from kivy.clock import Clock
from kivy.properties import ColorProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from pony.orm import db_session

from mydevoirs.database import db
from mydevoirs.imagebutton import ImageButton
from mydevoirs.ouinonpopup import OuiNonPopup
from mydevoirs.utils import datas

MATIERE_ITEM_HEIGHT = 30
OPACITY_UNSELECTED = 0.5


class AddButton(ImageButton):
    """Add a matière"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = datas["icon_new"]
        # self.bind(release=self.parent.grid.add_item)

    def on_release(self):

        self.parent.grid.add_item(self.parent)


class RemoveButton(ImageButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = datas["icon_unchecked"]

    def on_release(self):
        # def remove(self):
        parent = self.parent
        pop = OuiNonPopup(
            title=f"""Effacer {parent.data['nom']} ?
        Ceci effacera TOUTES les lignes de devoirs de cette matiere
        """,
            on_oui=lambda x: parent.grid.remove_item(parent),
        )
        pop.open()


class MoveButton(ImageButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = datas["icon_arrowmove"]

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):  # pragma: no branch
            parent = self.parent
            grid = parent.grid

            initial_y = parent.y
            parent.diff_y = initial_y - touch.y
            touch.grab(parent)
            grid.grabbed = parent
            parent_index = grid.children.index(parent)
            grid.last_hovered = grid.children[parent_index - 1]
            grid.remove_widget(parent)
            grid.add_widget(parent)
            Clock.schedule_once(lambda dt: grid.setup_on_drag(initial_y))
            return True


class MatiereItem(BoxLayout):

    bgColor = ColorProperty()
    texte = ObjectProperty()

    def __init__(self, data, grid, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.data = data
        self.grid = grid
        self.height = MATIERE_ITEM_HEIGHT
        self.size_hint_y = None
        self.texte = MatiereInput(size_hint_x=0.9)
        self.bind(bgColor=self.texte.setter("background_color"))
        self.add_widget(self.texte)
        self.add_widget(AddButton(size_hint_x=0.1))
        self.add_widget(MoveButton(size_hint_x=0.1))
        remove = RemoveButton(size_hint_x=0.1)
        self.add_widget(remove)
        self.bgColor = data["color"]

    def __repr__(self):
        return (
            f"MatireItem[{self.data['nom']}]"
            if hasattr(self, "data")
            else super().__repr__()
        )

    def on_touch_move(self, touch):
        if grabbed := self.grid.grabbed:

            if self.collide_point(touch.x, touch.y) and self != grabbed:
                self.opacity = 1
                self.grid.last_hovered = self
            else:
                self.opacity = OPACITY_UNSELECTED
        else:
            return


class MatiereInput(TextInput):

    multiline = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_parent(self, instance, parent):
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
            return True

        elif touch.button == "right":  # pragma: no branch
            self.colorpopup = ColorPopup(
                title=f"Couleur pour {self.parent.data['nom']}",
                color=self.background_color,
            )
            self.colorpopup.bind(color=self.update_color)
            self.colorpopup.open()
            return True

    @db_session
    def update_color(self, popup, color):
        self.parent.bgColor = color
        db.Matiere[self.parent.data["id"]].color = color

    @db_session
    def on_text_changed(self, instance, text):
        if not text:  # block la souvegarde d'une matiere sans nom
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

    def on_touch_move(self, touch):

        if grabbed := self.grabbed:
            grabbed.pos = (0, touch.y + grabbed.diff_y)
        super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if grabbed := self.grabbed:
            actual_index = self.children.index(self.last_hovered)
            grabbed.texte.halign = "left"
            self.remove_widget(grabbed)
            self.bind(children=self.teardown_on_drag)
            self.add_widget(grabbed, actual_index)
            for it in self.children:
                it.opacity = 1
            self.grabbed = None
            self.last_hovered = None

        super().on_touch_up(touch)

    @db_session
    def add_item(self, instance):
        index = self.children.index(instance) + 1
        matiere = db.Matiere(nom="nouvelle matière", color=[1, 1, 1, 1])
        mat_item = MatiereItem(matiere.to_dict(), self)
        self.add_widget(mat_item, index)
        mat_item.texte.focus = True
        mat_item.texte.select_all()
        self.save_order()

    @db_session
    def load_items(self):
        for it in db.Matiere.get_ordered():
            self.add_widget(MatiereItem(it, self))

    @db_session
    def remove_item(self, instance):
        self.remove_widget(instance)
        db.Matiere[instance.data["id"]].delete()
        self.save_order()

    def save_order(self):
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
                it.opacity = OPACITY_UNSELECTED

    def teardown_on_drag(self, *args):
        self.unbind(children=self.save_order)
        self.save_order()


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
    def reload(self):
        self.clear_widgets()
        self.colorlist = ColorList(size_hint_y=None)
        self.colorlist.bind(minimum_height=self.colorlist.setter("height"))
        sc = ScrollView(do_scroll_x=False)
        sc.add_widget(self.colorlist)
        self.add_widget(sc)
