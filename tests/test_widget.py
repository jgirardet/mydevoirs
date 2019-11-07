from mydevoirs import __version__
from kivy.tests.common import GraphicUnitTest, UnitTestTouch
from mydevoirs.widgets import ItemWidget
from kivy.lang import Builder
import os

os.environ["MYDEVOIRS_BASE_DIR"] = os.getcwd()
Builder.load_file("mydevoirs/mydevoirs.kv")
from pony.orm import db_session
from mydevoirs.database.database import db
import datetime


def test_version():
    assert __version__ == "0.1.0"


with db_session:
    m = db.Matiere["Français"]
    j = db.Jour(date=datetime.date.today())
    db.Item(content="omko", matiere=m, jour=j)
    db.Item(content="omko", matiere=m, jour=j, done=True)


class Touche(UnitTestTouch):
    def click(self):
        self.touch_down()
        self.touch_up()


def get_touch(item):
    return Touche(
        item.ids.done.pos[0] + item.ids.done.size[0] / 2,
        item.ids.done.pos[1] + item.ids.done.size[1] / 2,
    )


class ItemWidgetTestCase(GraphicUnitTest):
    def test_render(self):

        for n in [1, 2]:
            with db_session:
                d = db.Item[n].to_dict()

            item = ItemWidget(**d)
            self.render(item)

            assert item.ids.done.active == d["done"]

            touch = get_touch(item)
            touch.click()

            with db_session:
                self.assertTrue(db.Item[n].done == (not d["done"]))
