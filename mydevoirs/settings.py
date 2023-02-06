import json
from importlib.metadata import metadata

from mydevoirs.constants import DDB_FILENAME, VERSION, SEMAINE, THEMES
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
    {
        "type": "options",
        "options": SEMAINE,
        "title": "Premier jour de la semaine",
        "desc": "Premier jour de la semaine",
        "section": "agenda",
        "key": "start_day",
    },
    {"type": "title", "title": "Le Week-end afficher la semaine suivante"},
    {
        "type": "bool",
        "title": "Afficher la semaine suivante",
        "desc": "Affiche directement la semaine suivante le WE",
        "section": "agenda",
        "key": "auto_next_week",
    },
    {"type": "title", "title": "Choisir le thème"},
    {
        "type": "options",
        "options": list(THEMES),
        "title": "thème",
        "desc": "",
        "section": "theme",
        "key": "theme",
    },
    {"type": "title", "title": "Choix du fichier base de données"},
    {
        "type": "filepath",
        "title": "chemin de la base de données",
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
        "start_day": "lundi",
        "auto_next_week": 1,
    },
    "theme": {"theme": "standard"},
    "ddb": {"path": str(get_dir("cache") / DDB_FILENAME), "file_config_path": ""},
    "aide": {"aide": homepage, "version": VERSION},
}


SETTING_PANELS = [("Agenda", json.dumps(AGENDA_PANEL))]
