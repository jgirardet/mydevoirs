from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

from mydevoirs.imagebutton import ImageButton
from tests.fixtures import MyDevoirsTestCase


class TestImageButton(MyDevoirsTestCase):
    def check_init(self):
        self.check_super_init(Image, ImageButton)
        self.check_super_init(ButtonBehavior, ImageButton)

    def test_color_update_on_state(self):
        a = ImageButton()
        assert a.color == [1, 1, 1, 1]
        a.state = "down"
        assert a.color == [1, 1, 1, 0.5]
        a.state = "normal"
        assert a.color == [1, 1, 1, 1]
