import appdirs
from pathlib import Path
from mydevoirs.constants import APP_NAME, MATIERES
import os
from kivy.utils import rgba
from mydevoirs.datas import get_datas

datas = get_datas()


def get_dir(key):

    # test config dir
    dire = Path(getattr(appdirs, "user_" + key + "_dir")(), APP_NAME)
    if not dire.is_dir():
        dire.mkdir(parents=True)
    return dire


def get_matiere_color(nom):
    try:

        return rgba(MATIERES[nom])
    except KeyError:
        return (0, 0, 0)


BASE_DIR = os.environ["MYDEVOIRS_BASE_DIR"]


def get_base_dir():
    return Path(BASE_DIR)


gmc = get_matiere_color
