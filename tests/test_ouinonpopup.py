from unittest.mock import MagicMock

from mydevoirs.ouinonpopup import OuiNonPopup

from .fixtures import *


class TestOuiNonPopup(MyDevoirsTestCase):
    def test_show(self):
        a = OuiNonPopup()
        assert self.window.children[0] == a

    def test_show_no_autopen(self):
        a = OuiNonPopup(auto_open=False)
        assert not self.window.children

    def test_click_oui(self):
        self.some_var = 0

        def plus(*args):
            self.some_var += 1

        a = OuiNonPopup(on_oui=plus)
        a.on_dismiss = MagicMock()
        self.popup_click("oui")
        assert self.some_var == 1
        assert a.on_dismiss.called

    def test_click_oui(self):
        self.some_var = 0

        def plus(*args):
            self.some_var += 1

        a = OuiNonPopup(on_oui=plus)
        a.on_dismiss = MagicMock()
        self.popup_click("oui")
        assert self.some_var == 1
        assert a.on_dismiss.called

    def test_press_oui(self):
        self.some_var = 0

        def plus(*args):
            self.some_var += 1

        a = OuiNonPopup(on_oui=plus)
        a.on_dismiss = MagicMock()
        self.press_key("enter")
        assert self.some_var == 1
        assert a.on_dismiss.called

    def test_click_non(self):
        self.some_var = 0

        def plus(*args):
            self.some_var += 1

        a = OuiNonPopup(on_oui=plus)
        a.on_dismiss = MagicMock()
        self.popup_click("non")
        assert self.some_var == 0
        assert a.on_dismiss.called

    def test_press_non(self):
        self.some_var = 0

        def plus(*args):
            self.some_var += 1

        a = OuiNonPopup(on_oui=plus)
        a.on_dismiss = MagicMock()
        self.press_key("left")
        self.press_key("enter")
        assert self.some_var == 0
        assert a.on_dismiss.called

    def test_toggle(self):
        a = OuiNonPopup()
        assert a.content.ids.oui.state == "down"
        assert a.content.ids.non.state == "normal"

        self.press_key("left")
        assert a.content.ids.oui.state == "normal"
        assert a.content.ids.non.state == "down"

        self.press_key("right")
        assert a.content.ids.oui.state == "down"
        assert a.content.ids.non.state == "normal"

    def test_not_consume_key(self):
        a = OuiNonPopup()
        assert not a.content.keyboard_on_key_down("window", (123, "up"), "omk", "okm")
