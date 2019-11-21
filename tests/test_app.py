from .fixtures import *


from mydevoirs.app import MyDevoirsApp
from kivy.config import Config


class TestMyDevoirsApp(MyDevoirsTestCase):
    def setUp(self):
        super().setUp()
        # Config.set('agenda', 'retain_time', '50')
        # with patch(
        #     "mydevoirs.agenda.BaseGrid.get_days_to_show",
        #     return_value=[True, True, False, True, True, False, False],
        # ):
        self.app = MyDevoirsApp()
        self.app.build()
        self.actionbar = self.app.box.children[1]

    def test_init_super(self):
        self.check_super_init("App", MyDevoirsApp)
        assert self.app.get_application_name() == APP_NAME

    def test_sm(self):

        assert self.app.sm.current == "agenda"
        assert self.app.sm.screen_names == ["agenda", "todo"]

    def test_go_aatodo(self):
        self.app.sm.current = "agenda"
        todolist = self.app.sm.get_screen("todo").todolist
        if self.app.sm.current == "agenda":  # let time of change to be done
            # self.app.go_todo()
            self.actionbar.ids.go_todo.trigger_action(0)

        # with patch.object(self.app, 'go_todo') as m:
        #     # self.app.sm.current = "agenda"
        #     self.actionbar.ids.go_todo.trigger_action(0)
        #     assert m.called

        assert self.app.sm.current == "todo"
        assert self.app.sm.transition.direction == "down"
        assert id(todolist) != id(self.app.sm.current_screen.todolist)  # widget rebuild

    # def test_go_agenda(self):
    #     print(self.app.sm.current)
    #     self.app.sm.current = "todo"
    #     carousel = self.app.sm.get_screen("agenda").carousel
    #     click = lambda: self.actionbar.ids.go_agenda.trigger_action(0)
    #     import time
    #     time.sleep(0.3)
    #     click()
    #     # else:

    #     assert self.app.sm.current == "agenda"
    #     assert self.app.sm.transition.direction == "up"
    #     assert id(carousel) != id(self.app.sm.current_screen.carousel) # widget rebuild
