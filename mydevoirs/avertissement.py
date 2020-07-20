# from kivy.app
from kivy.app import App
from kivy.uix.widget import Widget

from mydevoirs.ouinonpopup import OuiNonPopup


class BackupAncienneDB(Widget):
    def __init__(self, old_path, backup_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_path = old_path
        self.backup_path = backup_path
        self.app = App.get_running_app()
        self.popup = OuiNonPopup(
            title=f"""Cette de version MyDevoirs n'est pas
compatible avec la version de la base de donnée actuelle.
Si vous continuez, l'actuelle base de donnée sera sauvegardée vers
{backup_path}.
Ces données ne serons alors accessible qu'avec  l'ancienne version de MyDevoirs.
Cliquez sur OUI pour accepter, NON pour quitter
""",
            size_hint=(0.6, 0.5),
            on_oui=self.replace_db,
            on_non=self.app.stop,
        )

        self.popup.open()

    def replace_db(self, *args):
        self.old_path.replace(self.backup_path)
        self.app.config.write()
        self.app._reload_app()
