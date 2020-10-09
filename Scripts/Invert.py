from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition


# creating .py class (inherently calls on .kv class)
class HomeScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class PlaySetScreen(Screen):
    pass


class PlayScreen(Screen):
    pass


class ScreenManager(ScreenManager):
    pass


# app class; runs the app
class InvertApp(App):
    def build(self):
        return Builder.load_file('Invert.kv')


if __name__ == '__main__':
    InvertApp().run()
