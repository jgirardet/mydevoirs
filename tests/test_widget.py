# from mydevoirs import __version__
# from mydevoirs.widgets import ItemWidget, Clock, JourItems, JourWidget, BaseGrid


# from pony.orm import db_session, delete
from mydevoirs.database.database import db, db_init
# from mydevoirs.constants import MATIERES
# import datetime
# from unittest.mock import patch, MagicMock
# import pytest
# from kivy.config import ConfigParser
from .fixtures import *
# from kivy.uix.dropdown import DropDown
# from mydevoirs.matiere_dropdown import MatiereOption

db_init()


# test_setup()


# class JourItemsTestCase(MyDevoirsTestCase):
#     def setUp(self):

#         super().setUp()

#         self.a = item_today()
#         self.b = item_today()
#         self.c = item_today()

#         self.jouritems = JourItems(self.a.jour.date)

#         self.render(self.jouritems)

#     def test_load(self):

#         assert len(self.jouritems.children) == 3
#         assert self.jouritems.children[0].entry == self.c.id

#     # def test_remove(self):

#     #     remove_item = self.jouritems.children[0].ids.remove_item

#     #     with patch(remove_item, "on_release"):
#     #         touch = get_touch(remove_item)
#     #         touch.click()
#     #         self.render(self.jouritems)
#     #         assert len(self.jouritems.children) == 2

#     #     assert self.jouritems.children[1].entry == self.a.id
#     #     assert self.jouritems.children[0].entry == self.b.id

#     #     with db_session:
#     #         assert self.c.id not in db.Item.select()


# class JourWidgetTestCase(MyDevoirsTestCase):
#     def setUp(self):

#         super().setUp()

#         self.a = item_today()
#         self.b = item_today()
#         self.c = item_today()

#     def test_nice_date(self):
#         jour = JourWidget(datetime.date(2019, 11, 12))
#         assert jour.ids.titre_jour.text == "mardi 12 novembre 2019"

#     def test_add(self):
#         jour = JourWidget(self.a.jour.date)
#         self.render(jour)
#         assert len(jour.jouritem.children) == 3

#         get_touch(jour.ids.add_button).click()
#         self.render(jour)

#         assert len(jour.jouritem.children) == 4
#         print(self.Window.children)
#         assert any(isinstance(x, DropDown) for x in self.Window.children)
#         with db_session:
#             assert db.Item[jour.jouritem.children[0].entry]


# class TestBaseGrid(MyDevoirsTestCase):
#     def test_get_week_days(self):
#         with patch.object(
#             BaseGrid,
#             "get_days_to_show",
#             return_value=[False, True, False, True, False, True, False],
#         ):
#             b = BaseGrid(day=datetime.date(2019, 11, 12))
#             for d, z in zip(
#                 b.children,
#                 [
#                     datetime.date(2019, 11, 16),
#                     datetime.date(2019, 11, 14),
#                     datetime.date(2019, 11, 12),
#                 ],
#             ):

#                 assert d.date == z
