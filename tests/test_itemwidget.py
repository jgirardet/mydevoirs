from mydevoirs.itemwidget import ItemWidget  # , Clock, JourItems, JourWidget, BaseGrid


from pony.orm import db_session
import datetime
from unittest.mock import patch, MagicMock
from .fixtures import *
from mydevoirs.matiere_dropdown import MatiereOption
from mydevoirs.datas import datas
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout


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

    def test_init(self):
        self.check_super_init("BoxLayout", ItemWidget, **self.FIRST.to_dict())

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

    def test_aaa_updatematiere(self):
        # don't chage test name, I don't know why...
        a = item_today()
        item = ItemWidget(**a.to_dict())

        self.render(item)

        spin = item.ids.spinner
        touch = get_touch(spin)
        touch.click()

        self.Window.children[0].select(MatiereOption(text="Divers"))
        with db_session:
            it = db.Item[a.id]
            assert a.matiere.nom == "Grammaire"
            assert it.matiere.nom == "Divers"

        assert item.matiere_nom == "Divers"
        assert item.ids.textinput.focus
        assert item.ids.textinput.cursor_col == len(item.ids.textinput.text)

        # no change:
        assert item.update_matiere("Divers") is None

    def test_done(self):

        for n in [0, 1]:
            with db_session:
                d = db.Item.select()[:][n].to_dict()
            x = d["id"]

            item = ItemWidget(**d)
            self.render(item)

            touch = get_touch(item.ids.done)
            touch.click()

            with db_session:
                if db.Item[x].done:
                    assert item.ids.image_done.source == datas["icon_checked"]
                else:
                    assert item.ids.image_done.source == datas["icon_unchecked"]
                assert db.Item[x].done != d["done"]

    def test_on_content(self):
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
        assert fakejob.cancel.called, "trigger then cancel"

        assert item.job.is_triggered, "a job sould be triggered after content"

        # simule le timeout
        item.job.callback()
        item.job.cancel()

        with db_session:
            assert db.Item[self.FIRST.id].content == item.ids.textinput.text
        assert item.ids.textinput.text == item.content

    def test_remove_after_confirmation(self):
        a = Widget()
        b = ItemWidget(**self.FIRST.to_dict())
        c = ItemWidget(**self.SECOND.to_dict())
        a.add_widget(b)
        a.add_widget(c)

        c.remove_after_confirmation()

        assert b in a.children
        assert c not in a.children

        with db_session:
            assert not db.Item.exists(lambda x: x.id == self.SECOND.id)

    def test_remove(self):
        a = BoxLayout()
        b = ItemWidget(**self.FIRST.to_dict(), size_hint=(200, None))
        a.add_widget(b)

        self.render(a)
        t = get_touch(b.ids.remove_item)
        t.click()
        self.render(a)
        oui = get_touch(b.popup.content.ids.oui)
        oui.click()
        self.render(a)

        assert b not in a.children

        with db_session:
            assert not db.Item.exists(lambda x: x.id == self.FIRST.id)
