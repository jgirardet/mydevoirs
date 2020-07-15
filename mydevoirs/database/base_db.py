from pathlib import Path

from pony.orm import Database, db_session, flush, OperationalError

from mydevoirs.constants import MATIERES_TREE_INIT, VERSION

from .models import init_models


@db_session
def init_update_matiere(db, reset=False):
    if not db.Matiere.select().count() or reset:
        if reset:
            for it in db.Matiere.select():
                it.delete()
        flush()
        for m in MATIERES_TREE_INIT:
            db.Matiere(nom=m[0], color=m[1])


# def empty_database_initial_setup(db):
#     if


def ensure_database_directory(loc):
    loc = Path(loc)
    loc_exists = False
    if loc.is_file():
        return loc, True

    if not loc.parent.exists():
        loc.parent.mkdir(parents=True)
    return loc, False


"""
db = Database()
db.bind(**db_params)

with db_session:
    cursor = db.execute("select * from mytable")

class MyEntity(db.Entity):
    a = Required(int)

db.generate_mapping(check_tables=False)
db.drop_all_tables(with_all_data=True)
db.create_tables()"""


def get_database_version(db):
    with db_session:
        try:
            cursor = db.execute("select * from configuration").fetchone()
        except OperationalError:
            return ""
        return cursor[1] if cursor else ""


def compare_database_and_app_version(db_version):
    if db_version < VERSION:
        return "need update"
    elif db_version > VERSION:
        return "incompatible"
    return "ok"


def init_bind(db, provider="sqlite", filename=":memory:", create_db=False, **kwargs):
    if filename != ":memory:":
        filename, ddb_exists = ensure_database_directory(filename)
    db.bind(provider=provider, filename=str(filename), create_db=create_db, **kwargs)
    ddb_version = get_database_version(db)
    print("version", ddb_version)
    db.generate_mapping(create_tables=True)


def init_database(**kwargs):
    ddb = Database()
    init_models(ddb)
    init_bind(ddb, **kwargs)
    init_update_matiere(ddb)
    return ddb
