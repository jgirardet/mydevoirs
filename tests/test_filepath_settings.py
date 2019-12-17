from mydevoirs.filepath_setting import *


from pathlib import Path


from .fixtures import *
import tempfile

from kivy.uix.settings import SettingsPanel


class TestSettingFilePath(MyDevoirsTestCase):
    def setUp(self):
        super().setUp()
        # super().setUp(no_db=True)
        panel = SettingsPanel()
        self.fp = SettingFilePath(panel=panel)
        self.t = tempfile.NamedTemporaryFile()
        self.bla = tempfile.NamedTemporaryFile()

    def tearDown(self):
        super().tearDown()
        self.t.close()
        self.bla.close()
        self.window.clear()

    def boiler_plate(self, value=None, filename=None):
        value = value if value else self.t.name
        filename = filename if filename else self.t.name
        self.fp.value = value
        self.fp._create_popup(self.fp)
        self.fp.textinput.filename = filename

    def test_old_eq_new(self):
        self.boiler_plate()
        fp_popup = self.fp.popup
        self.fp.textinput.dispatch("on_success")
        assert self.window.children[0] == fp_popup
        assert self.fp.new_value == self.t.name

    def test_new_is_empty(self):
        self.boiler_plate()
        self.fp.textinput.filename = ""
        fp_popup = self.fp.popup
        self.fp.textinput.dispatch("on_success")
        assert self.window.children[0] == fp_popup
        assert self.fp.value == self.t.name
        del fp_popup

    def test_nouveau_nom_pas_copier(self):
        self.boiler_plate(value=self.bla.name)
        self.fp.textinput.dispatch("on_success")
        self.popup_click("non")
        assert self.fp.value == self.t.name

    def test_nouveau_nom_copier(self):

        self.boiler_plate(value=self.bla.name, filename="/some/improbable/name")
        self.fp.textinput.dispatch("on_success")
        self.popup_click("oui")
        assert self.fp.value == "/some/improbable/name"

    def test_nouveau_nom_copier_fichier_existe_ecrase(self):
        with tempfile.NamedTemporaryFile(delete=False) as old:
            old.close()
            Path(old.name).write_bytes(b"coucou")
            self.boiler_plate(value=old.name)
            self.fp.textinput.dispatch("on_success")
            self.popup_click("oui")  # copier le contenu
            self.popup_click("oui")  # ecraser fichier
            assert self.fp.value == self.t.name
            assert Path(self.t.name).read_bytes() == b"coucou"

    def test_nouveau_nom_copier_fichier_existe_pas_ecraser(self):
        self.boiler_plate(value=self.bla.name)
        self.fp.textinput.dispatch("on_success")
        self.popup_click("oui")  # copier le contenu
        self.popup_click("non")  # ecraser fichier
        assert self.fp.value == self.bla.name

    def test_dispatch_submit(self):
        self.boiler_plate(value=self.bla.name)
        self.fp.textinput.dispatch("on_submit")
        self.popup_click("non")
        assert self.fp.value == self.t.name

    def test_dispatch_canceled(self):
        self.boiler_plate(value=self.bla.name)
        self.fp.textinput.dispatch("on_canceled")
        assert self.fp.value == self.bla.name

    def test_input_property(self):
        self.boiler_plate()
        assert self.fp.textinput.path == self.t.name
        assert not self.fp.textinput.dirselect
        assert self.fp.textinput.show_hidden
