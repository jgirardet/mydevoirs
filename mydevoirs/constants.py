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
print(MATIERES)

THEMES = {
    "vert": {
        "fond": [0.6, 0.8, 0.4, 1],
        "card": [0.2, 0.4, 0, 0.7],
        "card_entete": [0.2, 0.4, 0, 1],
        "titre_jour": [0.2, 0.4, 0, 1],
        "progression": [0.92,0.008,0.008,1]

    },
    "vert_gris": {"fond": [0, 0.4, 0.196, 1], "card": [0, 0.6, 0.404, 1]},
}

COLORS = THEMES["vert"]
