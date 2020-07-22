from pathlib import Path

from mydevoirs.constants import BASE_DIR

# from mydevoirs.utils import build_matieres


def test_base_dir():
    assert BASE_DIR == Path(__file__).parents[1] / "mydevoirs"
