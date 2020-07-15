import datetime

import pony.orm.dbproviders.sqlite  # noqa: W291
from pony.orm import Optional, PrimaryKey, Required, Set, count, flush, select
from pony.orm.ormtypes import FloatArray, IntArray


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

    class Ordre(db.Entity, GetOrCreateMixin):
        """L'ordre n'est pas maintenu automatiquement dans la ddb"""

        nom = PrimaryKey(str)
        ordre = Required(IntArray, default=[])

    class Configuration(db.Entity):
        version = Required(str)

    class Matiere(db.Entity):
        nom = Required(str)
        color = Required(FloatArray)
        items = Set("Item")

        @classmethod
        def get_ordered(cls):
            tout = cls.select()[:]
            ordre = Ordre.get_or_create(nom="Matiere").ordre
            if ordre:
                tout_sorted = sorted(tout, key=lambda item: ordre.index(item.id))
            else:
                tout_sorted = tout
            return [x.to_dict() for x in tout_sorted]

    class Item(db.Entity):
        id = PrimaryKey(int, auto=True)
        matiere = Required(Matiere)
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
            dico["matiere_id"] = self.matiere.id
            dico["matiere_nom"] = self.matiere.nom
            dico["matiere_color"] = self.matiere.color
            dico["date"] = self.jour.date
            return dico

        def __repr__(self):
            return f"Item {self.id} => {self.matiere.nom} :\
             {self.content} {'ø' if self.done else 'o'}"
