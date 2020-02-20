import os
import sys
import tempfile
from pathlib import Path as PythonPath

import appdirs
from kivy.utils import rgba

from mydevoirs.constants import APP_NAME
from mydevoirs.datas import get_datas

datas = get_datas()

class Path(type(PythonPath())):
    @property
    def aname(self):
        return str(self.absolute())

_temppath=None

def get_dir(key, disable_debug=False):
    # test config dir
    global _temppath
    if DEBUG and not disable_debug:
        temppath = _temppath or Path(tempfile.TemporaryDirectory().name)
        _temppath = temppath
        dire = temppath / key /APP_NAME
    else:
        dire = Path(getattr(appdirs, "user_" + key + "_dir")(), APP_NAME)
    if not dire.is_dir():
        dire.mkdir(parents=True)
    return dire

def build_matieres(tree):
        mat = {}
        for k, v in tree.items():
            if isinstance(v, tuple):
                mat[k] = v
            else:
                # base = None
                for x, y in v.items():
                    if not mat.get(k, None):
                        mat[k] = y
                    mat[x] = y
        return mat

def get_matiere_color(nom, matiere):
    try:

        return rgba(matiere[nom])
    except KeyError:
        return rgba(0, 0, 0)



gmc = get_matiere_color