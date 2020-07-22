from unittest.mock import MagicMock

from kivy.app import App
from kivy.uix.widget import Widget

from mydevoirs.avertissement import BackupAncienneDB
from .fixtures import *


class MockApp(App):
    pass


@patch("mydevoirs.avertissement.App.get_running_App.return_value", MockApp())
class TestBackupancienneDB(MyDevoirsTestCase):
    def test_init(self):
        self.check_super_init("Widget", BackupAncienneDB, "old", "new")

    def test_popup_base(self):
        a = BackupAncienneDB("old", "new")
        a.old_path == "old"
        a.backup_path == "new"
