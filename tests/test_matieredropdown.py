from unittest.mock import MagicMock, call

from kivy.base import EventLoop
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget

from mydevoirs.matieredropdown import MatiereDropdown, MatiereOption

from .fixtures import *

MATIERES_TREE = {
    "Français": {"Orthographe": (91, 193, 242), "Rédaction": (0, 120, 255)},
    "Sciences": (255, 177, 88),
    "Histoire-Géo": {"Histoire": (227, 254, 0), "Géographie": (236, 254, 87)},
    "Divers": (89, 253, 89),
}


class MatiereDropdownTestCase(MyDevoirsTestCase):
    def test_init(self):
        self.check_super_init("DropDown", MatiereDropdown)

        w = Widget()
        m = MatiereDropdown(tree=MATIERES_TREE)
        m._create_options(w, None)
        assert [p.text for p in m.children[0].children] == [p.text for p in w.children]

    def test_create(self):
        self.check_super_init("DropDown", MatiereDropdown)

        w = Widget()
        m = MatiereDropdown(tree=MATIERES_TREE)
        m._create_options(w, None)

        res = [str(p) for p in w.children[::-1]]

        assert res == [
            str(MatiereOption(text="Français", has_sub=True)),
            str(MatiereOption(text="Sciences", has_sub=False)),
            str(MatiereOption(text="Histoire-Géo", has_sub=True)),
            str(MatiereOption(text="Divers", has_sub=False)),
        ]

    def test_on_select_has_sub(self):
        EventLoop.ensure_window()
        window = EventLoop.window
        base = Widget()
        window.add_widget(base)
        m = MatiereDropdown(tree=MATIERES_TREE, attach_to=base)

        m.on_select(MatiereOption(text="Français", has_sub=True))

        res = [str(p) for p in window.children[0].children[0].children][::-1]

        assert res == [
            str(MatiereOption(text="Orthographe", has_sub=False)),
            str(MatiereOption(text="Rédaction", has_sub=False)),
        ]

    def test_on_select_not_has_sub(self):
        b1 = Widget()
        b1.update_matiere = MagicMock()
        # b1.update_matiere =
        base = Widget()
        b1.add_widget(base)
        m = MatiereDropdown(tree=MATIERES_TREE, attach_to=base)
        m.on_select(MatiereOption(text="Sciences", has_sub=False))
        assert b1.update_matiere.called
        assert b1.update_matiere.call_args == call("Sciences")

    def test_focus_on_create(self):
        m = MatiereDropdown(tree=MATIERES_TREE)
        # option bold == focused
        assert m.focus
        assert m.focused_index == -1
        assert m.options[-1].bold
        assert not m.options[0].bold

    def test_on_keyboard_keydown(self):
        """ test haut, bas, dépassement des limites, touche entrée"""
        m = MatiereDropdown(tree=MATIERES_TREE)

        # Point de départ
        assert m.focused_index == -1
        assert m.options[3].bold

        # 1 coup en bas
        m.keyboard_on_key_down("window", (274, ""), "omk", "modifier")
        assert m.focused_index == -2
        assert m.options[2].bold
        assert not m.options[3].bold

        # puis 2 coup en bas (donc dernier)
        m.keyboard_on_key_down("window", (274, ""), "omk", "modifier")
        m.keyboard_on_key_down("window", (274, ""), "omk", "modifier")
        assert m.focused_index == -4
        assert m.options[0].bold
        assert not all(x.bold for x in m.options[1:])

        # puis 1 coup en bas (donc dépasse doit repasser premier)
        m.keyboard_on_key_down("window", (274, ""), "omk", "modifier")
        assert m.focused_index == -1
        assert m.options[3].bold
        assert not all(x.bold for x in m.options[-4:-1])

        # puis 1 coup en haut : dépasse revient en position précédente
        m.keyboard_on_key_down("window", (273, ""), "omk", "modifier")
        assert m.focused_index == -4
        assert m.options[0].bold
        assert not all(x.bold for x in m.options[1:])

        # puis 2 coup en haut
        m.keyboard_on_key_down("window", (273, ""), "omk", "modifier")
        m.keyboard_on_key_down("window", (273, ""), "omk", "modifier")
        assert m.focused_index == -2
        assert m.options[2].bold
        assert not m.options[0].bold
        assert not m.options[1].bold
        assert not m.options[3].bold

        # appuyer sur entrée
        m.on_select = MagicMock()
        m.keyboard_on_key_down("window", (13, ""), "omk", "modifier")
        assert m.on_select.called
        assert m.on_select.call_args[0][0].text == "Sciences"

    def test_on_keyboard_keydown_2(self):
        """ test touche droite qui fait comme entrée
        et focus sur nouvel catégorie, 
        touche traité renvoie True
        et rien de trouver renvoi false"""
        EventLoop.ensure_window()
        window = EventLoop.window
        base = Widget()
        window.add_widget(base)
        m = MatiereDropdown(tree=MATIERES_TREE, attach_to=base)
        assert m.keyboard_on_key_down("window", (275, ""), "omk", "modifier")
        d2 = window.children[0]
        assert d2.options[-1].text == "Orthographe"

        # test pas de touche identifié
        assert not m.keyboard_on_key_down("window", (2000, ""), "omk", "modifier")


class TestMatiereOption(MyDevoirsTestCase):
    def test_init(self):
        a = MatiereOption()
        assert not a.has_sub
        a = MatiereOption(has_sub=True)
        assert a.has_sub

    def test_on_release(self):
        w = DropDown()
        w.on_select = MagicMock()
        a = MatiereOption(dropdown=w)
        a.trigger_action(0)

        assert w.on_select.called
        assert w.on_select.call_args == call(a)

    def test_toggle_focus(self):
        a = MatiereOption()
        assert a.bold == False
        a.toggle_focus()
        assert a.bold == True
        a.toggle_focus()
        assert a.bold == False
