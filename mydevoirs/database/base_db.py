from pony import orm

db = orm.Database()


class GetOrCreateMixin:
    @classmethod
    def get_or_create(cls, **kwargs):
        if not cls.exists(**kwargs):
            res = cls(**kwargs)
            db.flush()
        else:
            res = cls.get(**kwargs)
        return res
