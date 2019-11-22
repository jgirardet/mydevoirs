from kivy.lang import Builder
from kivy.properties import ColorProperty
from kivy.uix.settings import SettingItem
from kivy.uix.slider import Slider


class SettingSlider(SettingItem):
    def __init__(self, **kwargs):
        self.register_event_type("on_touch_up")
        kw = kwargs.copy()
        kw.pop("id", None)
        super(SettingItem, self).__init__(**kw)
        oSlider = ColorSlider()
        # oSlider.ID = aSlider["id"]
        # oSlider.ID = kwargs['id']
        self.add_widget(oSlider)
        oSlider.bind(on_touch_up=self.on_slider_moved)

    def set_value(self, section, key, value):
        # set_value normally reads the configparser values and runs on an error
        # to do nothing here
        return

    def on_slider_moved(self, instance, touch):
        if instance.collide_point(touch.x, touch.y):
            self.panel.settings.dispatch(
                "on_config_change",
                self.panel.config,
                self.section,
                self.key,
                instance.color,
            )


SLIDER_KV = """
<ColorSlider>:
    canvas.before:
        Color:
            rgb: self.color
        Rectangle:
            size: (self.width, self.height)
            pos: (self.x, self.y)

    max: 1530
    value: 1000
"""

Builder.load_string(SLIDER_KV)


class ColorSlider(Slider):

    color = ColorProperty()

    def on_value(self, *args):
        value = int(args[1])
        self.color = self.do_color(value)

    def do_color(self, x):

        if x >= 0 and x < 255:
            r = 255
            g = x
            b = 0

        elif x >= 255 and x < 510:
            r = 510 - x
            g = 255
            b = 0

        elif x >= 510 and x < 765:
            r = 0
            g = 255
            b = x - 510

        elif x >= 765 and x < 1020:
            r = 0
            g = 1020 - x
            b = 255

        elif x >= 1020 and x < 1275:
            r = x - 1020
            g = 0
            b = 255

        else:
            # elif x >= 1275 and x <= 1530:
            r = 255
            g = 0
            b = 1530 - x

        print(r, g, b)
        return (r / 255, g / 255, b / 255)
