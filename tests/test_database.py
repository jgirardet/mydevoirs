import datetime

from pony.orm import db_session, select

from mydevoirs.constants import MATIERES
from mydevoirs.database import (
    init_bind,
    init_database,
    init_update_matiere,
    db
)

from .fixtures import f_item


def test_init_update_matiere():
    """ in tests init_update_matiere already run
    so we check the result first"""
    print(MATIERES.keys())
    with db_session:
        keys = set(select(b.nom for b in db.Matiere))
    assert set(MATIERES) == keys

    MATIERES["Nouvelle"] = (91, 193, 242)

    init_update_matiere(db,matieres=MATIERES)
    with db_session:
        keys = set(select(b.nom for b in db.Matiere))
    assert set(MATIERES) == keys

    MATIERES["Nouvelle"] = (0, 0, 0)
    init_update_matiere(db,matieres=MATIERES)
    with db_session:
        keys = set(select(b.nom for b in db.Matiere))
    assert set(MATIERES) == keys

    # teardown
    with db_session:
        db.Matiere["Nouvelle"].delete()
    MATIERES.pop("Nouvelle")


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
