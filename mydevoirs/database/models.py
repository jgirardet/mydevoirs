import datetime

import pony.orm.dbproviders.sqlite  # noqa: W291
from pony.orm import Optional, PrimaryKey, Required, Set, count, select, flush
from pony.orm.ormtypes import FloatArray


class GetOrCreateMixin:
    @classmethod
    def get_or_create(cls, **kwargs):
        if not cls.exists(**kwargs):
            res = cls(**kwargs)
            flush()
        else:
            res = cls.get(**kwargs)
        return res

def init_models(db):
    class Jour(db.Entity, GetOrCreateMixin):
        date = PrimaryKey(datetime.date)
        items = Set("Item")

        @property
        def progression(self):
            return count(x for x in self.items if x.done), len(self.items)

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
            return select(  # pragma: no cover_all
                x for x in Item if x.jour.date >= datetime.date.today() and not x.done
            ).order_by(Item.jour)

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
