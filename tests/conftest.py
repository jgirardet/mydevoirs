from mydevoirs.__main__ import configure_env

configure_env()

import pytest
from kivy.lang import Builder
from kivy.logger import LOG_LEVELS, Logger
from mimesis import Generic

import mydevoirs.database
from mydevoirs.database import init_database
from mydevoirs.main import setup_kivy

generic_mimesis = Generic("fr")


@pytest.fixture(scope="function")
def gen(request):
    return generic_mimesis


def pytest_configure(config):
    Logger.setLevel(LOG_LEVELS["error"])


def pytest_sessionstart():
    setup_kivy()
    mydevoirs.database.db = init_database()
    Builder.load_file("mydevoirs/mydevoirs.kv")


@pytest.fixture(scope="function")
def tmpfile(request, tmp_path, gen):
    """tempfile which exists"""
    file = tmp_path / gen.file.file_name()
    file.touch()
    return file


@pytest.fixture(scope="function")
def tmpfilename(request, tmp_path, gen):
    """tempfile which does not exists"""
    return tmp_path / gen.file.file_name()
