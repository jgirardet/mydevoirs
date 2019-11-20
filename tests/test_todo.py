from .fixtures import *
from mydevoirs.todo import TodoItemWidget, Todo, TodoList
from unittest.mock import patch
from pony.orm import db_session


class TodoItemWidgetTestCas(MyDevoirsTestCase):
    def test_on_done(self):
        self.check_super_init("ItemWidget", TodoItemWidget)

        with patch("mydevoirs.todo.App.get_running_app") as m:
            with db_session:
                it = TodoItemWidget(**item_today().to_dict())
            it.loaded_flag = True
            self.render(it)

            t = get_touch(it.ids.done)
            t.click()
            self.render(it)
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
