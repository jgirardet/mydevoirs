from unittest.mock import call, patch

from kivy.uix.settings import SettingsPanel

from mydevoirs.custom_setting import *

from .fixtures import *


class TestSettingFilePath(MyDevoirsTestCase):
    def setUp(self):
        super().setUp()
        panel = SettingsPanel()
        self.fp = SettingFilePath(panel=panel)
        self.fp.value = self.T.file.aname
        self.fp._create_popup(self.fp)
        self.fp.textinput.filename = self.T.filename.aname

    def test_old_eq_new(self):
        self.fp.textinput.filename = self.T.file.aname
        self.fp.textinput.dispatch("on_success")
        assert self.fp.new_value == self.T.file.aname

    def test_new_is_empty(self):
        self.fp.textinput.filename = ""
        fp_popup = self.fp.popup
        self.fp.textinput.dispatch("on_success")
        assert self.window.children[0] == fp_popup
        assert self.fp.value == self.T.file.aname
        del fp_popup

    def test_nouveau_nom_pas_copier(self):
        self.fp.textinput.dispatch("on_success")
        self.popup_click("non")
        assert self.fp.value == self.T.filename.aname

    def test_nouveau_nom_copier_non_existe(self):

        self.T.file.write_bytes(b"blabla")
        self.fp.textinput.dispatch("on_success")
        self.popup_click("oui")
        assert self.fp.value == self.T.filename.aname
        assert self.T.filename.exists()
        assert self.T.file.read_bytes() == self.T.filename.read_bytes()

    def test_nouveau_nom_copier_fichier_existe_ecrase(self):

        self.T.file.write_bytes(b"contenu de old")
        self.T.filename.write_bytes(b"coucou")
        self.fp.textinput.dispatch("on_success")
        self.popup_click("oui")  # copier le contenu
        self.popup_click("oui")  # ecraser fichier
        assert self.fp.value == self.T.filename.aname
        assert self.T.file.read_bytes() == self.T.filename.read_bytes()

    def test_nouveau_nom_copier_fichier_existe_pas_ecraser(self):
        self.T.file.write_bytes(b"contenu de old")
        self.T.filename.write_bytes(b"coucou")
        self.fp.textinput.dispatch("on_success")
        self.popup_click("oui")  # copier le contenu
        self.popup_click("non")  # ecraser fichier
        assert self.fp.value == self.T.file.aname
        assert self.T.filename.read_bytes() == b"coucou"

    def test_dispatch_submit(self):
        self.fp.textinput.dispatch("on_submit")
        self.popup_click("non")
        assert self.fp.value == self.T.filename.aname

    def test_dispatch_canceled(self):
        self.fp.textinput.dispatch("on_canceled")
        assert self.fp.value == self.T.file.aname

    def test_input_property(self):
        assert self.fp.textinput.path == self.T.file.aname
        assert not self.fp.textinput.dirselect
        assert self.fp.textinput.show_hidden


class TestSettingCustomConfigFilePath(MyDevoirsTestCase):
    def setUp(self):
        super().setUp()
        panel = SettingsPanel()
        self.fp = SettingCustomConfigFilePath(panel=panel)
        self.fp.value = self.T.file.aname
        self.fp._create_popup(self.fp)
        self.fp.textinput.filename = self.T.filename.aname

    def test_old_eq_new(self):
        self.fp.textinput.filename = self.T.file.aname
        self.fp.textinput.dispatch("on_success")
        assert self.fp.new_value == self.T.file.aname

    def test_new_is_empty(self):
        self.fp.textinput.filename = ""
        fp_popup = self.fp.popup
        self.fp.textinput.dispatch("on_success")
        assert self.window.children[0] == fp_popup
        assert self.fp.value == self.T.file.aname
        del fp_popup

    #
    def test_ne_rien_changeer(self):
        self.fp.textinput.dispatch("on_canceled")
        self.popup_click("non")
        # assert self.fp.value == ""
        assert self.fp.value == self.T.file.aname

    def test_effacer_fichier_config(self):
        self.fp.textinput.dispatch("on_canceled")
        self.popup_click("oui")
        assert self.fp.value == ""

    def test_set_new_file(self):

        self.T.file.write_bytes(b"blabla")
        self.fp.textinput.dispatch("on_success")
        self.popup_click("oui")
        assert self.fp.value == self.T.filename.aname

    #
    # def test_nouveau_nom_copier_fichier_existe_ecrase(self):
    #
    #     self.T.file.write_bytes(b"contenu de old")
    #     self.T.filename.write_bytes(b"coucou")
    #     self.fp.textinput.dispatch("on_success")
    #     self.popup_click("oui")  # copier le contenu
    #     self.popup_click("oui")  # ecraser fichier
    #     assert self.fp.value == self.T.filename.aname
    #     assert self.T.file.read_bytes() == self.T.filename.read_bytes()
    #
    # def test_nouveau_nom_copier_fichier_existe_pas_ecraser(self):
    #     self.T.file.write_bytes(b"contenu de old")
    #     self.T.filename.write_bytes(b"coucou")
    #     self.fp.textinput.dispatch("on_success")
    #     self.popup_click("oui")  # copier le contenu
    #     self.popup_click("non")  # ecraser fichier
    #     assert self.fp.value == self.T.file.aname
    #     assert self.T.filename.read_bytes() == b"coucou"
    #
    # def test_dispatch_submit(self):
    #     self.fp.textinput.dispatch("on_submit")
    #     self.popup_click("non")
    #     assert self.fp.value == self.T.filename.aname
    #
    # def test_dispatch_canceled(self):
    #     self.fp.textinput.dispatch("on_canceled")
    #     assert self.fp.value == self.T.file.aname
    #
    # def test_input_property(self):
    #     assert self.fp.textinput.path == self.T.file.aname
    #     assert not self.fp.textinput.dirselect
    #     assert self.fp.textinput.show_hidden


class TestSettingLabel(MyDevoirsTestCase):
    def test_base(self):
        panel = SettingsPanel()
        self.fp = SettingLabel(panel=panel)
        self.fp.value = "some url"
        with patch("mydevoirs.custom_setting.webbrowser.open_new") as m:
            self.fp.dispatch("on_release")
            assert m.called
            assert m.call_args_list == [call("some url")]
