from mydevoirs.constants import build_matiere


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
