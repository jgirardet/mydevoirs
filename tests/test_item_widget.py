from mydevoirs import __version__
from mydevoirs.itemwidget import ItemWidget  # , Clock, JourItems, JourWidget, BaseGrid


from pony.orm import db_session, delete
from mydevoirs.database.database import db, db_init
from mydevoirs.constants import MATIERES
import datetime
from unittest.mock import patch, MagicMock
import pytest
from kivy.config import ConfigParser
from .fixtures import *
from kivy.uix.dropdown import DropDown
from mydevoirs.matiere_dropdown import MatiereOption
from mydevoirs.datas import datas
import pytest


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
        touch = get_touch(spin)
        touch.click()
        self.render(item)

        self.Window.children[0].select(MatiereOption(text="Divers"))
        with db_session:
            it = db.Item[self.FIRST.id]
            assert self.FIRST.matiere.nom == "Grammaire"
            assert it.matiere.nom == "Divers"

        assert item.matiere_nom == "Divers"
        assert item.ids.textinput.focus == True
        assert item.ids.textinput.cursor_col == len(item.ids.textinput.text)

    def test_done(self):

        for n in [1, 2]:
            with db_session:
                d = db.Item[n].to_dict()

            item = ItemWidget(**d)
            self.render(item)

            touch = get_touch(item.ids.done)
            touch.click()

            with db_session:
                if db.Item[n].done:
                    assert item.ids.image_done.source == datas["icon_checked"]
                else:
                    assert item.ids.image_done.source == datas["icon_unchecked"]
                assert db.Item[n].done != d["done"]

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

    def test_on_content_job_cancel_if_previous(self):
        item = ItemWidget(**self.FIRST.to_dict())
        assert item.loaded_flag, "should be loaded"
        assert item.job is None, "There is no job at init"

        item.ids.textinput.text = "emptyjob"
        assert item.job.is_triggered, "no previous job, no error"
        item.job.cancel()

        fakejob = MagicMock()
        item.job = fakejob
        item.job.is_triggered = 0
        item.ids.textinput.text = "untriggeredjob"
        assert not fakejob.cancel.called, "no trigger,  no cancel"

        fakejob = MagicMock()
        item.job = fakejob
        item.job.is_triggered = 1
        item.ids.textinput.text = "triggredjob"
        assert fakejob.cancel.called, "no trigger,  no cancel"

        assert item.job.is_triggered, "a job sould be triggered after content"

        # simule le timeout
        item.job.callback()
        item.job.cancel()

        with db_session:
            assert db.Item[self.FIRST.id].content == item.ids.textinput.text
        assert item.ids.textinput.text == item.content
