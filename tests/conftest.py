from kivy.lang import Builder
from main import setup_start


def pytest_sessionstart():
    Builder.load_file("mydevoirs/mydevoirs.kv")
    setup_start()
