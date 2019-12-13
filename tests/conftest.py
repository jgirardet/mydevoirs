from kivy.lang import Builder

from main import setup_start
from mydevoirs.database import init_database
import pytest
import mydevoirs.database


def pytest_sessionstart():
    Builder.load_file("mydevoirs/mydevoirs.kv")
    setup_start()
    mydevoirs.database.db = init_database()

