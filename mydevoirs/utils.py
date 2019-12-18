import os
from pathlib import Path as PythonPath

import appdirs
from kivy.utils import rgba

from mydevoirs.constants import APP_NAME, MATIERES
from mydevoirs.datas import get_datas

datas = get_datas()

class Path(type(PythonPath())):
    @property
    def aname(self):
        return str(self.absolute())

def get_dir(key):

    # test config dir
    dire = Path(getattr(appdirs, "user_" + key + "_dir")(), APP_NAME)
    if not dire.is_dir():
        dire.mkdir(parents=True)
    return dire


def get_matiere_color(nom, matiere=MATIERES):
    try:

        return rgba(matiere[nom])
    except KeyError:
        return rgba(0, 0, 0)


gmc = get_matiere_color

BASE_DIR = os.environ["MYDEVOIRS_BASE_DIR"]


def get_base_dir():
    return Path(BASE_DIR)


