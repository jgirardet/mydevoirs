import pytest
from kivy.lang import Builder
from kivy.logger import LOG_LEVELS, Logger
from mimesis import Generic
from pony.orm import db_session, delete

import mydevoirs.database
from mydevoirs.database import init_database
from mydevoirs.main import setup_start

generic_mimesis = Generic("fr")


@pytest.fixture(scope="function")
def gen(request):
    return generic_mimesis


def pytest_configure(config):
    Logger.setLevel(LOG_LEVELS["error"])


def pytest_sessionstart():
    mydevoirs.database.db = init_database()
    Builder.load_file("mydevoirs/mydevoirs.kv")
    setup_start()


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


@pytest.fixture()
def ddbn():
    """database no reset"""
    from mydevoirs.database import db

    return db


@pytest.fixture(scope="session")
def session_ddb():
    """database no reset"""
    from mydevoirs.database import db

    return db


@pytest.fixture()
def ddbr(reset_db):
    """database reset db"""
    from mydevoirs.database import db

    return db


@pytest.fixture()
def ddb(ddbr, reset_db):
    """database reset with ddb_sesion"""
    db_session.__enter__()
    yield ddbr
    db_session.__exit__()
    # reset_db(database)


@pytest.fixture(scope="function")
def reset_db(ddbn):
    fn_reset_db(ddbn)
    yield


def fn_reset_db(db):
    with db_session:
        for entity in db.entities.values():
            delete(e for e in entity)
            db.execute(
                f"UPDATE SQLITE_SEQUENCE  SET  SEQ = 0 WHERE NAME = '{entity._table_}';"
            )
