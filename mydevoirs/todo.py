from kivy.app import App
from kivy.properties import (
    BooleanProperty,
    DictProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from pony.orm import db_session

from mydevoirs.agenda import ItemWidget
from mydevoirs.database.database import db


class TodoItemWidget(ItemWidget):
    def on_done(self, *args):
        super().on_done(*args)
        if self.loaded_flag:
            app = App.get_running_app()
            app.todo.reload()
            print("ok", app)


class Todo(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.todolist = TodoList()
        self.add_widget(self.todolist)

    def reload(self):
        self.remove_widget(self.todolist)
        self.todolist = TodoList()
        self.add_widget(self.todolist)


class DateLabel(Label):
    pass


class TodoList(BoxLayout):

    progression = StringProperty("0/0")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box = BoxLayout(orientation="vertical", size_hint_y=None)
        self.box.bind(minimum_height=self.box.setter("height"))
        self.load_items()
        sc = ScrollView(do_scroll_x=False)
        sc.add_widget(self.box)
        self.add_widget(sc)

    def load_items(self):
        with db_session:
            items = [x.to_dict() for x in db.Item.todo_list()]

        if not items:
            return
        date_en_cours = items[0]["date"]

        self.add_date_label(date_en_cours)
        for it in items:
            if it["date"] != date_en_cours:
                date_en_cours = it["date"]
                self.add_date_label(it["date"])
            self.box.add_widget(TodoItemWidget(**it))

    def add_date_label(self, date):
        self.box.add_widget(DateLabel(text=date.strftime("%A %d %B %Y")))
