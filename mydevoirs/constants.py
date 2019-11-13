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
        "Grammaire": (0, 0, 1),
        "Orthographe": (0, 0, 1),
        "Conjugaison": (0, 0, 1),
        "Vocabulaire": (0, 0, 1),
        "Rédaction": (0, 0, 1),
    },
    "Mathématiques": {"Mathématiques": (0, 1, 0), "Géométrie": (0, 1, 0)},
    "Histoire-Géo": {"Histoire": (1, 0, 0), "Géographie": (1, 0, 0)},
    "Sciences": (1, 0, 1),
    "Musqiue-Poésie": {"Musique": (1, 1, 0), "Poésie": (1, 1, 0)},
    "Anglais": (200, 0, 1),
    "Divers": (200, 200, 0),
}


def build_matiere(tree):
    mat = {}
    for k, v in tree.items():
        if isinstance(v, tuple):
            mat[k] = v
        else:
            for x, y in v.items():
                mat[x] = y
    return mat


MATIERES = build_matiere(MATIERES_TREE)
