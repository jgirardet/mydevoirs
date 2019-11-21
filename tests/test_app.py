from .fixtures import *


from mydevoirs.app import MyDevoirsApp

class TestMyDevoirsApp(MyDevoirsTestCase):
    def test_init_super(self):
        self.check_super_init("App", MyDevoirsApp)
        a = MyDevoirsApp()
        assert a.get_application_name() == APP_NAME