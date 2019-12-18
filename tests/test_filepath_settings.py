from mydevoirs.filepath_setting import *


from pathlib import Path


from .fixtures import *

# import tempfile

from kivy.uix.settings import SettingsPanel
import pytest


class TestSettingFilePath(MyDevoirsTestCase):
    def setUp(self):
        super().setUp()
        panel = SettingsPanel()
        self.fp = SettingFilePath(panel=panel)

    def boiler_plate(self, old, new):
        self.fp.value = old
        self.fp._create_popup(self.fp)
        self.fp.textinput.filename = new

    def test_old_eq_new(self):
        self.boiler_plate(old = self.T.file.aname, new = self.T.aname)
        self.fp.textinput.dispatch("on_success")
        assert self.fp.new_value == self.T.filename.aname

    def test_new_is_empty(self):
        self.boiler_plate(old=self.T.file.aname, new="")
        fp_popup = self.fp.popup
        self.fp.textinput.dispatch("on_success")
        assert self.window.children[0] == fp_popup
        assert self.fp.value == self.T.file.aname
        del fp_popup

    def test_nouveau_nom_pas_copier(self):
        self.boiler_plate(old=self.T.file.aname, )
        self.fp.textinput.dispatch("on_success")
        self.popup_click("non")
        assert self.fp.value == self.t.name

    # def test_nouveau_nom_copier(self):

    #     self.boiler_plate(value=self.bla.name, filename="/some/improbable/name")
    #     self.fp.textinput.dispatch("on_success")
    #     self.popup_click("oui")
    #     assert self.fp.value == "/some/improbable/name"

    # def test_nouveau_nom_copier_fichier_existe_ecrase(self):
    #     with tempfile.NamedTemporaryFile(delete=False) as old:
    #         old.close()
    #         Path(old.name).write_bytes(b"coucou")
    #         self.boiler_plate(value=old.name)
    #         self.fp.textinput.dispatch("on_success")
    #         self.popup_click("oui")  # copier le contenu
    #         self.popup_click("oui")  # ecraser fichier
    #         assert self.fp.value == self.t.name
    #         assert Path(self.t.name).read_bytes() == b"coucou"

    # def test_nouveau_nom_copier_fichier_existe_pas_ecraser(self):
    #     self.boiler_plate(value=self.bla.name)
    #     self.fp.textinput.dispatch("on_success")
    #     self.popup_click("oui")  # copier le contenu
    #     self.popup_click("non")  # ecraser fichier
    #     assert self.fp.value == self.bla.name

    # def test_dispatch_submit(self):
    #     self.boiler_plate(value=self.bla.name)
    #     self.fp.textinput.dispatch("on_submit")
    #     self.popup_click("non")
    #     assert self.fp.value == self.t.name

    # def test_dispatch_canceled(self):
    #     self.boiler_plate(value=self.bla.name)
    #     self.fp.textinput.dispatch("on_canceled")
    #     assert self.fp.value == self.bla.name

    # def test_input_property(self):
    #     self.boiler_plate()
    #     assert self.fp.textinput.path == self.t.name
    #     assert not self.fp.textinput.dirselect
    #     assert self.fp.textinput.show_hidden
