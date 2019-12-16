import datetime

from pony.orm import db_session, select

from mydevoirs.constants import MATIERES
from mydevoirs.database import (
    init_bind,
    init_database,
    init_update_matiere,
    db,
    ensure_database_directory,
)

from .fixtures import f_item
import tempfile
from pathlib import Path
from pony.orm import Database, OperationalError
import pytest


def test_init_update_matiere():
    """ in tests init_update_matiere already run
    so we check the result first"""
    print(MATIERES.keys())
    with db_session:
        keys = set(select(b.nom for b in db.Matiere))
    assert set(MATIERES) == keys

    MATIERES["Nouvelle"] = (91, 193, 242)

    init_update_matiere(db, matieres=MATIERES)
    with db_session:
        keys = set(select(b.nom for b in db.Matiere))
    assert set(MATIERES) == keys

    MATIERES["Nouvelle"] = (0, 0, 0)
    init_update_matiere(db, matieres=MATIERES)
    with db_session:
        keys = set(select(b.nom for b in db.Matiere))
    assert set(MATIERES) == keys

    # teardown
    with db_session:
        db.Matiere["Nouvelle"].delete()
    MATIERES.pop("Nouvelle")


def test_ensure_update_matiere():
    with tempfile.TemporaryDirectory() as t:
        file = Path(t, "rien", "nouveau", "bla", "lieu", "base.ddb")
        loc = ensure_database_directory(str(file))
        assert file.parent.is_dir()
        assert loc == file


def test_init_bind():
    # memorry
    ddb = Database()
    init_bind(ddb)

    # file existe:
    ddb = Database()
    with tempfile.NamedTemporaryFile() as t:
        init_bind(ddb, filename=t.name)

    # file does not exists, no create_db:
    ddb = Database()
    with tempfile.TemporaryDirectory() as t:
        with pytest.raises(OSError):
            init_bind(ddb, filename=Path(t, "mokmokmok"))

    # file exists, no create_db:
    ddb = Database()
    with tempfile.NamedTemporaryFile() as t:
        init_bind(ddb, filename=str(t.name))

    # file does not exists,  create_db:
    ddb = Database()
    with tempfile.TemporaryDirectory() as t:
        init_bind(ddb, filename=Path(t, "unexistentfile"), create_db=True)

    # file  et prents dir does not exists
    ddb = Database()
    with tempfile.TemporaryDirectory() as t:
        file = Path(t, "rien", "nouveau", "bla", "lieu", "base.ddb")
        init_bind(ddb, filename=str(file), create_db=True)


def test_init_database():
    with tempfile.TemporaryDirectory() as t:
        d = init_database(filename=Path(t, "unexistentfile"), create_db=True)
        with db_session:
            assert d.Matiere.exists(nom="Sciences")


class TestItem:
    def test_todo_list(self):
        with db_session:
            for i in range(100):
                pair = bool(i % 2)
                f_item(done=pair)

            assert (
                db.Item.todo_list()[:]
                == db.Item.select(
                    lambda x: x.jour.date >= datetime.date.today() and not x.done
                ).order_by(lambda x: x.jour)[:]
            )
