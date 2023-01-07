import locale
import os
import platform
import sys
from configparser import MissingSectionHeaderError, NoOptionError, NoSectionError
from pathlib import Path
from typing import Optional, Tuple


from kivy.config import ConfigParser
from mydevoirs.app import MyDevoirsApp
from mydevoirs.avertissement import BackupAncienneDB


def set_locale_fr() -> None:
    if platform.system() == "Linux":
        locale.setlocale(locale.LC_ALL, "fr_FR.utf8")  # pragma: no cover_win
    else:
        locale.setlocale(locale.LC_ALL, "french")  # pragma: no cover_linux


def setup_kivy() -> bool:

    from kivy.config import Config

    Config.set("input", "mouse", "mouse,multitouch_on_demand")
    Config.set(
        "kivy", "window_icon", Path(__file__).parent / "data" / "icons" / "logo.png"
    )
    set_locale_fr()

    return True


def reapply_version(app: MyDevoirsApp) -> Tuple[int, str]:
    """
    Verifie les differents version précendentes
    :param app: L'instance en cours
    :return:
        0: le fichier n'existe pas
        1: la version a du être ajoutée
        2: la version existe == version en cours
        3: la version existe < version en cours
        4: la version existe > version en cours
    """
    cf_file = app.get_application_config()
    file = Path(cf_file)
    return_value = 0
    file_version = None
    if file.is_file():  # pragma: no branch
        config = ConfigParser()
        try:
            config.read(cf_file)
            file_version = config.get("aide", "version")
        except NoSectionError:
            return_value = 1
        except NoOptionError:
            return_value = 1
    from mydevoirs.constants import VERSION # not import constant to early because of theme 

    if file_version is not None:
        if file_version < VERSION:
            return_value = 3
        elif file_version > VERSION:
            return_value = 4
        else:
            return_value = 2

    return return_value, file_version


def get_backup_ddb_path(app: MyDevoirsApp, state: int) -> Tuple[Path, Optional[Path]]:
    path = Path(app.load_config()["ddb"]["path"])
    new_path = None
    if path.is_file() and state < 2:
        # on ne crée pas de nouvelle db  qui sera crée + tard dans load_config de app
        new_path = path.parent / "mydevoirs_sauvegarde_ancienne_version.ddb"
    return path, new_path


def main():  # pragma: no cover_all
    # covered in check_executable.py
    setup_kivy()
    app = MyDevoirsApp()
    state, file_version = reapply_version(app)
    old_path, backup_path = get_backup_ddb_path(app, state)
    if backup_path:
        app.avertissement = BackupAncienneDB(old_path, backup_path)
    else:
        app.init_database()

    app.run()
