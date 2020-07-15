from pathlib import Path

from pony.orm import Database, db_session, flush

from mydevoirs.constants import MATIERES_TREE_INIT

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


def ensure_database_directory(loc):
    loc = Path(loc)
    if not loc.parent.exists():
        loc.parent.mkdir(parents=True)
    return loc


def init_bind(db, provider="sqlite", filename=":memory:", create_db=False, **kwargs):
    if filename != ":memory:":
        filename = ensure_database_directory(filename)
    db.bind(provider=provider, filename=str(filename), create_db=create_db, **kwargs)
    db.generate_mapping(create_tables=True)


def init_database(**kwargs):
    ddb = Database()
    init_models(ddb)
    init_bind(ddb, **kwargs)
    init_update_matiere(ddb)
    return ddb
