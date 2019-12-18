from kivy.lang import Builder

from main import setup_start
from mydevoirs.database import init_database
import pytest
import mydevoirs.database
from mimesis import Generic

generic_mimesis = Generic("fr")

@pytest.fixture(scope='function')
def gen(request):
    return generic_mimesis

def pytest_sessionstart():
    Builder.load_file("mydevoirs/mydevoirs.kv")
    setup_start()
    mydevoirs.database.db = init_database()

@pytest.fixture(scope='function')
def tmpfile(request, tmp_path, gen):
    """tempfile which exists"""
    file = tmp_path / gen.file.file_name()
    file.touch()
    return file
    
@pytest.fixture(scope='function')
def tmpfilename(request, tmp_path, gen):
    """tempfile which does not exists"""
    return tmp_path / gen.file.file_name()
    