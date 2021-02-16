import datetime
from unittest.mock import MagicMock

import freezegun
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
from mydevoirs.matieredropdown import MatiereDropdown
from mydevoirs.utils import get_config

from .fixtures import *


class AgendaItemWidgetTestCase(MyDevoirsTestCase):
    def setUp(self, no_db=False):
        super().setUp(no_db)
        # nexecessaire pour utiliser app dans kv independant
        from mydevoirs.app import MyDevoirsApp

        self.myapp = MyDevoirsApp()

    def tearDown(self):
        super().tearDown()
        self.myapp.stop()

    def test_rine(self):
        assert True

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
    def setUp(self, no_db=False):
        super().setUp(no_db)
        # nexecessaire pour utiliser app dans kv independant
        from mydevoirs.app import MyDevoirsApp

        self.myapp = MyDevoirsApp()

    def tearDown(self):
        super().tearDown()
        self.myapp.stop()

    def test_init(self):
        self.check_super_init("BoxLayout", JourItems, datetime.date.today())

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
    def setUp(self, no_db=False):
        super().setUp(no_db)
        # nexecessaire pour utiliser app dans kv independant
        from mydevoirs.app import MyDevoirsApp

        self.myapp = MyDevoirsApp()

    def tearDown(self):
        super().tearDown()
        self.myapp.stop()

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

        assert len(jour.jouritem.children) == 4
        assert any(isinstance(x, DropDown) for x in self.Window.children)
        with db_session:
            assert db.Item[jour.jouritem.children[0].entry]

    def test_add_matiere_dropdown_correctly_called(self):
        day = f_jour()
        jour = JourWidget(day.date)
        self.render(jour)
        jour.ids.add_button.trigger_action(0)

        dd = [x for x in self.Window.children if isinstance(x, MatiereDropdown)][0]
        dd.select(dd.options[0])
        # should simply not failed

    def test_add_udpate_progression(self):
        day = f_jour()
        jour = JourWidget(day.date)
        self.render(jour)
        assert jour.progression == "0/0"
        jour.add_item()
        assert jour.progression == "0/1"

    def test_remove_item_upate_progression(self):
        day = f_jour()
        for i in range(3):
            f_item(jour=day.date)

        jour = JourWidget(day.date)
        self.render(jour)
        assert len(jour.jouritem.children) == 3

        entry = jour.jouritem.children[1]
        jour.jouritem.children[1].ids.remove_item.trigger_action(0)

        EventLoop.ensure_window()
        window = EventLoop.window
        window.children[0].content.ids.oui.trigger_action(0)
        with db_session:
            assert not db.Item.get(id=entry.entry)
        assert entry not in jour.jouritem.children
        assert jour.progression == "0/2"

    def test_jour_item(self):
        day = f_jour()
        for i in range(3):
            f_item(jour=day.date)

        jour = JourWidget(day.date)
        assert len(jour.items) == 3


class TestBaseGrid(MyDevoirsTestCase):
    @patch(
        "mydevoirs.agenda.get_config", return_value="lundi",
    )
    def test_get_week_days(self, m):
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

    week_day_params = [
        (
            0,
            [True, True, True, True, True, True, True],
            [
                datetime.date(2019, 11, 11),
                datetime.date(2019, 11, 12),
                datetime.date(2019, 11, 13),
                datetime.date(2019, 11, 14),
                datetime.date(2019, 11, 15),
                datetime.date(2019, 11, 16),
                datetime.date(2019, 11, 17),
            ],
        ),
        (
            0,
            [True, True, False, True, True, False, False],
            [
                datetime.date(2019, 11, 11),
                datetime.date(2019, 11, 12),
                datetime.date(2019, 11, 14),
                datetime.date(2019, 11, 15),
            ],
        ),
        (
            6,
            [True, True, True, True, True, True, True],
            [
                datetime.date(2019, 11, 10),
                datetime.date(2019, 11, 11),
                datetime.date(2019, 11, 12),
                datetime.date(2019, 11, 13),
                datetime.date(2019, 11, 14),
                datetime.date(2019, 11, 15),
                datetime.date(2019, 11, 16),
            ],
        ),
        (
            6,
            [True, False, True, False, True, False, True],
            [
                datetime.date(2019, 11, 10),
                datetime.date(2019, 11, 11),
                datetime.date(2019, 11, 13),
                datetime.date(2019, 11, 15),
            ],
        ),
        (
            3,
            [True, True, True, True, True, True, True],
            [
                datetime.date(2019, 11, 14),
                datetime.date(2019, 11, 15),
                datetime.date(2019, 11, 16),
                datetime.date(2019, 11, 17),
                datetime.date(2019, 11, 18),
                datetime.date(2019, 11, 19),
                datetime.date(2019, 11, 20),
            ],
        ),
    ]

    def test___get_week_days(self):
        day = datetime.date(2019, 11, 16)  # c'est un samedi == 5
        for n, test in enumerate(self.week_day_params):
            assert list(BaseGrid._get_week_days(day, test[0], test[1])) == test[2]
            print("index ", n, "ok")

    def test___get_week_days_range(self):
        today = datetime.date(2019, 11, 16)  # c'est un samedi == 5
        starts_date = [11, 12, 13, 14, 15, 16, 10]
        starts_day = range(7)
        for date, day in zip(starts_date, starts_day):
            assert list(BaseGrid._get_week_days(today, day, [True] * 7)) == [
                datetime.date(2019, 11, date) + datetime.timedelta(days=n)
                for n in range(7)
            ]

    def test_init(self):
        self.check_super_init("GridLayout", BaseGrid)

        self.app.config["agenda"].update({k: "1" for k in SEMAINE})
        b = BaseGrid()
        assert b.get_days_to_show() == [True] * 7
        assert len(b.children) == 7

        self.app.config["agenda"].update({k: "0" for k in SEMAINE})
        b = BaseGrid()
        assert b.get_days_to_show() == [False] * 7
        assert len(b.children) == 0

        b = BaseGrid(day=datetime.date(2019, 7, 18))
        assert b.day == datetime.date(2019, 7, 18)


class TestCaroussel(MyDevoirsTestCase):
    def test_init(self):
        CarouselWidget()
        self.check_super_init("Carousel", CarouselWidget)

        d = datetime.date(2015, 12, 11)
        c = CarouselWidget(day=d)
        assert c.index == 1

        # also test Carousel.on_done
        assert c.slides[0].day == datetime.date(2015, 12, 4)
        assert c.slides[1].day == datetime.date(2015, 12, 11)
        assert c.slides[2].day == datetime.date(2015, 12, 18)

    def test_on_index_1(self):
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
        assert c.index == 1
        assert c.slides == [un, deux, trois]

    def test_on_index_0(self):

        d = datetime.date(2015, 12, 11)
        c = CarouselWidget(day=d)
        un, deux, trois = c.slides

        c.on_index(None, 0)

        quatre = c.slides[0]
        assert c.slides == [quatre, un, deux]
        assert len(c.slides) == 3

    def test_on_index_2(self):
        d = datetime.date(2020, 7, 6)
        c = CarouselWidget(day=d)
        un, deux, trois = c.slides

        c.on_index(None, 2)

        quatre = c.slides[2]
        assert c.slides == [deux, trois, quatre]
        assert len(c.slides) == 3

    def test_auto_next_week(self):
        # vendredi rien ne change
        with patch(
            "mydevoirs.agenda.BaseGrid", side_effect=lambda x: Widget(),
        ):
            # AUTONEXTWEEK  = FALSE
            self.app.config["agenda"].update({"auto_next_week": "0"})
            # vendredi
            with freezegun.freeze_time("2020-07-10"):
                c = CarouselWidget()
                assert c.date == datetime.date(2020, 7, 10)

            # samedi

            with freezegun.freeze_time("2020-07-11"):
                c = CarouselWidget()
                assert c.date == datetime.date(2020, 7, 11)

            # autoweek = TRUE
            self.app.config["agenda"].update({"auto_next_week": "1"})
            # vendredi
            with freezegun.freeze_time("2020-07-10"):
                c = CarouselWidget()
                assert c.date == datetime.date(2020, 7, 10)

            # samedi
            with freezegun.freeze_time("2020-07-11"):
                c = CarouselWidget()
                assert c.date == datetime.date(2020, 7, 14)

            # dimanche
            with freezegun.freeze_time("2020-07-12"):
                c = CarouselWidget()
                assert c.date == datetime.date(2020, 7, 15)


class TestAgendaScreen(MyDevoirsTestCase):
    def test_init(self):
        self.check_super_init("Screen", Agenda)

    def test_go_date(self):
        b = Agenda()
        assert b.carousel.date == datetime.date.today()
        b.go_date(datetime.date(2012, 3, 2))
        assert b.carousel.date == datetime.date(2012, 3, 2)
