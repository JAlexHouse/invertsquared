from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty, BoundedNumericProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
import random


Window.size = (540, 960)
button_press_sound = SoundLoader.load('../Audio/BUTTON_PRESS.wav')
is_sound_enabled = True
is_music_enabled = True
background_music = SoundLoader.load('../Audio/BACKGROUND.wav')

# creating .py class (inherently calls on .kv class)
# alphabetical order ish
class GameLose(ModalView):
    def on_open(self):
        game_lose_sound = SoundLoader.load('../Audio/GAME_LOSE.wav')
        game_lose_sound.play() 


class GameWin(ModalView):
    def on_open(self):
        game_win_sound = SoundLoader.load('../Audio/GAME_WIN.wav')
        game_win_sound.play()


class HomeScreen(Screen):
    def btn_press_audio(self):
        if is_sound_enabled:
            button_press_sound.play()

class SettingsScreen(Screen):
    def enable_or_disable_audio(self):
        global is_sound_enabled
        is_sound_enabled = not is_sound_enabled

    def enable_or_disable_music(self):
        if background_music.state == "stop":
            background_music.play()
        else:
            background_music.stop()


class ShareScreen(Screen):
    pass


class MoreScreen(Screen):
    pass


class PauseScreen(Screen):
    pass


class Pause(ModalView):
    pass


class WinScreen(Screen):
    pass


class PlayScreen(Screen):
    game_mode = ""
    rows = 3
    cols = 3
    moves_made = BoundedNumericProperty(0)
    max_moves = BoundedNumericProperty(15)
    time_limit_sec = BoundedNumericProperty(30)
    time_remaining = StringProperty()
    gridlayout = GridLayout(rows=rows, cols=cols)
    answerlayout = GridLayout(rows=rows, cols=cols)
    button_ids = {}
    random = True
    resume = False
    game_tile_sound = None

    def on_enter(self):
        self.set_mode()
        if not self.resume:
            # generate answer key
            self.generate_answer()
            self.answerlayout.size_hint = [0.3, 0.17]
            self.answerlayout.pos = (0.35*self.width, 0.7*self.height)  # Not sure where to place this
            self.add_widget(self.answerlayout)

            # generate game board
            self.generate_grid()
            self.gridlayout.size_hint = [0.75, 0.43]  # height, width
            self.gridlayout.pos = (0.13*self.width, 0.25*self.height)  # x, y
            self.add_widget(self.gridlayout)

            self.resume = True
        self.game_tile_sound = SoundLoader.load('../Audio/GAME_TILE_PRESS.wav')
        

    def generate_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                button = Button(background_normal="../Art/TILE.png", background_down="../Art/TILE_DOWN.png")
                button.bind(on_release=self.move_made)
                self.button_ids[button] = "{},{}".format(i, j)
                self.gridlayout.add_widget(button, len(self.gridlayout.children))

    def generate_answer(self):
        if random:
            for i in range(self.rows):
                for j in range(self.cols):
                    button = Button()
                    color = random.randint(0, 1)
                    if color:
                        button.background_normal = "../Art/TILE.png"
                        button.background_down = "../Art/TILE.png"
                    else:
                        button.background_normal = "../Art/TILE_DOWN.png"
                        button.background_down = "../Art/TILE_DOWN.png"
                    self.answerlayout.add_widget(button, len(self.answerlayout.children))
            # if all answer tiles are grey, then redo the answer generation process
            if all([button.background_normal == "Art/TILE.png" for button in self.answerlayout.children]):
                self.answerlayout.clear_widgets()
                self.generate_answer()

    def move_made(self, instance):
        self.game_tile_sound.play()

        row, col = (int(d) for d in self.button_ids[instance].split(','))
        index = self.get_index_by_tile_id(col, row)
        self.moves_made += 1
        self.change_tile_color(index)
        print("Pressed button {},{}".format(row, col))

        # check if NOT top row
        if (row < self.rows - 1):
            top_index = self.get_index_by_tile_id(col, row + 1)
            self.change_tile_color(top_index)
        # check if NOT bottom row
        if (row > 0):
            bottom_index = self.get_index_by_tile_id(col, row - 1)
            self.change_tile_color(bottom_index)
        # check if NOT left column
        if (col < self.cols - 1):
            left_index = self.get_index_by_tile_id(col + 1, row)
            self.change_tile_color(left_index)
        # check if NOT right column
        if (col > 0):
            right_index = self.get_index_by_tile_id(col - 1, row)
            self.change_tile_color(right_index)

        self.goal_reached()

    def get_index_by_tile_id(self, col, row):
        return row * self.cols + col

    def change_tile_color(self, index):
        if self.gridlayout.children[index].background_normal == "../Art/TILE.png":
            self.gridlayout.children[index].background_normal = "../Art/TILE_DOWN.png"
            self.gridlayout.children[index].background_down = "../Art/TILE_DOWN.png"
        else:
            self.gridlayout.children[index].background_normal = "../Art/TILE.png"
            self.gridlayout.children[index].background_down = "../Art/TILE.png"

    def goal_reached(self):
        for i in range(self.cols):
            for j in range(self.rows):
                index = self.get_index_by_tile_id(i, j)
                if self.gridlayout.children[index].background_normal != self.answerlayout.children[index].background_normal:
                    if self.game_mode != "Classic":
                        self.ids.moves.text = "Moves Left: " + str(self.max_moves - self.moves_made)
                        if self.moves_made == self.max_moves:
                            print("Oops, you lost!")
                            self.open_lost()
                            self.clear_game()
                            return
                    return
        print("Yay, you won!")
        self.open_won()
        self.clear_game()

    def reset_board(self):
        self.moves_made = 0
        if self.game_mode == "Classic":
            self.ids.moves.text = ""
        else:
            self.ids.moves.text = "Moves Left: " + str(self.max_moves - self.moves_made)

        for tile in self.gridlayout.children:
            tile.background_normal = "../Art/TILE.png"
            tile.background_down = "../Art/TILE_DOWN.png"

    def clear_game(self):
        self.moves_made = 0
        self.gridlayout.clear_widgets()
        self.answerlayout.clear_widgets()
        self.clear_widgets([self.gridlayout, self.answerlayout])
        self.resume = False

    def open_pause(self):
        popup = Pause()
        popup.open()

    def open_won(self):
        popup = GameWin()
        popup.open()

    def open_lost(self):
        popup = GameLose()
        popup.open()

    def set_mode(self):
        app = App.get_running_app()
        self.game_mode = app.DIFFICULTY
        if self.game_mode == "Classic":
            self.ids.moves.text = ""
        else:
            self.ids.moves.text = "Moves Left: " + str(self.max_moves - self.moves_made)


class ScreenManager(ScreenManager):
    def build(self):
        return

# app class; runs the app
class InvertApp(App):
    def build(self):
        background_music.loop = True
        background_music.play()

if __name__ == '__main__':
    app = InvertApp()
    app.run()
