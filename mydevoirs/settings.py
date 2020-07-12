import json
import sys
from pathlib import Path

from mydevoirs.constants import DDB_FILENAME
from mydevoirs.utils import get_dir

from importlib import metadata as importlib_metadata

# Find the name of the module that was used to start the app
# app_module = sys.modules["__main__"].__package__
# app_module = sys.modules["__main__"].__package__
# Retrieve the app's metadata
metadata = importlib_metadata.metadata("mydevoirs")
homepage = metadata["Home-page"]


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
    {"type": "title", "title": "Choix du fichier base de donnée"},
    {
        "type": "filepath",
        "title": "chemin de la base de donné",
        "desc": "",
        "section": "ddb",
        "key": "path",
    },
    {"type": "title", "title": "Importer un fichier de configuration"},
    {
        "type": "configfilepath",
        "title": "chemin du fichier",
        "desc": "",
        "section": "ddb",
        "key": "file_config_path",
    },
    # {
    #     "type": "numeric",
    #     "title": "Nombre de jour à afficher",
    #     "desc": "Nombre de jour à afficher",
    #     "section": "agenda",
    #     "key": "nbjour",
    # },
    # {
    #     "type": "buttons",
    #     "title": "essai bout",
    #     # "title": "$lvar(565)",
    #     "desc": "la desc",
    #     # "desc": "$lvar(566)",
    #     # "section": "$var(InterfaceConfigSection)",
    #     "section": "agenda",
    #     "key": "configchangebuttons",
    #     "buttons": [
    #         {"title": "Add", "id": "button_add"},
    #         {"title": "Del", "id": "button_delete"},
    #         {"title": "Rename", "id": "button_rename"},
    #     ],
    # },
    # {
    #     "type": "slider",
    #     "title": "essai bout",
    #     "desc": "la desc",
    #     "section": "agenda",
    #     "key": "slider1",
    # }
    # {
    #     "type": "options",
    #     "title": "An options setting",
    #     "desc": "Options description text",
    #     "section": "example",
    #     "key": "optionsexample",
    #     "options": ["option1", "option2", "option3"],
    # },
]


import mydevoirs.utils

DEFAULT_SETTINGS = {
    "agenda": {
        "lundi": 1,
        "mardi": 1,
        "mercredi": 0,
        "jeudi": 1,
        "vendredi": 1,
        "samedi": 0,
        "dimanche": 0,
    },
    "ddb": {"path": str(get_dir("cache") / DDB_FILENAME), "file_config_path": ""},
    "aide": {"aide": homepage},
}


SETTING_PANELS = [("Agenda", json.dumps(AGENDA_PANEL))]
