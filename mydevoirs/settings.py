import json
from importlib.metadata import metadata

from mydevoirs.constants import DDB_FILENAME
from mydevoirs.utils import get_dir

meta = metadata("mydevoirs")
homepage = meta["Home-page"]


AGENDA_PANEL = [
    {"type": "title", "title": "Aide/À propos de MyDevoirs"},
    {
        "type": "label",
        "title": f"\nDes questions ? Besoin d'aide ? Cliquez sur le lien :             ",
        "section": "aide",
        "key": "aide",
    },
    {"type": "title", "title": "Jours à afficher"},
    {
        "type": "bool",
        "title": "Afficher le lundi",
        "desc": "Afficher le lundi",
        "section": "agenda",
        "key": "lundi",
    },
    {
        "type": "bool",
        "title": "Afficher le mardi",
        "desc": "Afficher le mardi",
        "section": "agenda",
        "key": "mardi",
    },
    {
        "type": "bool",
        "title": "Afficher le mercredi",
        "desc": "Afficher le mercredi",
        "section": "agenda",
        "key": "mercredi",
    },
    {
        "type": "bool",
        "title": "Afficher le jeudi",
        "desc": "Afficher le jeudi",
        "section": "agenda",
        "key": "jeudi",
    },
    {
        "type": "bool",
        "title": "Afficher le vendredi",
        "desc": "Afficher le vendredi",
        "section": "agenda",
        "key": "vendredi",
    },
    {
        "type": "bool",
        "title": "Afficher le samedi",
        "desc": "Afficher le samedi",
        "section": "agenda",
        "key": "samedi",
    },
    {
        "type": "bool",
        "title": "Afficher le dimanche",
        "desc": "Afficher le dimanche",
        "section": "agenda",
        "key": "dimanche",
    },
    {"type": "title", "title": "Le Week-end afficher la semaine suivante"},
    {
        "type": "bool",
        "title": "Afficher la semaine suivante",
        "desc": "Affiche directement la semaine suivante le WE",
        "section": "agenda",
        "key": "auto_next_week",
    },
    {"type": "title", "title": "Choix du fichier base de donnée"},
    {
        "type": "filepath",
        "title": "chemin de la base de donné",
        "desc": "",
        "section": "ddb",
        "key": "path",
    },
]


DEFAULT_SETTINGS = {
    "agenda": {
        "lundi": 1,
        "mardi": 1,
        "mercredi": 0,
        "jeudi": 1,
        "vendredi": 1,
        "samedi": 0,
        "dimanche": 0,
        "auto_next_week": 1,
    },
    "ddb": {"path": str(get_dir("cache") / DDB_FILENAME), "file_config_path": ""},
    "aide": {"aide": homepage},
}


SETTING_PANELS = [("Agenda", json.dumps(AGENDA_PANEL))]
