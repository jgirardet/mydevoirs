from pathlib import Path
from importlib.metadata import metadata

APP_NAME = "MyDevoirs"
DDB_FILENAME = "ddb_hard.sqlite"
BASE_DIR = Path(__file__).parent


VERSION = metadata("mydevoirs")["version"]


SEMAINE = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


MATIERES_TREE_INIT = [
    ("Orthographe", (91 / 255, 193 / 255, 242 / 255)),
    ("Grammaire", (153 / 255, 200 / 255, 245 / 255)),
    ("Conjugaison", (34 / 255, 174 / 255, 241 / 255)),
    ("Vocabulaire", (2 / 255, 162 / 255, 240 / 255)),
    ("Rédaction", (0 / 255, 120 / 255, 255 / 255)),
    ("Mathématiques", (216 / 255, 88 / 255, 243 / 255)),
    ("Géométrie", (229 / 255, 151 / 255, 246 / 255)),
    ("Histoire", (227 / 255, 254 / 255, 0 / 255)),
    ("Géographie", (236 / 255, 254 / 255, 87 / 255)),
    ("Musique", (142 / 255, 108 / 255, 252 / 255)),
    ("Poésie", (186 / 255, 165 / 255, 252 / 255)),
    ("Sciences", (255 / 255, 177 / 255, 88 / 255)),
    ("Anglais", (255 / 255, 90 / 255, 90 / 255)),
    ("Divers", (89 / 255, 253 / 255, 89 / 255)),
]


THEMES = {
    "standard": {
        "fond": [130 / 255, 134 / 255, 138 / 255, 1],
        "card": [98 / 255, 105 / 255, 114 / 236, 1],
        "card_entete": [83 / 255, 93 / 255, 105 / 236, 1],
        "card_texte_entete": [0, 0, 0, 1],
        "card_texte_size": "16sp",
        "titre_jour": [0.2, 0.4, 0, 1],
        "progression": [0.92, 0.008, 0.008, 1],
        "spinner_text_color": [0, 0, 0, 1],
        "police": str(BASE_DIR / "data" / "fonts" / "Verdana.ttf")
    },
    "standard-dys": {
        "fond": [130 / 255, 134 / 255, 138 / 255, 1],
        "card": [98 / 255, 105 / 255, 114 / 236, 1],
        "card_entete": [83 / 255, 93 / 255, 105 / 236, 1],
        "card_texte_entete": [0, 0, 0, 1],
        "card_texte_size": "16sp",
        "titre_jour": [0.2, 0.4, 0, 1],
        "progression": [0.92, 0.008, 0.008, 1],
        "spinner_text_color": [0, 0, 0, 1],
        "police": str(BASE_DIR / "data" / "fonts" / "OpenDyslexic-Regular.ttf")
    },    
    "contrast": {
        "fond": [130 / 255, 134 / 255, 138 / 255, 1],
        "card": [98 / 255, 105 / 255, 114 / 236, 1],
        "card_texte_entete": [1, 1, 1, 1],
        "card_entete": [0, 0, 0, 1],
        "card_texte_size": "18sp",
        "titre_jour": [0.2, 0.4, 0, 1],
        "progression": [1, 1, 1, 1],
        "spinner_text_color": [0, 0, 0, 1],
        "police": str(BASE_DIR / "data" / "fonts" / "Verdana.ttf")
    },
    "contrast-dys": {
        "fond": [130 / 255, 134 / 255, 138 / 255, 1],
        "card": [98 / 255, 105 / 255, 114 / 236, 1],
        "card_texte_entete": [1, 1, 1, 1],
        "card_entete": [0, 0, 0, 1],
        "card_texte_size": "18sp",
        "titre_jour": [0.2, 0.4, 0, 1],
        "progression": [1, 1, 1, 1],
        "spinner_text_color": [0, 0, 0, 1],
        "police": str(BASE_DIR / "data" / "fonts" / "OpenDyslexic-Regular.ttf")
    },
}
