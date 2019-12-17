import datetime
from unittest.mock import patch

from pony.orm import db_session

from mydevoirs.todo import DateLabel, Todo, TodoItemWidget, TodoList

from .fixtures import *


class TodoItemWidgetTestCas(MyDevoirsTestCase):
    def test_on_done(self):
        self.check_super_init("ItemWidget", TodoItemWidget)

        with patch("mydevoirs.todo.App.get_running_app") as m:
            with db_session:
                it = TodoItemWidget(**f_item().to_dict())
            it.loaded_flag = True
            it.ids.done.trigger_action(0)
            assert m.return_value.todo.reload.called


class TestTodoScreen(MyDevoirsTestCase):

    def test_init(self):
        self.check_super_init("Screen", Todo)
        t = Todo()
        assert isinstance(t.todolist, TodoList)

    def test_reload(self):
        t = Todo()
        tl = t.todolist
        t.reload()
        assert len(t.children) == 1
        assert tl != t.todolist


class TestTodoList(MyDevoirsTestCase):
    def _gen_ddb(self):
        for i in gen.datetime.bulk_create_datetimes(
            date_start=datetime.date.today(),
            date_end=datetime.date.today() + datetime.timedelta(days=10),
            days=2,
        ):
            f_item(jour=i, done=False)
            f_item(jour=i, done=False)
            f_item(jour=i, done=True)

    def test_init(self):
        self.check_super_init("BoxLayout", TodoList)

    def test_load_items(self):

        self._gen_ddb()

        t = TodoList()
        assert len(t.box.children) == 18  # 6 label + 18 item - 6 done

        temoin = 1
        for i in t.box.children[::-1]:
            if str(temoin) == "1":
                assert isinstance(i, DateLabel)
                temoin += 1
            else:
                assert isinstance(i, TodoItemWidget)
                temoin = 1 if temoin == 3 else 3
