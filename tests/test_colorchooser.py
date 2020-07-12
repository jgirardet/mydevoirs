from time import sleep
from unittest.mock import MagicMock, patch

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from pony.orm import db_session

from mydevoirs.colorchooser import (
    ColorChooser,
    MatiereItem,
    AddButton,
    RemoveButton,
    MoveButton,
    MATIERE_ITEM_HEIGHT,
    OPACITY_UNSELECTED,
    ColorPopup,
)

from .fixtures import *


class TestColorChooserScreen(MyDevoirsTestCase):
    def test_init(self):
        self.check_super_init("Screen", ColorChooser)

    def test_reload(self):
        # setup
        a = ColorChooser()
        w = Widget()
        a.add_widget(w)
        a.reload()

        # tests
        assert w not in a.children
        assert a.colorlist

    def test_populate(self):
        a = ColorChooser()
        a.reload()
        assert len(a.colorlist.children) == 14


class TestMatiereItem(MyDevoirsTestCase):
    def test_show_de_base(self):
        a = ColorChooser()
        a.reload()
        poesie = a.colorlist.children[3]
        assert poesie.data["nom"] == "Poésie"
        with db_session:
            pp = db.Matiere[poesie.data["id"]]
            assert pp.nom == "Poésie"
            assert pp.color == poesie.data["color"]


class TestSomeBehaviors(MyDevoirsTestCase):
    def setUp(self):
        super().setUp()
        self.cc = ColorChooser()
        self.cc.reload()
        self.cl = self.cc.colorlist
        self.poesie = self.cl.children[3]
        self.ordre = list(reversed([x.data["id"] for x in self.cl.children]))
        self.render(self.cc)

    def test_new_item(self):
        ab = self.poesie.children[2]
        assert isinstance(ab, AddButton)
        ab.trigger_action(0)
        assert len(self.cl.children) == 15
        assert self.cl.children[3] == self.poesie
        nb = self.cl.children[4]
        assert nb.texte.text == "nouvelle matière"

        # on verifie la ddb
        with db_session:
            obj = db.Matiere[nb.data["id"]]
            assert obj.nom == "nouvelle matière"
            assert obj.color == [1, 1, 1, 1]

            # on verifie l'ordre
            db_ordre = db.Ordre["Matiere"]
            self.ordre.insert(-4, obj.id)
            assert db_ordre.ordre == self.ordre

    def test_delete_item(self):
        ab = self.poesie.children[0]
        assert isinstance(ab, RemoveButton)
        ab.trigger_action(0)
        self.popup_click("oui")
        assert len(self.cl.children) == 13

        assert self.poesie not in self.cl.children

        # on verifie la ddb
        with db_session:
            assert not db.Matiere.get(id=self.poesie.data["id"])
            # on verifie l'ordre
            db_ordre = db.Ordre["Matiere"]
            self.ordre.pop(-4)
            assert db_ordre.ordre == self.ordre

    def do_touchdown(self):
        ab = self.poesie.children[1]
        assert isinstance(ab, MoveButton)
        ev = UnitTestTouch(*ab.pos)
        ev.touch_down()
        ab.on_touch_down(ev)
        parent = ab.parent
        self.advance_frames(5)  # wait async clock

        return ab, ev, parent

    def do_move(self):
        self.do_touchdown()
        ev = UnitTestTouch(30, 10)
        ev.touch_move(1, MATIERE_ITEM_HEIGHT * 10)
        self.cl.on_touch_move(ev)
        self.advance_frames(1)
        return self.cl.grabbed, self.cl.last_hovered

    def test_move_item_touch_down(self):
        ab, ev, parent = self.do_touchdown()
        assert self.cl.grabbed == parent, "parent should be grabbed"
        assert (
            self.cl.children.index(parent) == 0
        ), "parent should be on top of other with 0 index"
        # self.advance_frames(1)  # wait async clock

        # style ui
        assert parent.opacity == 0.3
        assert parent.y == ab.y
        assert parent.texte.halign == "center"
        sciences = self.cl.children[3]
        assert all(
            i.opacity == OPACITY_UNSELECTED
            for i in self.cl.children
            if i not in [parent, sciences]
        )

    def test_move_iteem_move(self):
        _, target = self.do_move()
        math = self.cl.children[-6]
        assert math == target
        assert self.cl.last_hovered == math
        assert math.opacity == 1
        assert self.cl.children[-5].opacity == OPACITY_UNSELECTED
        assert self.cl.children[-7].opacity == OPACITY_UNSELECTED

    def test_move_item_drop(self):
        grabbed, target = self.do_move()
        ev = UnitTestTouch(*target.pos)
        ev.touch_up()
        self.cl.on_touch_up(ev)
        self.advance_frames(1)

        # pos
        ll = len(self.cl.children)
        grabbed_index = self.cl.children.index(grabbed)
        assert grabbed_index == ll - 6  # àl palce de target
        assert self.cl.children.index(target) == ll - 7  # un cran plus bas

        # db
        grabbed_id = self.ordre.pop(self.ordre.index(grabbed.data["id"]))
        self.ordre.insert(-grabbed_index, grabbed_id)
        with db_session:
            assert self.ordre == db.Ordre["Matiere"].ordre

        # UI
        assert all(i.opacity == 1 for i in self.cl.children)
        assert self.cl.grabbed is None
        assert self.cl.last_hovered is None

        # breakpoint()
        # ab.on_touch_up(get_touch(ab))
        # ab.trigger_action(0)
        # self.popup_click("oui")
        # assert len(self.cl.children) == 13
        #
        # assert self.poesie not in self.cl.children
        #
        # # on verifie la ddb
        # with db_session:
        #     assert not db.Matiere.get(id=self.poesie.data["id"])
        #     # on verifie l'ordre
        #     db_ordre = db.Ordre["Matiere"]
        #     self.ordre.pop(-4)
        #     assert db_ordre.ordre == self.ordre


class TestMatiereInputAndColorPopup(MyDevoirsTestCase):
    def setUp(self):
        super().setUp()
        self.cc = ColorChooser()
        self.cc.reload()
        self.cl = self.cc.colorlist
        self.poesie = self.cl.children[3]
        self.render(self.cc)

    def test_onchanged_text(self):
        tx = self.poesie.texte
        lid = self.poesie.data["id"]

        tx.text = "bla"
        with db_session:
            assert db.Matiere[lid].nom == "bla"

        # text vide
        tx.text = ""
        with db_session:
            assert db.Matiere[lid].nom == "bla"

    def test_left_click(self):
        ev = UnitTestTouch(10, self.poesie.y + 5)
        ev.button = "left"
        ev.touch_down()
        assert self.poesie.on_touch_down(ev)

    def test_click_outside(self):
        ev = UnitTestTouch(9999, 9999)
        ev.touch_down()
        assert not self.poesie.on_touch_down(ev)

    def test_right_click(self):

        # on affiche le popup
        ev = UnitTestTouch(10, self.poesie.y + 5)
        ev.button = "right"
        ev.touch_down()
        assert self.poesie.on_touch_down(ev)
        ch: ColorPopup = self.poesie.texte.colorpopup
        self.render(ch)  # jsute pour aider le debug

        # change couleur
        new_c = [0.3, 0.4, 0.5, 1]
        ch.cp.color = new_c
        ch.ok_button.trigger_action(0)
        assert ch.color == new_c
        assert self.poesie.bgColor == new_c

        with db_session:
            assert db.Matiere[self.poesie.data["id"]].color == new_c
