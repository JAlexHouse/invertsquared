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
from kivy.clock import Clock
import random
import os
import time
from functools import partial


Window.size = (540, 960)
button_press_sound = SoundLoader.load('../Audio/BUTTON_PRESS.wav')
is_sound_enabled = True
is_music_enabled = True
background_music = SoundLoader.load('../Audio/BACKGROUND.wav')
dirname = os.path.dirname(__file__)

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
    current_level = {}
    rows = 3
    cols = 3
    moves_made = BoundedNumericProperty(0)
    max_moves = BoundedNumericProperty(15)
    time_limit = BoundedNumericProperty(15)
    time_elapsed = BoundedNumericProperty(0)
    timer = 0
    gridlayout = None
    answerlayout = None
    button_ids = {}
    random = False
    resume = False
    game_tile_sound = None
    filename = None
    level = None

    def on_enter(self):
        self.set_mode()
        
        if not self.resume:
            self.gridlayout = GridLayout(rows=self.rows, cols=self.cols)
            self.answerlayout = GridLayout(rows=self.rows, cols=self.cols)
            # generate answer key
            self.generate_answer()
            self.answerlayout.size_hint = [0.3, 0.17]
            self.answerlayout.pos = (0.35*self.width, 0.695*self.height)  # Not sure where to place this
            self.add_widget(self.answerlayout)

            # generate game board
            self.generate_grid()
            self.gridlayout.size_hint = [0.75, 0.43]  # height, width
            self.gridlayout.pos = (0.13*self.width, 0.25*self.height)  # x, y
            self.add_widget(self.gridlayout)
            self.user_key = "0" * self.rows * self.cols

            self.resume = True
        self.game_tile_sound = SoundLoader.load('../Audio/GAME_TILE_PRESS.wav')
        
        if self.game_mode == "Expert":
            self.start_timer()
        

        

    def generate_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                button = Button(background_normal="../Art/TILE.png", background_down="../Art/TILE_DOWN.png")
                button.bind(on_release=self.move_made)
                self.button_ids[button] = "{},{}".format(i, j)
                self.gridlayout.add_widget(button, len(self.gridlayout.children))

    def generate_answer(self):
        for _ in range(self.rows*self.cols):
            button = Button(background_normal="../Art/TILE.png", background_down="../Art/TILE_DOWN.png")
            self.answerlayout.add_widget(button, len(self.answerlayout.children))
        
        # if random, generate new answer_key
        if self.random:
            # while loop to make sure at least one tile is pressed
            while True:
                self.answer_key = ""
                for _ in range(self.rows*self.cols):
                    self.answer_key = self.answer_key + str(random.randint(0, 1))
                if "1" in self.answer_key:
                    break

        for index in range(len(self.answerlayout.children)):
            if self.answer_key[index] == "1":
                row, col = self.get_row_col_by_index(index)
                self.change_surrounding_tiles(index, row, col, is_answer_grid=True)
        
    def get_index_by_tile_id(self, col, row):
        return row * self.cols + col

    def get_row_col_by_index(self, index):
        return (index // self.cols, index % self.cols)

    def move_made(self, instance):
        self.game_tile_sound.play()

        row, col = (int(d) for d in self.button_ids[instance].split(','))
        index = self.get_index_by_tile_id(col, row)
        self.moves_made += 1
        self.user_key = self.user_key[:index] + ("1" if self.user_key[index] == "0" else "0") + self.user_key[index+1:]
        print("Pressed button row: {}, col: {}".format(row, col))

        self.change_surrounding_tiles(index, row, col)
        self.goal_reached()

    def change_surrounding_tiles(self, index, row, col, is_answer_grid=False):
        self.change_tile_color(index, is_answer_grid)
        # check if NOT top row
        if (row < self.rows - 1):
            top_index = self.get_index_by_tile_id(col, row + 1)
            self.change_tile_color(top_index, is_answer_grid)
        # check if NOT bottom row
        if (row > 0):
            bottom_index = self.get_index_by_tile_id(col, row - 1)
            self.change_tile_color(bottom_index, is_answer_grid)
        # check if NOT left column
        if (col < self.cols - 1):
            left_index = self.get_index_by_tile_id(col + 1, row)
            self.change_tile_color(left_index, is_answer_grid)
        # check if NOT right column
        if (col > 0):
            right_index = self.get_index_by_tile_id(col - 1, row)
            self.change_tile_color(right_index, is_answer_grid)

    def change_tile_color(self, index, is_answer_grid=False):
        grid = self.gridlayout if not is_answer_grid else self.answerlayout
        if grid.children[index].background_normal == "../Art/TILE.png":
            grid.children[index].background_normal = "../Art/TILE_DOWN.png"
            grid.children[index].background_down = "../Art/TILE_DOWN.png"
        else:
            grid.children[index].background_normal = "../Art/TILE.png"
            grid.children[index].background_down = "../Art/TILE.png"

    def goal_reached(self):
        if self.user_key == self.answer_key:
            print("Yay, you won!")
            self.open_won()
            self.clear_game()
        else:
            if self.game_mode != "Classic":
                self.ids.moves.text = "Moves Left: " + str(self.max_moves - self.moves_made)
                if self.moves_made == self.max_moves:
                    print("Oops, you lost!")
                    self.open_lost()
                    self.clear_game()

    def reset_board(self):
        self.moves_made = 0
        self.user_key = "0" * self.rows * self.cols
        if self.game_mode == "Classic":
            self.ids.moves.text = ""
        else:
            self.ids.moves.text = "Moves Left: " + str(self.max_moves - self.moves_made)

        for tile in self.gridlayout.children:
            tile.background_normal = "../Art/TILE.png"
            tile.background_down = "../Art/TILE_DOWN.png"
        self.start_timer()

    def clear_game(self):
        self.ids.extra_settings.text = ""     # to clear up numbers from timer
        self.moves_made = 0
        self.time_elapsed = 0
        self.gridlayout.clear_widgets()
        self.answerlayout.clear_widgets()
        self.clear_widgets([self.gridlayout, self.answerlayout])
        self.resume = False

    def open_pause(self):
        if self.game_mode == "Expert":
            self.timer.cancel()
        popup = Pause()
        popup.open()

    def open_won(self):
        self.timer.cancel()
        self.current_level[self.game_mode] = self.current_level[self.game_mode] + 1
        popup = GameWin()
        popup.open()
        self.clear_game()

    def open_lost(self):
        self.timer.cancel()
        popup = GameLose()
        popup.open()
        self.clear_game()

    def set_mode(self):
        app = App.get_running_app()
        self.game_mode = app.DIFFICULTY

        # Initialize what level we are on for each difficulty level
        if self.game_mode not in self.current_level:
            self.current_level[self.game_mode] = 1

        if self.game_mode == "Classic":
            self.filename = os.path.join(dirname, '../Levels/Classic.txt')
            self.ids.moves.text = ""

            with open(self.filename) as f:
                for _ in range(self.current_level[self.game_mode] - 1):
                    next(f)
                # level data in the format col row answerkey
                level_info = f.readline().rstrip('\n').split(' ')
                rows, cols, self.answer_key = level_info
                self.rows = int(rows)
                self.cols = int(cols)
        
            # reached end of file: will read random levels now
            self.random = level_info == ''
        elif self.game_mode == "Challenge" or self.game_mode == "Expert":
            self.filename = os.path.join(dirname, '../Levels/Challenge.txt')
            self.ids.moves.text = ""

            with open(self.filename) as f:
                for _ in range(self.current_level[self.game_mode] - 1):
                    next(f)
                # level data in the format col row answerkey timelimit
                level_info = f.readline().rstrip('\n').split(' ')
                rows, cols, self.answer_key, time_limit = level_info
                self.rows = int(rows)
                self.cols = int(cols)
                self.time_limit = float(time_limit)

            # reached end of file: will read random levels now
            self.random = level_info == ''
        else:
            # FIXME: add behavior for other difficulty settings
            self.random = True
            self.ids.moves.text = "Moves Left: " + str(self.max_moves - self.moves_made)
    def start_timer(self):
        if self.game_mode == "Expert":
            self.ids.extra_settings.text = str(self.time_limit - self.time_elapsed)
            self.timer = Clock.schedule_interval(partial(self.timer_tick), 1)
    #update the timer every sec        
    def timer_tick(self, *largs):
        self.time_elapsed += 1
        self.ids.extra_settings.text = str(self.time_limit - self.time_elapsed)
        if self.time_limit - self.time_elapsed <= 0:
            self.timer.cancel()
            self.open_lost()


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
