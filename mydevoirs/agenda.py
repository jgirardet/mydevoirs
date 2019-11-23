import datetime
import itertools

from kivy.config import ConfigParser
from kivy.properties import (
    BooleanProperty,
    DictProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from pony.orm import db_session

from mydevoirs.constants import SEMAINE
from mydevoirs.database.database import db
from mydevoirs.itemwidget import ItemWidget
from mydevoirs.matiere_dropdown import MatiereDropdown


class AgendaItemWidget(ItemWidget):
    def __init__(self, **kwargs):
        self._jour_widget = None
        super().__init__(**kwargs)

    def on_done(self, *args):
        super().on_done(*args)
        if self.loaded_flag:
            self.jour_widget.update_progression()

    @property
    def jour_widget(self):
        if not self._jour_widget:
            for x in self.walk_reverse():
                if isinstance(x, JourWidget) and x.date == self.date:
                    self._jour_widget = x
        return self._jour_widget


class JourItems(BoxLayout):
    def __init__(self, date):
        super().__init__()
        self.date = date

        with db_session:
            query = db.Item.select(
                lambda x: x.jour.date == date
            )  # pragma: no cover_all
            widgets = [AgendaItemWidget(**i.to_dict()) for i in query]
        for item in widgets:
            self.add_widget(item)


class JourWidget(BoxLayout):

    progression = StringProperty("0/0")

    def __init__(self, date, **kwargs):
        self.date = date  # need in nice_date
        super().__init__(**kwargs)

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
            item_widget = AgendaItemWidget(**item.to_dict())
        self.jouritem.add_widget(item_widget)
        MatiereDropdown().open(item_widget.ids.spinner)


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
        try:
            cp = ConfigParser.get_configparser("app")
            return [cp.getboolean("agenda", j) for j in SEMAINE]
        except AttributeError:
            return [True, True, False, True, True, False, False]

    def build_grid(self, jours):
        for d in self.get_week_days(jours):
            self.add_widget(JourWidget(d))

    def __init__(self, day=None):
        super().__init__(cols=2)
        self.day = day or datetime.date.today()
        self.build_grid(self.get_days_to_show())


class CarouselWidget(Carousel):
    def __init__(self, day=None):
        self.date = day or datetime.date.today()
        super().__init__()

        self.add_widget(BaseGrid(self.date - datetime.timedelta(weeks=1)))
        self.add_widget(BaseGrid(self.date))
        self.add_widget(BaseGrid(self.date + datetime.timedelta(weeks=1)))

        self.index = 1

    def on_index(self, *args):

        super().on_index(*args)
        print("mlokk", self.current_slide.day)

        index = args[1]

        if index == 1:
            return

        else:
            sens = 0 if index else -1

            # can't remove the if statement/don't why.
            if index:
                # build right
                self.add_widget(
                    BaseGrid(self.slides[index].day + datetime.timedelta(weeks=1)), sens
                )
                self.remove_widget(self.slides[sens])

            else:
                # build left
                self.add_widget(
                    BaseGrid(self.slides[index].day - datetime.timedelta(weeks=1)), sens
                )
                self.remove_widget(self.slides[sens])

        self.date = self.current_slide.day
        print(self.current_slide.day)
        self.index = 1


    def load_previous(self, *args):
        print(self.current_slide)
        super().load_previous(*args)
        self.date = self.current_slide.day
        print("après previous", self.current_slide.day)
        print(self.current_slide)




class Agenda(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.carousel = CarouselWidget()
        self.add_widget(self.carousel)

    def go_date(self, date=None):
        self.remove_widget(self.carousel)

        self.carousel = CarouselWidget(date)

        self.add_widget(self.carousel)
