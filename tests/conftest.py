import pytest
from kivy.lang import Builder
from kivy.logger import LOG_LEVELS, Logger
from mimesis import Generic

import mydevoirs.database
from main import setup_start
from mydevoirs.database import init_database
from mydevoirs.constants import MATIERES_TREE
from mydevoirs.utils import  build_matieres

generic_mimesis = Generic("fr")

@pytest.fixture()
def matieres_config():
    build_matieres(MATIERES_TREE)

@pytest.fixture(scope="function")
def gen(request):
    return generic_mimesis


def pytest_configure(config):
    Logger.setLevel(LOG_LEVELS["error"])


def pytest_sessionstart():
    Builder.load_file("mydevoirs/mydevoirs.kv")
    setup_start()
    mydevoirs.database.db = init_database(build_matieres(MATIERES_TREE))


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
