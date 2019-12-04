from pony.orm import Database, db_session

from mydevoirs.constants import MATIERES

db = Database()


class GetOrCreateMixin:
    @classmethod
    def get_or_create(cls, **kwargs):
        if not cls.exists(**kwargs):
            res = cls(**kwargs)
            db.flush()
        else:
            res = cls.get(**kwargs)
        return res


def init_update_matiere(matieres=MATIERES):
    with db_session():
        for k, v in matieres.items():
            if db.Matiere.exists(nom=k):
                db.Matiere[k].color = v

            else:
                db.Matiere(nom=k, color=v)


def init_bind(provider="sqlite", filename=":memory:", create_db=False, **kwargs):
    db.bind(provider=provider, filename=filename, create_db=create_db)
    db.generate_mapping(create_tables=True)


def init_import_models():

    from .models import Jour, Matiere, Item  # flake8: noqa


def init_database(**kwargs):
    init_import_models()
    init_bind(**kwargs)
    init_update_matiere()
