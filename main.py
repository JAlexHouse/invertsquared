import kivy
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

# creating .kv class
Builder.load_string("""
<HomeScreen>:
    rows: 3
    AnchorLayout:
        anchor_x: "center"
        anchor_y: "top"
        Label:
            text: "Welcome to Invert2!"
    AnchorLayout:
        anchor_x: "left"
        anchor_y: "bottom"
        Button:
            text: "Play"
            size_hint: (0.1, 0.1)
            on_press: root.manager.current = "Play"
    AnchorLayout:
        anchor_x: "center"
        anchor_y: "bottom"
        Button:
            text: "Settings"
            size_hint: (0.1, 0.1)
            on_press: root.manager.current = "Settings"
    AnchorLayout:
        anchor_x: "right"
        anchor_y: "bottom"
        Button: 
            text: "Quit"
            size_hint: (0.1, 0.1)
            on_press: quit() 
            
<SettingsScreen>:
    Label: 
        text: "Settings"
        pos: 0, 250
    BoxLayout:
        orientation: "horizontal"
        size: (20, 20)
        Button:
            text: "Setting 1"
            size_hint: (0.3, 0.3)
            padding: [20, 20]
        Button:
            text: "Setting 2"
            size_hint: (0.3, 0.3)
            padding: [20, 20]
        Button:
            text: "Setting 3"
            size_hint: (0.3, 0.3)
            padding: [20, 20]
        Button:
            text: "Back to Home"
            size_hint: (0.3, 0.3)
            padding: [20, 20]
            on_press: root.manager.current = "Home"
            
<PlaySetScreen>:
    Label: 
        text: "Settings"
    BoxLayout:
        orientation: "horizontal"
        size: (20, 20)
        Button:
            text: "Setting 1"
            size_hint: (0.3, 0.3)
            padding: [20, 20]
        Button:
            text: "Setting 2"
            size_hint: (0.3, 0.3)
            padding: [20, 20]
        Button:
            text: "Setting 3"
            size_hint: (0.3, 0.3)
            padding: [20, 20]
        Button:
            text: "Back to Home"
            size_hint: (0.3, 0.3)
            padding: [20, 20]
            on_press: root.manager.current = "Home"
        Button:
            text: "Resume Game"
            size_hint: (0.3, 0.3)
            padding: [20, 20]
            on_press: root.manager.current = "Play"
            
<PlayScreen>:
    AnchorLayout:
        anchor_x: "center"
        anchor_y: "top"
        Label:
            text: "Time to Play! :D"
    RelativeLayout:
        Button: 
            text: "Settings"
            size_hint: (0.1, 0.1)
            pos: 0, 540
            on_press: root.manager.current = "PlaySet"
        Button:
            text: "Home"
            size_hint: (0.1, 0.1)
            pos: 80, 540
            on_press: root.manager.current = "Home"
""")


# creating .py class (inherently calls on .kv class)
class HomeScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class PlaySetScreen(Screen):
    pass


class PlayScreen(Screen):
    pass


sm = ScreenManager(transition=FadeTransition())
sm.add_widget(HomeScreen(name="Home"))
sm.add_widget(SettingsScreen(name="Settings"))
sm.add_widget(PlaySetScreen(name="PlaySet"))
sm.add_widget(PlayScreen(name="Play"))


# app class; runs the app
class InvertApp(App):
    def build(self):
        # can assign self.boop = Boop(); customizes self stuff
        return sm


if __name__ == '__main__':
    InvertApp().run()
