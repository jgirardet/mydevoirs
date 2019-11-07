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
from mydevoirs.constants import APP_NAME

from mydevoirs.settings import settings_json
from kivy.config import ConfigParser
from kivy.uix.spinner import Spinner


from pony.orm import db_session


from mydevoirs.slide_item import SettingSlider

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
        entry.pop("jour")
        super().__init__(**entry)

    def on_kv_post(self, *args):
        self.loaded_flag = True

    def update_matiere(self, text):
        if self.ids.spinner.is_open and text != self.matiere_nom:
            with db_session:
                a = db.Item[self.entry]
                a.matiere = text
                self.matiere_color = a.matiere.color
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
        print("on dones")
        if self.loaded_flag:
            with db_session:
                db.Item[self.entry].toggle()

    def remove(self):
        self.parent.remove_widget(self)
        with db_session:
            db.Item[self.entry].delete()


class JourItems(GridLayout):
    def __init__(self, date):
        super().__init__()
        self.date = date

        with db_session:
            widgets = [
                ItemWidget(**i.to_dict())
                for i in db.Item.select(lambda x: x.jour.date == date)
            ]
        for item in widgets:
            self.add_widget(item)


class JourWidget(BoxLayout):
    def __init__(self, date):
        self.date = date  # need in nice_date
        super().__init__()

        self.jouritem = JourItems(date)
        self.jouritem.bind(minimum_height=self.jouritem.setter("height"))
        self.ids.scroll_items.add_widget(self.jouritem)

    @property
    def nice_date(self):
        return self.date.strftime("%A %d %B %Y")

    def add_item(self):
        with db_session:
            jour = db.Jour.get_or_create(date=self.date)
            item = db.Item(jour=jour)
            item_widget = ItemWidget(**item.to_dict())
        self.jouritem.add_widget(item_widget)
        item_widget.ids.spinner.is_open = True


class BaseGrid(GridLayout):

    number_to_show = NumericProperty()
    week_days = None

    def get_week_days(self):
        days = [
            self.day + datetime.timedelta(days=i)
            for i in range(0 - self.day.weekday(), 7 - self.day.weekday())
        ]
        return days[: self.number_to_show]

    def __init__(self, day=None):
        super().__init__(cols=2)
        self.day = day or datetime.date.today()
        self.number_to_show = ConfigParser.get_configparser("app").getint(
            "agenda", "nbjour"
        )
        for d in self.get_week_days():
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


# MyDevoirsApp().run()
