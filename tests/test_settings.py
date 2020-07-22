from mydevoirs.constants import DDB_FILENAME
from mydevoirs.settings import *
from mydevoirs.utils import Path, get_dir
from scripted.check_executable import DDB

from .fixtures import *


def test_settings_item_section_exists():
    assert all(
        x["section"] in DEFAULT_SETTINGS for x in AGENDA_PANEL if x["type"] != "title"
    )


def test_each_key_has_default():
    assert all(
        x["key"] in DEFAULT_SETTINGS[x["section"]]
        for x in AGENDA_PANEL
        if x["type"] != "title"
    )


def test_each_default_has_good_type():
    for x in AGENDA_PANEL:
        if x["type"] == "title":
            continue
        elif x["type"] == "bool":
            assert isinstance(DEFAULT_SETTINGS[x["section"]][x["key"]], int)
            assert DEFAULT_SETTINGS[x["section"]][x["key"]] in (0, 1)

        elif x["type"] == "path":
            assert isinstance(DEFAULT_SETTINGS[x["section"]][x["key"]], str)

        elif x["type"] == "filepath":
            assert isinstance(DEFAULT_SETTINGS[x["section"]][x["key"]], str)

        elif x["type"] == "configfilepath":
            assert isinstance(DEFAULT_SETTINGS[x["section"]][x["key"]], str)

        elif x["type"] == "label":
            assert isinstance(DEFAULT_SETTINGS[x["section"]][x["key"]], str)

        else:
            assert False  # controle to not forget a use case


def test_ddb_path():
    assert Path(DEFAULT_SETTINGS["ddb"]["path"]) == Path(
        get_dir("cache", enable_pytest=False), DDB_FILENAME
    )
    assert str(DDB)[-26:] == str(Path(DEFAULT_SETTINGS["ddb"]["path"]))[-26:]
