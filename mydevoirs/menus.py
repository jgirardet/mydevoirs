#!python
#!/usr/bin/env python
from kivy.app import App
from kivy.uix.bubble import Bubble
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder

Builder.load_string(
    """
#template for menu items
[ListButton@ToggleButton]
    background_down: 'atlas://data/images/defaulttheme/bubble_btn'
    background_normal: 'atlas://data/images/defaulttheme/bubble_btn_pressed'
    group: 'context_menue_root'
    on_release: ctx.on_release(self) if hasattr(ctx, 'on_release') else None
    size_hint: ctx.size_hint if hasattr(ctx, 'size_hint') else (1, 1)
    width: ctx.width if hasattr(ctx, 'width') else 1
    text: ctx.text if hasattr(ctx, 'text') else ''
    Image:
        source: ctx.btn_img if ctx.text == 'hows' \
            else 'atlas://data/images/defaulttheme/bubble_btn'
        size: (20, 20)
        y: self.parent.y + (self.parent.height/2) - (self.height/2)
        x: self.parent.x + (self.parent.width - self.width)

<Test>
    Button:
        text: 'press to launch menu'
        size_hint: .2, .2
        on_release:  root.add_menu(args[0])

<Cmenu>
    size_hint: None, None
    size: 120, 250
    pos: (5, 50)
    padding: 5
    background_color: .2, .9, 1, .7
    #wanna have some fun? set this to 'data/images/image-loading.gif'
    background_image: 'atlas://data/images/defaulttheme/button_pressed'
    orientation: 'vertical'
    BoxLayout:
        padding: 5
        ScrollView:
            bar_color: (0,0,0,0)
            BoxLayout:
                size_hint: None, 1
                width: root.width * 5 - 40
                #root menu add/edit items here to show them in root menu
                BoxLayout:
                    orientation: 'vertical'
                    id: premier
                    ListButton:
                        text: 'Hello'
                        on_release: root.menu_selected
                    ListButton:
                        text: 'deux'
                        on_release: root.menu_selected
                    ListButton:
                        text: 'hows'
                        #'>'image
                        btn_img: 'atlas://data/images/defaulttheme/tree_closed'
                        on_release: root.menu_selected
             
                # end root menu
                #sub-menu
                BoxLayout:
                    id: deuxième
                    ListButton:
                        # go back(root menu) button
                        text: '<'
                        size_hint: (.15, 1)
                        on_release: root.menu_selected
                    BoxLayout:
                        orientation: 'vertical'
                        ListButton:
                            text: 'The'
                            on_release: root.menu_selected
                #end sub-menu
                #sub-menu
                BoxLayout:
                    id: deuxième
                    ListButton:
                        # go back(root menu) button
                        text: '<'
                        size_hint: (.15, 1)
                        on_release: root.menu_selected
                    BoxLayout:
                        orientation: 'vertical'
                        ListButton:
                            text: 'The deuxième'
                            on_release: root.menu_selected
                #end sub-menu
                BoxLayout:
                    id: deuxième
                    ListButton:
                        # go back(root menu) button
                        text: '<'
                        size_hint: (.15, 1)
                        on_release: root.menu_selected
                    BoxLayout:
                        orientation: 'vertical'
                        ListButton:
                            text: 'The deuxième'
                            on_release: root.menu_selected
                #end sub-menu
                BoxLayout:
                    id: deuxième
                    ListButton:
                        # go back(root menu) button
                        text: '<'
                        size_hint: (.15, 1)
                        on_release: root.menu_selected
                    BoxLayout:
                        orientation: 'vertical'
                        ListButton:
                            text: 'The deuxième'
                            on_release: root.menu_selected
                #end sub-menu
"""
)


class Cmenu(Bubble):
    def menu_selected(self, *l):
        print(l[0].parent.parent.parent)
        if l[0].text == "hows":
            # move to sub menu
            Animation(scroll_x=0.25, d=0.1).start(l[0].parent.parent.parent)
            # l[0].parent.parent.parent change this and everything relative to something non-relative if you want-to make the menu more extensible
        elif l[0].text == "deux":
            # move back to root menu
            Animation(scroll_x=1, d=0.1).start(l[0].parent.parent.parent)
        elif l[0].text == "<":
            # move back to root menu
            Animation(scroll_x=0, d=0.1).start(l[0].parent.parent.parent)
        else:
            # fade out animation
            (r, g, b, a) = self.parent.context_menu.background_color

            def on_anim_complete(*l):
                self.parent.context_menu.background_color = (r, g, b, a)
                self.parent.remove_widget(self.parent.context_menu)

            anim = Animation(background_color=(0, 0, 0, 0), d=0.1)
            anim.start(self.parent.context_menu)
            anim.bind(on_complete=on_anim_complete)
            print(l[0].text + " selected")


class Test(FloatLayout):
    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)

    def on_touch_down(self, *l):
        # allow kids to get touch
        if super(Test, self).on_touch_down(*l):
            return True
        # remove menu when touched and menu exists
        if hasattr(self, "context_menu"):
            self.remove_widget(self.context_menu)

    def add_menu(self, obj, *l):
        if not hasattr(self, "context_menu"):
            self.context_menu = Cmenu()
        self.remove_widget(self.context_menu)
        self.add_widget(self.context_menu)
        self.context_menu.pos = obj.pos[0] + obj.width, obj.pos[1]


class MyApp(App):
    def build(self):
        return Test()


if __name__ == "__main__":
    MyApp().run()
