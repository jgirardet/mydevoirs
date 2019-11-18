import pony.orm.dbproviders.sqlite  # noqa: W291
import os


from pony.orm import Required, PrimaryKey, Set, Optional, db_session, min, select, count
from pony.orm.ormtypes import IntArray, FloatArray
import datetime
from mydevoirs.constants import MATIERES
from mydevoirs.utils import get_dir

from .base_db import db, GetOrCreateMixin


class Jour(db.Entity, GetOrCreateMixin):
    date = PrimaryKey(datetime.date)
    items = Set("Item")

    @classmethod
    def oldest(cls):
        return min(i.date for i in cls)

    @property
    def progression(self):
        return count(x for x in self.items if x.done), len(self.items)
        # return len(dones)


class Matiere(db.Entity):
    nom = PrimaryKey(str)
    color = Required(FloatArray)
    items = Set("Item")


class Item(db.Entity):
    id = PrimaryKey(int, auto=True)
    matiere = Required(Matiere, default="Grammaire")
    jour = Required(Jour)
    content = Optional(str)
    done = Required(bool, default=False)

    def toggle(self):
        self.done = not self.done

    @classmethod
    def todo_list(self):
        return Item.select(
            lambda x: x.jour.date >= datetime.date.today() and not x.done
        ).order_by(lambda x: x.jour)

    def to_dict(self):
        dico = super().to_dict()
        dico.pop("matiere")
        dico["matiere_nom"] = self.matiere.nom
        dico["matiere_color"] = self.matiere.color
        dico["date"] = self.jour.date
        return dico

    def __repr__(self):
        return f"Item {self.id} => {self.matiere.nom} :\
         {self.content} {'ø' if self.done else 'o'}"


@db.on_connect(provider="sqlite")
def sqlite_synchonous_off(db, connection):
    cursor = connection.cursor()
    cursor.execute("PRAGMA synchronous = OFF")


###################################################################
############## DATABASE SETUP #####################################
###################################################################


if os.environ.get("MYDEVOIRS_TESTING", False):
    db.bind(provider="sqlite", filename=":memory:")
else:

    light_db = get_dir("cache") / "ddb.sqlite"
    hard_db = get_dir("cache") / "ddb_hard.sqlite"
    db.bind(provider="sqlite", filename=str(hard_db.absolute()), create_db=True)
db.generate_mapping(create_tables=True)


def db_init():
    with db_session():
        for k, v in MATIERES.items():
            if db.Matiere.exists(nom=k):
                if db.Matiere[k].color != v:
                    db.Matiere[k].color = v

            else:
                db.Matiere(nom=k, color=v)
