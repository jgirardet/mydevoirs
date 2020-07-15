import datetime
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from pony.orm import Database, db_session, select

from mydevoirs.constants import MATIERES_TREE_INIT, VERSION
from mydevoirs.database import (
    db,
    ensure_database_directory,
    init_bind,
    init_database,
    init_update_matiere,
)
from mydevoirs.database.base_db import (
    get_database_version,
    compare_database_and_app_version,
)

from .fixtures import f_item, f_matiere


def test_init_update_matiere():

    # creation automatique
    def check_default_matiere():
        with db_session:
            assert db.Matiere.select().count() == len(MATIERES_TREE_INIT)
            assert db.Matiere.get(nom="Orthographe").color == [
                91 / 255,
                193 / 255,
                242 / 255,
            ]

    check_default_matiere()

    # si existe on ne change rien
    init_update_matiere(db)
    with db_session:
        assert db.Matiere.select().count() == len(MATIERES_TREE_INIT)

    # si aucun refait tout :
    with db_session:
        for it in db.Matiere.select():
            it.delete()
    with db_session:
        assert db.Matiere.select().count() == 0
    init_update_matiere(db)
    check_default_matiere()

    # si reset refait tout :
    with db_session:
        db.Matiere.get(nom="Orthographe").color = [1, 2, 3, 4, 5]
        db.Matiere(nom="aaa", color=[1, 1, 1])
    init_update_matiere(db, reset=True)
    check_default_matiere()


def test_ensure_database_directory_does_not_exists():
    with tempfile.TemporaryDirectory() as t:
        file = Path(t, "rien", "nouveau", "bla", "lieu", "base.ddb")
        loc, exists = ensure_database_directory(str(file))
        assert file.parent.is_dir()
        assert loc == file
        assert not exists


def test_ensure_database_directory_file_exists():
    with tempfile.TemporaryDirectory() as t:
        file = Path(t, "base.ddb")
        file.touch()
        loc, exists = ensure_database_directory(str(file))
        assert file.parent.is_dir()
        assert exists
        assert loc == file


def test_get_database_version_table_configuration_no_exists():
    db = Database()
    db.bind(provider="sqlite", filename=":memory:")
    assert get_database_version(db) == ""


def test_get_database_version_table_configuration_no_entry(ddbr):
    assert get_database_version(ddbr) == ""


def test_get_database_version_table_configuration_no_entry(ddbr):
    assert get_database_version(ddbr) == ""


def test_get_database_version_table_configuration_entry_ok(ddbr):
    with db_session:
        ddbr.Configuration(version="2.3.4")
    assert get_database_version(ddbr) == "2.3.4"


def test_compare_database_and_app_version():
    with patch("mydevoirs.database.base_db.VERSION", "1.2.3"):
        assert compare_database_and_app_version("1.2.2") == "need update"

    with patch("mydevoirs.database.base_db.VERSION", "1.2.1"):
        assert compare_database_and_app_version("1.2.2") == "incompatible"

    with patch("mydevoirs.database.base_db.VERSION", "1.2.2"):
        assert compare_database_and_app_version("1.2.2") == "ok"


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


def test_init_database(tmpfilename):
    d = init_database(filename=tmpfilename, create_db=True)
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


class TestMatiere:
    @db_session
    def reset_matiere(self):
        for m in db.Matiere.select():
            m.delete()

    def test_ordered_ordre_empty(self):
        self.reset_matiere()
        with db_session:
            assert not db.Ordre.get(nom="Matiere")
            res1 = db.Matiere.get_ordered()
            assert res1 == []
        a = f_matiere(nom="aaa")
        b = f_matiere(nom="bbb")
        c = f_matiere(nom="ccc")

        # with ordre empty
        with db_session:
            assert db.Matiere.get_ordered() == [
                a.to_dict(),
                b.to_dict(),
                c.to_dict(),
            ]

        # with ordre not empty
        with db_session:
            db.Ordre.get(nom="Matiere").ordre = [a.id, c.id, b.id]
            assert db.Matiere.get_ordered() == [
                a.to_dict(),
                c.to_dict(),
                b.to_dict(),
            ]


class TestConfiguration:
    def test_init(self):
        with db_session:
            x = db.Configuration(version="1.2.3")
        with db_session:
            assert db.Configuration[x.id].version == "1.2.3"
