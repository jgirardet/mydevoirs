from kivy.tests.common import GraphicUnitTest, UnitTestTouch
from pony.orm import db_session, delete
from mydevoirs.database.database import db, db_init
import datetime
import os
from kivy.lang import Builder
from unittest.mock import patch
from mydevoirs.constants import APP_NAME
import time


def test_setup():
    os.environ["MYDEVOIRS_BASE_DIR"] = os.getcwd()
    Builder.load_file("mydevoirs/mydevoirs.kv")
    Builder.load_file("mydevoirs/itemwidget.kv")


test_setup()
db_init()


class Touche(UnitTestTouch):
    def click(self):
        self.touch_down()
        self.touch_up()


def get_touch(item):
    return Touche(item.pos[0] + item.size[0] / 2, item.pos[1] + item.size[1] / 2)


def matiere_grammaire():
    with db_session:
        return db.Matiere["Grammaire"]


def jour_today():
    with db_session:
        return db.Jour.get(date=datetime.date.today()) or db.Jour(
            date=datetime.date.today()
        )


def item_today():
    with db_session:
        i = db.Item(
            content="item today", matiere=matiere_grammaire(), jour=jour_today()
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
        # print(f"durée: {(time.time()-self.debut_time)*1000}")

    def check_super_init(self, parent, enfant, *args, fn="__init__", **kwargs):
        module = self.__module__.split("_")[-1]
        full_parent = ".".join((APP_NAME.lower(), module, parent, fn))
        with patch(full_parent) as m:
            try:
                enfant(*args, **kwargs)
            except:
                pass
            assert m.called
