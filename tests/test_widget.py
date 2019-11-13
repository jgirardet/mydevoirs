from mydevoirs import __version__
from mydevoirs.widgets import ItemWidget, Clock, JourItems, JourWidget, BaseGrid


from pony.orm import db_session, delete
from mydevoirs.database.database import db, db_init
from mydevoirs.constants import MATIERES
import datetime
from unittest.mock import patch, MagicMock
import pytest
from kivy.config import ConfigParser

from .fixtures import *


db_init()


test_setup()


class ItemWidgetTestCase(MyDevoirsTestCase):
    def setUp(self):
        super().setUp()

        with db_session:
            self.JOUR = db.Jour(date=datetime.date.today())
            self.MAT = db.Matiere["Grammaire"]
            self.FIRST = db.Item(content="un", matiere=self.MAT, jour=self.JOUR)
            self.SECOND = db.Item(
                content="deux", matiere=self.MAT, jour=self.JOUR, done=True
            )

    def test_kv_post(self):
        """ No update on init """
        # setup
        with db_session:
            dico = db.Item(content="bla", jour=self.JOUR.date).to_dict()
        item = ItemWidget(**dico)

        # test on_content
        self.assertIsNone(item.job)

        # test on_done
        with db_session:
            assert db.Item[dico["id"]].done == dico["done"]

        # test_update_matiere
        with patch.object(ItemWidget, "update_matiere"):
            item = ItemWidget(**dico)
            item.update_matiere.assert_not_called()

    def test_update_matiere(self):
        item = ItemWidget(**self.FIRST.to_dict())
        self.render(item)
        spin = item.ids.spinner
        spin.is_open = True
        spin._dropdown.select("Poésie")

        with db_session:
            it = db.Item[self.FIRST.id]
            assert self.FIRST.matiere.nom == "Grammaire"
            assert it.matiere.nom == "Poésie"

        assert item.matiere_nom == "Poésie"
        assert item.ids.textinput.focus == True
        assert item.ids.textinput.cursor_col == len(item.ids.textinput.text)

    def test_done(self):

        for n in [1, 2]:
            with db_session:
                d = db.Item[n].to_dict()

            item = ItemWidget(**d)
            self.render(item)

            assert item.ids.done.active == d["done"]

            touch = get_touch(item.ids.done)
            touch.click()

            with db_session:
                self.assertTrue(db.Item[n].done == (not d["done"]))

    def test_on_content(self):
        item = ItemWidget(**self.FIRST.to_dict())
        assert item.loaded_flag
        assert item.job is None
        item.ids.textinput.text = "mok"
        item.job.callback()
        item.job.cancel()  #
        with db_session:
            assert db.Item[self.FIRST.id].content == item.ids.textinput.text
        assert item.ids.textinput.text == item.content


class JourItemsTestCase(MyDevoirsTestCase):
    def setUp(self):

        super().setUp()

        self.a = item_today()
        self.b = item_today()
        self.c = item_today()

        self.jouritems = JourItems(self.a.jour.date)

        self.render(self.jouritems)

    def test_load(self):

        assert len(self.jouritems.children) == 3
        assert self.jouritems.children[0].entry == self.c.id

    def test_remove(self):

        remove_item = self.jouritems.children[0].ids.remove_item
        touch = get_touch(remove_item)
        touch.click()
        assert len(self.jouritems.children) == 2

        assert self.jouritems.children[1].entry == self.a.id
        assert self.jouritems.children[0].entry == self.b.id

        with db_session:
            assert self.c.id not in db.Item.select()


class JourWidgetTestCase(MyDevoirsTestCase):
    def setUp(self):

        super().setUp()

        self.a = item_today()
        self.b = item_today()
        self.c = item_today()

    def test_nice_date(self):
        jour = JourWidget(datetime.date(2019, 11, 12))
        assert jour.ids.titre_jour.text == "mardi 12 novembre 2019"

    def test_add(self):
        jour = JourWidget(self.a.jour.date)
        self.render(jour)
        assert len(jour.jouritem.children) == 3

        get_touch(jour.ids.add_button).click()
        self.render(jour)

        assert len(jour.jouritem.children) == 4
        assert jour.jouritem.children[0].ids.spinner.is_open

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
