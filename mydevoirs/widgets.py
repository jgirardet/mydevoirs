from pathlib import Path

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import (
    StringProperty,
    ObjectProperty,
    ListProperty,
    NumericProperty,
    BooleanProperty,
    DictProperty,
)
from kivy.clock import Clock
from kivy.uix.carousel import Carousel
import datetime
import locale
from mydevoirs.database.database import db
from mydevoirs.constants import SEMAINE
from mydevoirs.matiere_dropdown import MatiereDropdown
from kivy.config import ConfigParser

import itertools
from pony.orm import db_session
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from functools import partial

locale.setlocale(locale.LC_ALL, "fr_FR.utf8")


class ItemWidget(BoxLayout):
    content = StringProperty()
    done = BooleanProperty()
    matiere_nom = StringProperty()
    matiere_color = ListProperty()

    def __init__(self, **entry):
        self.loaded_flag = False
        self.job = None

        self.entry = entry.pop("id")
        self.date = entry.pop("date")
        entry.pop("jour")
        super().__init__(**entry)
        self._jour_widget = None

    def on_kv_post(self, *args):
        self.loaded_flag = True

    def update_matiere(self, text):
        if text != self.matiere_nom:
            with db_session:
                a = db.Item[self.entry]
                a.matiere = text
                self.matiere_color = a.matiere.color
                self.matiere_nom = text
            content = self.ids.textinput
            content.focus = True
            content.do_cursor_movement("cursor_end")

    def on_content(self, _, text):
        if self.loaded_flag:
            if self.job:
                self.job.cancel()
            self.job = Clock.schedule_once(partial(self._set_content, text), 0.5)

    def _set_content(self, content, *args):
        with db_session:
            db.Item[self.entry].content = content

    def on_done(self, *args):
        if self.loaded_flag:
            with db_session:
                db.Item[self.entry].toggle()
            if self.jour_widget: 
                self.jour_widget.update_progression()
            else:
                self.parent.parent.parent.parent.reload()

    @property
    def jour_widget(self):
        if not self._jour_widget:
            for x in self.walk_reverse():
                if isinstance(x, JourWidget) and x.date == self.date:
                    self._jour_widget = x
        return self._jour_widget

    def remove(self):
        EffacerPopup(item=self).open()

    def remove_after_confirmation(self):
        with db_session:
            db.Item[self.entry].delete()
        self.parent.remove_widget(self)


class JourItems(GridLayout):
    def __init__(self, date):
        super().__init__()
        self.date = date

        with db_session:
            query = db.Item.select(lambda x: x.jour.date == date)
            widgets = [ItemWidget(**i.to_dict()) for i in query]
        for item in widgets:
            self.add_widget(item)


class JourWidget(BoxLayout):

    progression = StringProperty("0/0")

    def __init__(self, date):
        self.date = date  # need in nice_date
        super().__init__()

        self.jouritem = JourItems(date)
        self.jouritem.bind(minimum_height=self.jouritem.setter("height"))
        self.ids.scroll_items.add_widget(self.jouritem)
        self.update_progression()

    def update_progression(self):
        with db_session:
            pro = db.Jour.get_or_create(date=self.date).progression
            self.progression = f"{pro[0]}/{pro[1]}"

    @property
    def nice_date(self):
        return self.date.strftime("%A %d %B %Y")

    def add_item(self):
        with db_session:
            jour = db.Jour.get_or_create(date=self.date)
            item = db.Item(jour=jour)
            item_widget = ItemWidget(**item.to_dict())
        self.jouritem.add_widget(item_widget)
        MatiereDropdown().open(item_widget.ids.spinner)
        # if self.jouritem.height >  self.ids.scroll_items.height:
        #     self.add_widget(Button(text="ça dépasse "))


class BaseGrid(GridLayout):

    number_to_show = NumericProperty()

    def get_week_days(self, jours):
        days = [
            self.day + datetime.timedelta(days=i)
            for i in range(0 - self.day.weekday(), 7 - self.day.weekday())
        ]
        return itertools.compress(days, jours)

    @staticmethod
    def get_days_to_show():
        cp = ConfigParser.get_configparser("app")
        return [cp.getboolean("agenda", j) for j in SEMAINE]

    def __init__(self, day=None):
        super().__init__(cols=2)
        self.day = day or datetime.date.today()

        jours = self.get_days_to_show()
        for d in self.get_week_days(jours):
            self.add_widget(JourWidget(d))


class CarouselWidget(Carousel):
    def __init__(self, day=None):
        today = day or datetime.date.today()
        super().__init__()

        self.add_widget(BaseGrid(today - datetime.timedelta(weeks=1)))
        self.add_widget(BaseGrid(today))
        self.add_widget(BaseGrid(today + datetime.timedelta(weeks=1)))

        self.index = 1

    def on_index(self, *args):

        super().on_index(*args)

        index = args[1]

        if index == 1:
            return

        sens = 0 if index else -1

        # can't remove the if statement/don't why.
        if index == 0:
            self.add_widget(
                BaseGrid(self.slides[index].day - datetime.timedelta(weeks=1)), sens
            )
            self.remove_widget(self.slides[sens])

        elif index == 2:
            # build right
            self.add_widget(
                BaseGrid(self.slides[index].day + datetime.timedelta(weeks=1)), sens
            )
            self.remove_widget(self.slides[sens])

        self.index = 1
        assert len(self.slides) == 3


class EffacerPopup(Popup):
    item = ObjectProperty()

from kivy.uix.widget import Widget


class DateLabel(Label):
    pass

class TodoList(BoxLayout):

    progression = StringProperty("0/0")
    # orientation = "vertical"
    # size_hint = (None, None   )
    # id = "scroll_items"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box = BoxLayout(orientation="vertical", size_hint_y=None)
        self.box.bind(minimum_height=self.box.setter("height"))
        self.load_items()
        sc = ScrollView(do_scroll_x=False)
        sc.add_widget(self.box)
        self.add_widget(sc)
        # self.add_widget(self.box)

    def load_items(self):
        with db_session:
            items = [x.to_dict() for x in  db.Item.todo_list()]

        if not items:
            return
        date_en_cours = items[0]['date']
        
        self.add_date_label(date_en_cours)
        for it in items:
            if it['date'] != date_en_cours:
                date_en_cours = it['date']
                self.add_date_label(it['date'])
            self.box.add_widget(ItemWidget(**it))

    def add_date_label(self, date):
        self.box.add_widget(DateLabel(text=date.strftime("%A %d %B %Y")))


        # self.jouritem = JourItems(date)
        # self.jouritem.bind(minimum_height=self.jouritem.setter("height"))
        # self.ids.scroll_items.add_widget(self.jouritem)
        # self.update_progression()

    # def update_progression(self):
    #     with db_session:
    #         pro = db.Jour.get_or_create(date=self.date).progression
    #         self.progression = f"{pro[0]}/{pro[1]}"