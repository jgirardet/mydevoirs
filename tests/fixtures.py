from kivy.tests.common import GraphicUnitTest, UnitTestTouch
from pony.orm import db_session, delete
from mydevoirs.database.database import db, db_init
import datetime
import os
from kivy.lang import Builder
from unittest.mock import patch
from mydevoirs.constants import APP_NAME, MATIERES
import time
from mimesis import Generic
import random
from main import setup_start

gen = Generic("fr")


def setup_test():
    Builder.load_file("mydevoirs/mydevoirs.kv")
    setup_start()


setup_test()


class Touche(UnitTestTouch):
    def click(self):
        self.touch_down()
        self.touch_up()


def get_touch(item):
    return Touche(item.pos[0] + item.size[0] / 2, item.pos[1] + item.size[1] / 2)


def f_matiere(matiere=None):
    matiere = matiere or random.choice(list(MATIERES))
    with db_session:
        return db.Matiere[matiere]


def f_jour(jour=None):
    jour = jour or gen.datetime.date()
    with db_session:
        return db.Jour.get(date=jour) or db.Jour(date=jour)


def f_item(content=None, matiere=None, jour=None, done=None):
    content = content or gen.text.sentence()
    done = done or False
    with db_session:
        i = db.Item(
            content=content, matiere=f_matiere(matiere), jour=f_jour(jour), done=done
        )
        return i


class MyDevoirsTestCase(GraphicUnitTest):
    def setUp(self):
        self.debut_time = time.time()
        super().setUp()
        with db_session:
            for entity in db.entities.values():
                if entity.__name__ != "Matiere":
                    delete(e for e in entity)

    def tearDown(self):
        super().tearDown()
        print(f"durée: {(time.time()-self.debut_time)*1000}")

    def check_super_init(self, parent, enfant, *args, fn="__init__", **kwargs):
        module = self.__module__.split("_")[-1]
        full_parent = ".".join((APP_NAME.lower(), module, parent, fn))
        with patch(full_parent) as m:
            try:
                enfant(*args, **kwargs)
            except:
                pass
            assert m.called

            del enfant
