import platform
import random
import tempfile
import time
from unittest.mock import patch

from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.core.window import Keyboard
from kivy.tests.common import GraphicUnitTest, UnitTestTouch
from mimesis import Generic
from pony.orm import db_session, delete

from mydevoirs.constants import APP_NAME, MATIERES
from mydevoirs.database import db
from mydevoirs.utils import Path

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

    TIMER = False

    def setUp(self, no_db=False):
        super().setUp()

        if not no_db:
            with db_session:
                for entity in db.entities.values():
                    if entity.__name__ != "Matiere":
                        delete(e for e in entity)

        self.T = TempFile()

        EventLoop.ensure_window()
        self.window = EventLoop.window

        if self.TIMER:
            self.debut_time = time.time()

    def tearDown(self):
        super().tearDown()
        self.T.cleanup()
        self.unschedule_all()
        self.clear_window()
        if self.TIMER:
            print(f"durée: {(time.time()-self.debut_time)*1000}")

    def unschedule_all(self):
        for e in Clock.get_events():
            Clock.unschedule(e)

    def clear_window(self):
        self.window.clear()
        [self.window.remove_widget(x) for x in self.window.children]

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
        popup.content.ids[choix].trigger_action(0)


def platform_dispatcher(test, linux, windows):
    if platform.system() == "Linux":  # pragma: no cover_win
        assert test == linux
    elif platform.system() == "Windows":  # pragma: no cover_linux
        assert test == windows


# class NoGraphicTestCase(TestCase):

#     def setUp(self):
#         self.debut_time = time.time()

#         EventLoop.ensure_window()
#         self.window = EventLoop.window
#         self.T = TempFile()

#     def tearDown(self):
#         self.T.cleanup()
#         print(f"durée: {(time.time()-self.debut_time)*1000}")

#     def click(self, widget):
#         t = get_touch(widget)
#         t.click()

#     def popup_click(self, choix):
#         popup = self.window.children[0]
#         popup.content.ids[choix].trigger_action(0)


class TempFile:
    def __init__(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmpdir.name)
        self.file = self.tmpfile()
        self.filename = self.tmpfilename()
        assert not self.filename.exists()

    def tmpfile(self):
        file = self.dir / gen.file.file_name()
        file.touch()
        return file

    def tmpfilename(self):
        return self.dir / gen.file.file_name()

    def cleanup(self):
        self._tmpdir.cleanup()
