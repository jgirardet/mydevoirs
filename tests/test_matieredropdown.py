from unittest.mock import MagicMock, call

from kivy.base import EventLoop
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget

from mydevoirs.itemwidget import ItemWidget
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
        m = MatiereDropdown()
        m._create_options(w, None)
        assert [p.text for p in m.children[0].children] == [p.text for p in w.children]

    def test_create(self):
        self.check_super_init("DropDown", MatiereDropdown)

        w = Widget()
        m = MatiereDropdown()
        m._create_options(w, None)

        res = [str(p) for p in w.children[::-1]]

        assert res == [
            "MatiereOption: Orthographe",
            "MatiereOption: Grammaire",
            "MatiereOption: Conjugaison",
            "MatiereOption: Vocabulaire",
            "MatiereOption: Rédaction",
            "MatiereOption: Mathématiques",
            "MatiereOption: Géométrie",
            "MatiereOption: Histoire",
            "MatiereOption: Géographie",
            "MatiereOption: Musique",
            "MatiereOption: Poésie",
            "MatiereOption: Sciences",
            "MatiereOption: Anglais",
            "MatiereOption: Divers",
        ]

    def test_focus_on_create(self):
        m = MatiereDropdown()
        # option bold == focused
        assert m.focus
        assert m.focused_index == -1
        assert m.options[-1].bold
        assert not m.options[0].bold

    def test_on_keyboard_keydown(self):
        """test haut, bas, dépassement des limites, 
        touche entrée, le tout sur le key general"""

        m = MatiereDropdown()

        # Point de départ
        assert m.focused_index == -1
        assert m.options[-1].bold

        # 1 coup en bas
        self.press_key("down")
        assert m.focused_index == -2
        assert m.options[-2].bold
        assert not m.options[-3].bold

        # puis 2 coup en bas (donc dernier)
        self.press_key(274)
        self.press_key(274)
        assert m.focused_index == -4
        assert m.options[-4].bold
        assert not all(x.bold for x in m.options[:-4])

        # puis 1 coup en bas (donc dépasse doit repasser premier)
        m.options[-4].bold = False
        m.focused_index = 0
        self.press_key(274)
        assert m.focused_index == -1
        assert m.options[-1].bold
        assert not all(x.bold for x in m.options[:-1])

        # -len donne -1
        m.options[-1].bold = False
        m.focused_index = -len(m.options)
        self.press_key(274)
        assert m.focused_index == -1

    def test_on_keyboard_keydown3(self):
        """test haut, bas, dépassement des limites,
        touche entrée, le tout sur le key general"""

        m = MatiereDropdown()
        # puis 1 coup en haut : dépasse revient en position précédente
        m.focused_index = -1
        self.press_key(273)
        assert m.focused_index == -14
        print(m.options[-14])
        for x in m.options:
            print(x.matiere_id, x.text, x.bold, m.options.index(x))
        assert m.options[-14].bold
        assert not all(x.bold for x in m.options[1:])

        # puis 2 coup en haut
        self.press_key(273)
        self.press_key(273)
        assert m.focused_index == -12
        assert m.options[-12].bold
        assert not m.options[-14].bold
        assert not m.options[-13].bold
        assert not m.options[-1].bold

        # appuyer sur entrée
        m.on_select = MagicMock()
        self.press_key(13)
        assert m.on_select.called
        assert m.on_select.call_args[0][0].text == "Sciences"

    def test_on_keyboard_keydown_2(self):
        """test touche droite qui fait comme entrée
        et focus sur nouvel catégorie, 
        touche traité renvoie True
        et rien de trouver renvoi false"""

        EventLoop.ensure_window()
        window = EventLoop.window
        base = Widget()
        base.update_matiere = lambda x: x == x
        window.add_widget(base)
        m = MatiereDropdown(attach_to=base)
        assert m.keyboard_on_key_down("window", (275, "right"), "omk", "modifier")
        assert m.options[-1].text == "Orthographe"

        # test pas de touche identifié
        assert not m.keyboard_on_key_down("window", (2000, ""), "omk", "modifier")



class TestMatiereOption(MyDevoirsTestCase):
    def test_init(self):
        a = MatiereOption()

    def test_on_release(self):
        w = DropDown()
        w.on_select = MagicMock()
        a = MatiereOption(dropdown=w)
        a.trigger_action(0)

        assert w.on_select.called
        assert w.on_select.call_args == call(a)

    def test_toggle_focus(self):
        a = MatiereOption()
        assert not a.bold
        a.toggle_focus()
        assert a.bold
        a.toggle_focus()
        assert not a.bold
