
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
