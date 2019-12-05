from mydevoirs.constants import build_matiere, APP_NAME
from mydevoirs.utils import get_dir
from main import DDB_NAME, get_database_location, DDB_NAME
from main import APPNAME as MAIN_APPNAME
from scripted.check_executable import DDB
from pathlib import Path


def test_buildmatiere():
    tree = {
        "Français": {
            "Grammaire": (0, 0, 255),
            "Orthographe": (0, 0, 255),
            "Conjugaison": (0, 0, 255),
            "Vocabulaire": (0, 0, 255),
            "Rédaction": (0, 0, 255),
        },
        "Mathématiques": {"Mathématiques": (0, 255, 0), "Géométrie": (0, 255, 0)},
        "Histoire-Géo": {"Histoire": (255, 0, 0), "Géographie": (255, 0, 0)},
        "Sciences": (255, 0, 255),
        "Musqiue-Poésie": {"Musique": (255, 255, 0), "Poésie": (255, 255, 0)},
        "Anglais": (255, 120, 0),
        "Divers": (232, 120, 221),
    }

    res = {
        "Français": (0, 0, 255),
        "Grammaire": (0, 0, 255),
        "Orthographe": (0, 0, 255),
        "Conjugaison": (0, 0, 255),
        "Vocabulaire": (0, 0, 255),
        "Rédaction": (0, 0, 255),
        "Mathématiques": (0, 255, 0),
        "Géométrie": (0, 255, 0),
        "Histoire-Géo": (255, 0, 0),
        "Histoire": (255, 0, 0),
        "Géographie": (255, 0, 0),
        "Sciences": (255, 0, 255),
        "Musqiue-Poésie": (255, 255, 0),
        "Musique": (255, 255, 0),
        "Poésie": (255, 255, 0),
        "Anglais": (255, 120, 0),
        "Divers": (232, 120, 221),
    }

    assert res == build_matiere(tree)


def test_appname():
    assert APP_NAME == MAIN_APPNAME


def test_ddb_path():
    assert DDB == get_database_location() == Path(get_dir("cache"), DDB_NAME)
