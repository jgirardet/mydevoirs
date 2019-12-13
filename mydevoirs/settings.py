import json
from mydevoirs.utils import get_dir
from mydevoirs.constants import DDB_FILENAME
from pathlib import Path

AGENDA_PANEL = [
{
        "type": "title",
        "title": "Jours à afficher"
    },
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
        "type": "title",
        "title": "Choix du fichier base de donnée"
    },
    {
        "type": "path",
        "title": "chemin de la base de donné",
        "desc": "",
        "section": "ddb",
        "key": "path",
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
    # {
    #     "type": "string",
    #     "title": "A string setting",
    #     "desc": "String description text",
    #     "section": "example",
    #     "key": "stringexample",
    # },
]


DEFAULT_SETTINGS = {
    "agenda": {
        "lundi": True,
        "mardi": True,
        "mercredi": False,
        "jeudi": True,
        "vendredi": True,
        "samedi": False,
        "dimanche": False,
    },
    "ddb": {
    "path": str(Path(get_dir("cache"), DDB_FILENAME))
    }
}



SETTING_PANELS = [("Agenda", json.dumps(AGENDA_PANEL))]
