from unittest.mock import MagicMock, patch

from kivy.uix.widget import Widget
from pony.orm import db_session

from mydevoirs.agenda import JourWidget
from mydevoirs.itemwidget import (
    ContentTextInput,
    EffacerPopup,
    ItemWidget,
    ValidationPopup,
)
from mydevoirs.matieredropdown import MatiereDropdown, MatiereOption
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

    def test_updatematiere(self):
        a = f_item(matiere="Grammaire")
        item = ItemWidget(**a.to_dict())

        self.render(item)
        spin = item.ids.spinner
        spin.trigger_action(0)

        with db_session:
            divers = db.Matiere.get(nom="Divers")
        dd = self.Window.children[0]
        dd.select(MatiereOption(text="Divers", matiere_id=divers.id))
        with db_session:
            it = db.Item[a.id]
            assert a.matiere.nom == "Grammaire"
            assert it.matiere.nom == "Divers"

        assert item.matiere_nom == "Divers"
        assert item.ids.textinput.focus
        assert item.ids.textinput.cursor_col == len(item.ids.textinput._lines[-1])

        # no change:
        assert item.update_matiere(divers.id) is None

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

    # class TestItemWidgetoncontent(self):
    #     def setUp():

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
        self.add_to_window(b)

        b.ids.remove_item.trigger_action(0)

        self.window.children[0].content.ids.oui.state == "down"

        self.window.children[0].content.ids.oui.trigger_action(0)
        assert b not in self.window.children

    def test_remove_non(self):
        b = ItemWidget(**f_item().to_dict())

        self.add_to_window(b)
        b.ids.remove_item.trigger_action(0)

        self.window.children[0].content.ids.non.trigger_action(0)
        assert b in self.window.children

    def test_maitere_police_size(self):
        b = ItemWidget(**f_item(matiere="Mathématiques").to_dict())
        self.add_to_window(b)
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


app_agenda = MagicMock()
app_agenda.sm.current = "agenda"


class TestContentTextIput(MyDevoirsTestCase):
    @patch("mydevoirs.itemwidget.App.get_running_app", return_value=app_agenda)
    def test_keyboard_key_down(self, rapp):
        rapp.sm.current.return_value = "agenda"
        d = f_jour()
        f_item(jour=d.date)
        j = JourWidget(d.date)
        inp = j.items[0]
        self.render(j)

        # nouveau
        inp.ids.textinput.focus = True
        self.press_key("n", modifier="ctrl")
        assert isinstance(self.window.children[0], MatiereDropdown)
        assert len(j.items) == 2
        self.window.remove_widget(self.window.children[0])

        # duplicate
        inp.ids.textinput.focus = True
        self.press_key("d", modifier="ctrl")
        assert len(j.items) == 3
        assert j.items[0].ids.textinput.focus

        # afficher matier option
        # no need to be refocus
        assert all(not isinstance(x, MatiereDropdown) for x in self.window.children)
        self.press_key("m", modifier="ctrl")
        assert isinstance(self.window.children[0], MatiereDropdown)
        self.window.remove_widget(self.window.children[0])

        # effacer
        inp.ids.textinput.focus = True
        assert inp in j.items
        self.press_key("e", modifier="ctrl")
        popup = self.window.children[0]
        popup.content.ids.oui.trigger_action(0)
        assert len(j.items) == 2
        assert inp not in j.items

        # check True if consumed
        assert inp.ids.textinput.keyboard_on_key_down("w", (0, "e"), "test", ["ctrl"])

        # False no key
        assert not inp.ids.textinput.keyboard_on_key_down(
            "w", (0, "zzz"), "test", ["ctrl"]
        )
        assert not inp.ids.textinput.keyboard_on_key_down("w", (0, "zzz"), "test", [])



class TestEffacerPopup(MyDevoirsTestCase):
    def setUp(self):
        super().setUp()
        d = f_jour()
        f_item(jour=d.date)
        self.j = JourWidget(d.date)
        inp = self.j.items[0]
        self.popup = EffacerPopup(content=ValidationPopup(item=inp))
        self.popup.open()

    def test_keyboard_key_down(self):

        # oui preselectionné
        assert self.popup.content.ids.oui.state == "down"
        assert self.popup.content.ids.non.state == "normal"

        # fleches
        self.press_key("left")
        assert self.popup.content.ids.oui.state == "normal"
        assert self.popup.content.ids.non.state == "down"  # fleches

        # fleches
        self.press_key("left")
        assert self.popup.content.ids.oui.state == "down"
        assert self.popup.content.ids.non.state == "normal"

        self.press_key("right")
        assert self.popup.content.ids.oui.state == "normal"
        assert self.popup.content.ids.non.state == "down"

    def test_non(self):
        self.press_key("right")
        self.press_key("enter")
        assert self.j.items[0].ids.textinput.focus

    def test_oui(self):
        self.press_key("enter")
        assert self.j.items == []

    def test_other_key(self):
        assert not self.popup.content.keyboard_on_key_down(
            "window", (0, "okmk"), "text", "modifier"
        )
        assert self.popup.content.keyboard_on_key_down(
            "window", (0, "enter"), "text", "modifier"
        )
