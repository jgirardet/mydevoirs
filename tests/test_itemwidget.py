from unittest.mock import MagicMock, patch

from kivy.uix.widget import Widget
from pony.orm import db_session

from mydevoirs.itemwidget import ItemWidget  # , Clock, JourItems, JourWidget, BaseGrid
from mydevoirs.matieredropdown import MatiereOption
from mydevoirs.utils import datas

from .fixtures import *


class ItemWidgetTestCase(MyDevoirsTestCase):
    def test_init(self):
        self.check_super_init("BoxLayout", ItemWidget, **f_item().to_dict())

    def test_kv_post(self):
        """ No update on init """
        # setup
        it = f_item(content="bla", done=False)
        # with db_session:
        dico = it.to_dict()
        item = ItemWidget(**dico)

        # test on_content
        self.assertIsNone(item.job)

        # test on_done
        with db_session:
            assert db.Item[dico["id"]].done == dico["done"]

        # test_update_matiere
        with patch.object(ItemWidget, "update_matiere"):
            item = ItemWidget(**dico)
            assert not item.update_matiere.called

    def test_aaa_updatematiere(self):
        # don't chage test name, I don't know why...
        a = f_item(matiere="Grammaire")
        item = ItemWidget(**a.to_dict())

        self.render(item)

        spin = item.ids.spinner
        spin.trigger_action(0)

        self.Window.children[0].select(MatiereOption(text="Divers"))
        with db_session:
            it = db.Item[a.id]
            assert a.matiere.nom == "Grammaire"
            assert it.matiere.nom == "Divers"

        assert item.matiere_nom == "Divers"
        assert item.ids.textinput.focus
        print(item.ids.textinput._lines)
        assert item.ids.textinput.cursor_col == len(item.ids.textinput._lines[-1])

        # no change:
        assert item.update_matiere("Divers") is None

    def test_done(self):

        done = f_item(done=True)
        undone = f_item(done=False)

        for n in [done, undone]:
            # with db_session:
            d = n.to_dict()
            x = d["id"]

            item = ItemWidget(**d)

            item.ids.done.trigger_action(0)
            with db_session:
                if not n.done:
                    assert item.ids.image_done.source == datas["icon_checked"]
                else:
                    assert item.ids.image_done.source == datas["icon_unchecked"]
                assert db.Item[n.id].done != d["done"]

    def test_on_content(self):
        first = f_item()
        item = ItemWidget(**first.to_dict())
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
            assert db.Item[first.id].content == item.ids.textinput.text
        assert item.ids.textinput.text == item.content

    def test_remove_after_confirmation(self):
        a = Widget()
        b = ItemWidget(**f_item().to_dict())
        second = f_item()
        c = ItemWidget(**second.to_dict())
        a.add_widget(b)
        a.add_widget(c)

        c.remove_after_confirmation()

        assert b in a.children
        assert c not in a.children

        with db_session:
            assert not db.Item.exists(lambda x: x.id == second.id)

    def test_remove_oui(self):
        b = ItemWidget(**f_item().to_dict())
        window = self.add_to_window(b)

        b.ids.remove_item.trigger_action(0)

        window.children[0].content.ids.oui.trigger_action(0)
        assert b not in window.children

    def test_remove_non(self):
        b = ItemWidget(**f_item().to_dict())

        window = self.add_to_window(b)
        b.ids.remove_item.trigger_action(0)

        window.children[0].content.ids.non.trigger_action(0)
        assert b in window.children

    def test_maitere_police_size(self):
        b = ItemWidget(**f_item(matiere="Mathématiques").to_dict())
        window = self.add_to_window(b)
        sp = b.ids.spinner
        sp.size_hint_x = 0.1
        self.render(b)
        assert sp.is_shortened

        assert sp.valign == "middle"

    def test_size_depends_text_input_size(self):
        b = ItemWidget(**f_item(matiere="Mathématiques").to_dict())
        b.content = "Une ligne"
        assert b.height == b.ids.textinput.minimum_height
        b.content = "Une ligne\n2lignes"
        assert b.height == b.ids.textinput.minimum_height
