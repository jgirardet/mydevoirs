from mydevoirs.database.database import db_init, db
from pony.orm import  db_session, select
from mydevoirs.constants import MATIERES

def test_dbinit():
    """ in tests db_init already run
    so we check the result first"""
    print(MATIERES.keys())
    with db_session:
        keys = set(select(b.nom for b in db.Matiere))
    assert set(MATIERES) == keys

    MATIERES["Nouvelle"] = (91, 193, 242)

    db_init(matieres=MATIERES)
    with db_session:
        keys = set(select(b.nom for b in db.Matiere))
    assert set(MATIERES) == keys

    #teardown
    with db_session:
        db.Matiere['Nouvelle'].delete()
    MATIERES.pop('Nouvelle')
