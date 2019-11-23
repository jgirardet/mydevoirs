# MATIERES = {
#     "Français": (0, 0, 1),
#     "Mathématiques": (0, 1, 0),
#     "Histoire": (1, 0, 0),
#     "Géographie": (0, 1, 1),
#     "Poésie": (1, 1, 0),
# }

APP_NAME = "MyDevoirs"


SEMAINE = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


MATIERES_TREE = {
    "Français": {
        "Orthographe": (91, 193, 242),
        "Grammaire": (153, 200, 245),
        "Conjugaison": (34, 174, 241),
        "Vocabulaire": (2, 162, 240),
        "Rédaction": (0, 120, 255),
    },
    "Mathématiques": {"Mathématiques": (216, 88, 243), "Géométrie": (229, 151, 246)},
    "Histoire-Géo": {"Histoire": (227, 254, 0), "Géographie": (236, 254, 87)},
    "Sciences": (255, 177, 88),
    "Musqiue-Poésie": {"Musique": (142, 108, 252), "Poésie": (186, 165, 252)},
    "Anglais": (255, 90, 90),
    "Divers": (89, 253, 89),
}


def build_matiere(tree):
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


MATIERES = build_matiere(MATIERES_TREE)

THEMES = {
    "vert": {
        "fond": [0.6, 0.8, 0.4, 1],
        "card": [0.2, 0.4, 0, 0.7],
        "card_entete": [0.2, 0.4, 0, 1],
        "titre_jour": [0.2, 0.4, 0, 1],
        "progression": [0.92, 0.008, 0.008, 1],
    },
    "bleu": {
        "fond": [60 / 255, 109 / 255, 248 / 236, 1],
        "card": [140 / 255, 167 / 255, 248 / 255, 1],
        "card_entete": [0.2, 0.4, 0, 1],
        "titre_jour": [0.2, 0.4, 0, 1],
        "progression": [0.92, 0.008, 0.008, 1],
    },
    "bleu_t": {
        "fond": [2 / 255, 162 / 255, 240 / 236, 0.9],
        "card": [153 / 255, 215 / 255, 245 / 255, 0.9],
        "card_entete": [34 / 255, 174 / 255, 241 / 255, 0.9],
        "titre_jour": [0.2, 0.4, 0, 1],
        "progression": [0.92, 0.008, 0.008, 1],
    },
    "bleu_g": {
        "fond": [34 / 255, 174 / 255, 241 / 255, 0.5],
        "card": [164 / 255, 164 / 255, 247 / 236, 0.5],
        "card_entete": [57 / 255, 57 / 255, 244 / 236, 0.5],
        "titre_jour": [0.2, 0.4, 0, 1],
        "progression": [0.92, 0.008, 0.008, 1],
    },
    "gris": {
        "fond": [130 / 255, 134 / 255, 138 / 255, 1],
        "card": [98 / 255, 105 / 255, 114 / 236, 1],
        "card_entete": [83 / 255, 93 / 255, 105 / 236, 1],
        "titre_jour": [0.2, 0.4, 0, 1],
        "progression": [0.92, 0.008, 0.008, 1],
        "spinner_text_color": [0, 0, 0, 1],
    },
    "vert_gris": {"fond": [0, 0.4, 0.196, 1], "card": [0, 0.6, 0.404, 1]},
}

COLORS = THEMES["gris"]
