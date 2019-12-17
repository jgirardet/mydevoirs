import platform
import random
import time
from unittest.mock import patch

from kivy.base import EventLoop
from kivy.core.window import Keyboard
from kivy.tests.common import GraphicUnitTest, UnitTestTouch
from mimesis import Generic
from pony.orm import db_session, delete

from mydevoirs.constants import APP_NAME, MATIERES
from mydevoirs.database import db, init_database
import mydevoirs.database
from kivy.clock import Clock
from mydevoirs.itemwidget import ItemWidget

gen = Generic("fr")


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

    # @classmethod
    # def setUpClass(cls):
    #     print(mydevoirs.database)
        
    #     # mydevoirs.database.db = init_database()

    ASYNC_TO_CLEAN = [str(ItemWidget._set_content).split()[1]]

    def clean_async_calls(self):
        for e in Clock.get_events():
            for a in self.ASYNC_TO_CLEAN:
                if a  in str(e.callback):
                    e.cancel()

    def setUp(self,no_db=False):
        super().setUp()
        self.debut_time = time.time()
        if not no_db:
            with db_session:
                for entity in db.entities.values():
                    if entity.__name__ != "Matiere":
                        delete(e for e in entity)

        EventLoop.ensure_window()
        self.window = EventLoop.window
        [self.window.remove_widget(x) for x in self.window.children]

    def tearDown(self):
        super().tearDown()
        self.window.clear()

        

        print(f"durée: {(time.time()-self.debut_time)*1000}")


    def check_super_init(self, parent, enfant, *args, fn="__init__", **kwargs):
        module = self.__module__.split("_")[-1]
        full_parent = ".".join((APP_NAME.lower(), module, parent, fn))
        with patch(full_parent) as m:
            try:
                enfant(*args, **kwargs)
            except Exception:
                pass
            assert m.called

            del enfant

    def add_to_window(self, w, clear=False):
        if clear:
            self.window.clear()
        self.window.add_widget(w)

    def press_key(self, key, scancode=None, codepoint=None, modifier=None, **kwargs):
        if isinstance(key, str):
            key = Keyboard.keycodes[key]
        self.window.dispatch(
            "on_key_down", key, scancode, codepoint, modifier, **kwargs
        )

    def click(self, widget):
        t = get_touch(widget)
        t.click()

    def popup_click(self, choix):
        popup = self.window.children[0]
        print(popup.title, choix)
        popup.content.ids[choix].trigger_action(0)


def platform_dispatcher(test, linux, windows):
    if platform.system() == "Linux":  # pragma: no cover_win
        assert test == linux
    elif platform.system() == "Windows":  # pragma: no cover_linux
        assert test == windows
