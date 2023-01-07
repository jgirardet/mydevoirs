from pathlib import Path

from mydevoirs.constants import BASE_DIR, THEMES

# from mydevoirs.utils import build_matieres


def test_base_dir():
    assert BASE_DIR == Path(__file__).parents[1] / "mydevoirs"


def test_theme_colors():
    keys = set(THEMES["standard"].keys())
    for v in THEMES.values():
        assert keys == set(v.keys())
