from mydevoirs.settings import *

from .fixtures import *


def test_settings_item_section_exists():
    assert all(x["section"] in DEFAULT_SETTINGS for x in AGENDA_PANEL)


def test_each_key_has_default():
    assert all(x["key"] in DEFAULT_SETTINGS[x["section"]] for x in AGENDA_PANEL)


def test_each_default_has_good_type():
    # type(DEFAULT_SETTINGS[x["section"]][x["key"]]) for x in AGENDA_PANEL
    for x in AGENDA_PANEL:
        if x["type"] == "bool":
            assert isinstance(DEFAULT_SETTINGS[x["section"]][x["key"]], bool)

        else:
            assert False  # controle to not forget a use case
