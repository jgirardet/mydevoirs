from unittest.mock import MagicMock

from kivy.app import App
from kivy.uix.widget import Widget

from mydevoirs.avertissement import BackupAncienneDB
from .fixtures import *


class MockApp(MagicMock):
    # stop = MagicMock()
    pass


@patch("mydevoirs.avertissement.App.get_running_app", MockApp)
class TestBackupancienneDB(MyDevoirsTestCase):
    def test_init(self):
        self.check_super_init("Widget", BackupAncienneDB, "old", "new")

    def test_base(self):
        a = BackupAncienneDB("old", "new")
        assert a.old_path == "old"
        assert a.backup_path == "new"
        assert isinstance(a.app, MockApp)

    def test_popup(self):
        a = BackupAncienneDB("old", "new")
        assert a.popup in self.window.children  # == opened

    def test_popup_non(self):
        a = BackupAncienneDB("old", "new")
        a.app.stop.reset_mock()
        self.popup_click("non")
        assert a.app.stop.called == True

    def test_popup_oui(self):
        t = TempFile()
        new = t.file.parent / "new"
        a = BackupAncienneDB(t.file, new)
        a.app.stop.reset_mock()
        self.popup_click("oui")
        assert new.is_file()
        assert a.app.config.write.called
        assert a.app._reload_app.called
