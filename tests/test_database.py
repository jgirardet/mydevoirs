import datetime
import tempfile
from pathlib import Path

import pytest
from pony.orm import Database, db_session, select

from mydevoirs.database import (
    db,
    ensure_database_directory,
    init_bind,
    init_database,
    init_update_matiere,
)

from .fixtures import f_item


def test_init_update_matiere( matieres_config):
    """ in tests init_update_matiere already run
    so we check the result first"""
    MATIERES = matieres_config
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


def test_init_bind_memory():
    ddb = Database()
    init_bind(ddb)


def test_init_bind_file_exists(tmpfile):
    ddb = Database()
    init_bind(ddb, filename=tmpfile)


def test_init_bind_file_exists_with_string(tmpfile):
    ddb = Database()
    init_bind(ddb, filename=str(tmpfile))


def test_init_bind_file_no_exists_no_createdb(tmpfilename):
    ddb = Database()
    with pytest.raises(OSError):
        init_bind(ddb, filename=tmpfilename)


def test_init_bind_file_not_exists_create_db(tmpfilename):
    ddb = Database()
    init_bind(ddb, filename=tmpfilename, create_db=True)


def test_init_bind_file_and_parent_dir_does_not_exists(tmp_path):
    ddb = Database()
    file = tmp_path / "some" / "sub" / "sub" / "dir" / "some_file"
    init_bind(ddb, filename=file, create_db=True)


def test_init_database(tmpfilename, matieres_config):
    d = init_database(matieres_config, filename=tmpfilename, create_db=True)
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
