from pony.orm import Database, db_session

from mydevoirs.constants import MATIERES
from pathlib import Path
from .models import init_models


def init_update_matiere(db, matieres=MATIERES):
    with db_session():
        for k, v in matieres.items():
            if db.Matiere.exists(nom=k):
                db.Matiere[k].color = v

            else:
                db.Matiere(nom=k, color=v)


def ensure_database_directory(loc):

    if not loc.parent.exists():
        loc.parent.mkdir(parents=True)


def init_bind(db, provider="sqlite", filename=":memory:", create_db=False, **kwargs):
    if filename != ":memory:":
        filename = Path(filename)
        ensure_database_directory(filename)
    db.bind(provider=provider, filename=str(filename), create_db=create_db)
    db.generate_mapping(create_tables=True)


def init_database(**kwargs):
    ddb = Database()
    init_models(ddb)
    init_bind(ddb, **kwargs)
    init_update_matiere(ddb)
    return ddb
