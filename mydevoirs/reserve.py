
class SettingButtons(SettingItem):
    def __init__(self, **kwargs):
        self.register_event_type("on_release")
        # For Python3 compatibility we need to drop the buttons keyword
        # when calling super.
        kw = kwargs.copy()
        kw.pop("buttons", None)
        super(SettingItem, self).__init__(**kw)
        for aButton in kwargs["buttons"]:
            oButton = Button(text=aButton["title"], font_size="15sp")
            oButton.ID = aButton["id"]
            self.add_widget(oButton)
            oButton.bind(on_release=self.On_ButtonPressed)

    def set_value(self, section, key, value):
        # set_value normally reads the configparser values and runs on an error
        # to do nothing here
        return

    def On_ButtonPressed(self, instance):
        self.panel.settings.dispatch(
            "on_config_change", self.panel.config, self.section, self.key, instance.ID
        )

# box.add_widget(MyKeyboardListener(size_hint_y=0))


# class MyKeyboardListener(Widget):

#     def __init__(self, **kwargs):
#         super(MyKeyboardListener, self).__init__(**kwargs)
#         self._keyboard = Window.request_keyboard(
#             self._keyboard_closed, self, 'text')
#         if self._keyboard.widget:
#             # If it exists, this widget is a VKeyboard object which you can use
#             # to change the keyboard layout.
#             pass
#         self._keyboard.bind(on_key_down=self._on_keyboard_down)

#     def _keyboard_closed(self):
#         print('My keyboard have been closed!')
#         self._keyboard.unbind(on_key_down=self._on_keyboard_down)
#         self._keyboard = None

#     def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
#         app = App.get_running_app()

#         print('The key', keycode, 'have been pressed')
#         print(' - text is %r' % text)
#         print(' - modifiers are %r' % modifiers)

#         # Keycode is composed of an integer + a string
#         # If we hit escape, release the keyboard
#         if keycode[1] == 'escape':
#             keyboard.release()

#         if keycode[1] == 'left':
#             app = App.get_running_app()
#             app.carousel.load_previous()

#         if keycode[1] == 'right':
#             app = App.get_running_app()
#             app.carousel.load_next()


#         # Return True to accept the key. Otherwise, it will be used by
#         # the system.
#         return True
