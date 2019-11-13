import appdirs
from pathlib import Path
from mydevoirs.constants import APP_NAME, MATIERES
import os


def get_dir(key):

    # test config dir
    dire = Path(getattr(appdirs, "user_" + key + "_dir")(), APP_NAME)
    if not dire.is_dir():
        dire.mkdir(parents=True)
    return dire

def get_matiere_color(nom):
    try:
        
        return MATIERES[nom]
    except KeyError:
        return (0,0,0)