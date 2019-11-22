# from mydevoirs import __version__
# from mydevoirs.widgets import ItemWidget, Clock, JourItems, JourWidget, BaseGrid
from configparser import ConfigParser
# from mydevoirs.constants import MATIERES
# import datetime
from unittest.mock import MagicMock, patch

from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget

from mydevoirs.agenda import (
    Agenda,
    AgendaItemWidget,
    BaseGrid,
    CarouselWidget,
    JourItems,
    JourWidget,
)
from mydevoirs.constants import SEMAINE

from .fixtures import *

# import pytest
# from kivy.config import ConfigParser


# from mydevoirs.matiere_dropdown import MatiereOption



class AgendaItemWidgetTestCase(MyDevoirsTestCase):
    def test_widget_init(self):

        self.check_super_init("ItemWidget", AgendaItemWidget, **f_item().to_dict())
        it = f_item()
        item = AgendaItemWidget(**it.to_dict())
        assert item.entry == it.id  # super.__init__ called
        assert hasattr(item, "_jour_widget")

    def test_on_done(self):

        # check super call
        with patch("mydevoirs.agenda.ItemWidget.on_done") as e:
            item = AgendaItemWidget(**f_item().to_dict())
            item.loaded_flag = False
            item.on_done()
            assert e.called

        # reste
        item = AgendaItemWidget(**f_item().to_dict())
        item._jour_widget = MagicMock()
        item.on_done()
        assert item.jour_widget.update_progression.called

    def test_jour_widget(self):
        f = f_item()
        jw = JourWidget(f.jour.date)
        item = jw.jouritem.children[0]

        # base behaviour
        assert item.jour_widget == jw

        # test cache
        with patch.object(item, "walk_reverse") as m:
            assert item.jour_widget == jw
            assert not m.called


class JourItemsTestCase(MyDevoirsTestCase):
    def test_init(self):
        self.check_super_init("GridLayout", JourItems, datetime.date.today())

    def test_load(self):

        day = f_jour().date
        f_item(jour=day)
        f_item(jour=day)
        c = f_item(jour=day)

        jouritems = JourItems(day)

        self.render(jouritems)

        assert len(jouritems.children) == 3
        assert jouritems.children[0].entry == c.id


class JourWidgetTestCase(MyDevoirsTestCase):

    def test_init(self):
        self.check_super_init("BoxLayout", JourWidget, datetime.date(1999, 1, 1))

    def test_nice_date(self):
        jour = JourWidget(datetime.date(2019, 11, 12))
        assert jour.ids.titre_jour.text == "mardi 12 novembre 2019"

    def test_add(self):
        day = f_jour()
        for i in range(3):
            f_item(jour=day.date)

        jour = JourWidget(day.date)
        self.render(jour)
        assert len(jour.jouritem.children) == 3
        jour.ids.add_button.trigger_action(0)

        print(jour.jouritem.children)
        # return
        assert len(jour.jouritem.children) == 4
        assert any(isinstance(x, DropDown) for x in self.Window.children)
        with db_session:
            assert db.Item[jour.jouritem.children[0].entry]


class TestBaseGrid(MyDevoirsTestCase):
    def test_get_week_days(self):
        with patch.object(
            BaseGrid,
            "get_days_to_show",
            return_value=[False, True, False, True, False, True, False],
        ):
            b = BaseGrid(day=datetime.date(2019, 11, 12))
            for d, z in zip(
                b.children,
                [
                    datetime.date(2019, 11, 16),
                    datetime.date(2019, 11, 14),
                    datetime.date(2019, 11, 12),
                ],
            ):

                assert d.date == z

    def test_init(self):
        self.check_super_init("GridLayout", BaseGrid)

        cp = ConfigParser()
        cp.add_section("agenda")
        cp["agenda"].update({k: "True" for k in SEMAINE})

        with patch("mydevoirs.agenda.ConfigParser.get_configparser", return_value=cp):
            b = BaseGrid()
            assert b.get_days_to_show() == [True] * 7
            assert len(b.children) == 7

        cp["agenda"].update({k: "False" for k in SEMAINE})
        with patch("mydevoirs.agenda.ConfigParser.get_configparser", return_value=cp):
            b = BaseGrid()
            assert b.get_days_to_show() == [False] * 7
            assert len(b.children) == 0

        with patch("mydevoirs.agenda.ConfigParser.get_configparser", return_value=cp):
            b = BaseGrid(day=datetime.date(2019, 7, 18))
            assert b.day == datetime.date(2019, 7, 18)


class TestCaroussel(MyDevoirsTestCase):
    def test_init(self):
        self.check_super_init("Carousel", CarouselWidget)

        d = datetime.date(2015, 12, 11)
        c = CarouselWidget(day=d)
        assert c.index == 1

        # also test Carousel.on_done
        assert c.slides[0].day == datetime.date(2015, 12, 4)
        assert c.slides[1].day == datetime.date(2015, 12, 11)
        assert c.slides[2].day == datetime.date(2015, 12, 18)

    def test_on_index(self):
        """Carousel slides values:
            0: gauche
            1: centre
            2: droite
            """

        d = datetime.date(2015, 12, 11)
        c = CarouselWidget(day=d)

        un, deux, trois = c.slides
        # in the middle, no move
        c.on_index(None, 1)
        assert c.slides == [un, deux, trois]
        assert len(c.slides) == 3

        # go right/previous
        c.on_index(None, 0)
        assert c.slides[1:3] == [un, deux]
        assert len(c.slides) == 3

        quatre = c.slides[0]

        # then left/after
        c.on_index(None, 2)
        assert c.slides[0:2] == [un, deux]
        cinq = c.slides[2]
        assert trois.day == cinq.day
        assert len(c.slides) == 3

        # then left/after
        c.on_index(None, 2)
        assert c.slides[0:2] == [deux, cinq]
        assert len(c.slides) == 3

        # two times right previous
        c.on_index(None, 0)
        c.on_index(None, 0)
        assert c.slides[2] == deux
        assert len(c.slides) == 3
        for i, j in zip(range(3), [quatre, un, deux]):
            assert c.slides[i].day == j.day


class TestAgendaScreen(MyDevoirsTestCase):
    def test_init(self):
        self.check_super_init("Screen", Agenda)

    def test_go_date(self):
        b = Agenda()
        assert b.carousel.date == datetime.date.today()
        b.go_date(datetime.date(2012, 3, 2))
        assert b.carousel.date == datetime.date(2012, 3, 2)
