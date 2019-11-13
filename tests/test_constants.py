from mydevoirs.constants import build_matiere


def test_buildmatiere():
    tree = {
        "Français": {
            "Grammaire": (0, 0, 1),
            "Orthographe": (0, 0, 1),
            "Conjugaison": (0, 0, 1),
            "Vocabulaire": (0, 0, 1),
            "Rédaction": (0, 0, 1),
        },
        "Mathématiques": {"Mathématiques": (0, 1, 0), "Géométrie": (0, 1, 0)},
        "Histoire-Géo-Science": {
            "Histoire": (1, 0, 0),
            "Géographie": (1, 0, 0),
            "Sciences": (1, 0, 0),
        },
        "Musqiue-Poésie": {"Musique": (1, 1, 0), "Poésie": (1, 1, 0),},
        "Anglais": (50, 50, 20),
        "Divers": (200, 200, 0),
    }

    res = {
        "Grammaire": (0, 0, 1),
        "Orthographe": (0, 0, 1),
        "Conjugaison": (0, 0, 1),
        "Vocabulaire": (0, 0, 1),
        "Rédaction": (0, 0, 1),
        "Mathématiques": (0, 1, 0),
        "Géométrie": (0, 1, 0),
        "Histoire": (1, 0, 0),
        "Géographie": (1, 0, 0),
        "Sciences": (1, 0, 0),
        "Musique": (1, 1, 0),
        "Poésie": (1, 1, 0),
        "Anglais": (50, 50, 20),
        "Divers": (200, 200, 0),
    }

    assert res == build_matiere(tree)
