from pathlib import Path

from mydevoirs.constants import BASE_DIR, VERSION, APP_NAME
import toml

# from mydevoirs.utils import build_matieres


def test_base_dir():
    assert BASE_DIR == Path(__file__).parents[1] / "mydevoirs"


def test_VERSION():
    pp = toml.load(Path(__file__).parents[1] / "pyproject.toml")
    assert VERSION == pp["tool"]["briefcase"]["version"]
