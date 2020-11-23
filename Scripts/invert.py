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
from kivy.uix.image import Image
import time
from functools import partial
import webbrowser
from threading import Timer


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

        star_layout = BoxLayout(orientation="horizontal")
        star_layout.size_hint = [1, 0.33]
        #Replace Tile image with Gray star img, and Tile_Down with yellow star img
        for _ in range(3):
            button = Button(background_normal="../Art/NOSTAR.png", background_down="../Art/NOSTAR.png")
            star_layout.add_widget(button, len(star_layout.children))
        star_layout.pos = (50, 50)
        if self.level_stars == 1:
            star_layout.children[2].background_normal = "../Art/GOLDSTAR.png"
            star_layout.children[2].background_down = "../Art/GOLDSTAR.png"
        elif self.level_stars == 2:
            star_layout.children[2].background_normal = "../Art/GOLDSTAR.png"
            star_layout.children[2].background_down = "../Art/GOLDSTAR.png"
            star_layout.children[1].background_normal = "../Art/GOLDSTAR.png"
            star_layout.children[1].background_down = "../Art/GOLDSTAR.png"
        elif self.level_stars == 3:
            star_layout.children[2].background_normal = "../Art/GOLDSTAR.png"
            star_layout.children[2].background_down = "../Art/GOLDSTAR.png"
            star_layout.children[1].background_normal = "../Art/GOLDSTAR.png"
            star_layout.children[1].background_down = "../Art/GOLDSTAR.png"
            star_layout.children[0].background_normal = "../Art/GOLDSTAR.png"
            star_layout.children[0].background_down = "../Art/GOLDSTAR.png"
        self.add_widget(star_layout)

    def set_stars(self, stars):
        self.level_stars = stars

class ExpertAnswer(ModalView):
    def init(self, board, time):
        self.board = board
        if time:
            self.exit_btn = False
        else:
            self.exit_btn = True

    def on_open(self):
        self.board.size_hint = [0.4, 0.4]
        self.board.pos = (0.35*self.width, 0.695*self.height)  # Not sure where to place this
        self.add_widget(self.board)

    def clean(self, instance=0):
        self.remove_widget(self.board)
        self.dismiss()

class HomeScreen(Screen):
    def btn_press_audio(self):
        if is_sound_enabled:
            button_press_sound.play()


class SettingsScreen(Screen):
    def enable_or_disable_audio(self):
        global is_sound_enabled
        if is_sound_enabled is True:
            is_sound_enabled = False
            self.ids.soundbutt.background_normal = "../Art/SOUNDOFF.png"
            self.ids.soundbutt.background_down = "../Art/SOUNDOFF_DOWN.png"
        else:
            is_sound_enabled = True
            self.ids.soundbutt.background_normal = "../Art/SOUND.png"
            self.ids.soundbutt.background_down = "../Art/SOUND_DOWN.png"

    def enable_or_disable_music(self):
        if background_music.state == "stop":
            background_music.play()
            self.ids.musicbutt.background_normal = "../Art/MUSIC.png"
            self.ids.musicbutt.background_down = "../Art/MUSIC_DOWN.png"
        else:
            background_music.stop()
            self.ids.musicbutt.background_normal = "../Art/MUSICOFF.png"
            self.ids.musicbutt.background_down = "../Art/MUSICOFF_DOWN.png"

    def open_empty(self):
        nofunctionality = NoFunctionality()
        nofunctionality.open()


class ShareScreen(Screen):

    def open_twitter(self):
        webbrowser.open("https://twitter.com/")

    def open_facebook(self):
        webbrowser.open("https://www.facebook.com/")

    def open_link(self):
        webbrowser.open("https://github.com/JAlexHouse/invertsquared")

    def open_instagram(self):
        webbrowser.open("https://www.instagram.com/")


class LevelScreen(Screen):
    pass


class MoreScreen(Screen):
    def open_empty(self):
        nofunctionality = NoFunctionality()
        nofunctionality.open()


class PauseScreen(Screen):
    pass


class Pause(ModalView):
    pass


class NoFunctionality(ModalView):
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
    timer = None
    gridlayout = None
    answerlayout = None
    button_ids = {}
    random = False
    resume = False
    game_tile_sound = None
    filename = ''
    level = None
    level_stars = 0
    stars = [0] * 20

    def on_enter(self):
        self.set_mode()
        self.set_level()
        if not self.resume:
            self.gridlayout = GridLayout(rows=self.rows, cols=self.cols)
            self.answerlayout = GridLayout(rows=self.rows, cols=self.cols)
            # generate answer key
            self.generate_answer()
            if self.game_mode != "Expert":
                self.answerlayout.size_hint = [0.3, 0.17]
                self.answerlayout.pos = (0.35*self.width, 0.695*self.height)
                self.add_widget(self.answerlayout)

            # generate game board
            self.generate_grid()
            self.gridlayout.size_hint = [0.75, 0.43]  # height, width
            self.gridlayout.pos = (0.13*self.width, 0.25*self.height)  # x, y
            self.add_widget(self.gridlayout)
            self.user_key = "0" * self.rows * self.cols

            self.resume = True
        if self.game_mode == "Expert":
            self.open_answer("init")
            self.answer_button = Button(background_normal="../Art/SHOWANS.png", background_down='../Art/SHOWANS_DOWN.png', size=(99.8, 67), size_hint=(None, None), pos=(430, 843))
            self.answer_button.bind(on_release=self.open_answer)
            self.add_widget(self.answer_button)
        else:
            self.hint_button = Button(background_normal="../Art/HINT.png", background_down='../Art/HINT_DOWN.png', size=(99.8, 67), size_hint=(None, None), pos=(430, 845))
            self.hint_button.bind(on_release=self.get_hint)
            self.add_widget(self.hint_button)

        self.game_tile_sound = SoundLoader.load('../Audio/GAME_TILE_PRESS.wav')

    def generate_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                button = Button(background_normal="../Art/TILE.png", background_down="../Art/TILE.png")
                button.bind(on_release=self.move_made)
                self.button_ids[button] = "{},{}".format(i, j)
                self.gridlayout.add_widget(button, len(self.gridlayout.children))

    def generate_answer(self):
        for _ in range(self.rows*self.cols):
            button = Button(background_normal="../Art/TILE.png", background_down="../Art/TILE.png")
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

        self.minimum_moves = self.answer_key.count("1")
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
        if grid.children[index].background_normal == "../Art/TILE_HINT.png":
            if grid.children[index].background_down == "../Art/TILE_DOWN.png":
                grid.children[index].background_normal = "../Art/TILE.png"
            else:
                grid.children[index].background_normal = "../Art/TILE_DOWN.png"
        elif grid.children[index].background_normal == "../Art/TILE.png" or grid.children[index].background_normal == "tile":
            grid.children[index].background_normal = "../Art/TILE_DOWN.png"
            grid.children[index].background_down = "../Art/TILE_DOWN.png"
        else:
            grid.children[index].background_normal = "../Art/TILE.png"
            grid.children[index].background_down = "../Art/TILE.png"

    def goal_reached(self):
        if self.user_key == self.answer_key:
            print("Yay, you won!")
            self.number_stars()
            self.open_won()
            self.clear_game()
        else:
            if self.game_mode != "Classic":
                self.ids.moves.text = "Moves Left: " + str(self.max_moves - self.moves_made)
                if self.moves_made == self.max_moves:
                    print("Oops, you lost!")
                    self.open_lost()
                    self.clear_game()
            else:
                self.ids.moves.text = "Moves Made: " + str(self.moves_made)

    def number_stars(self):
        intervals = 5
        if self.moves_made <= self.minimum_moves + intervals:
            self.level_stars = 3
        elif self.moves_made <= self.minimum_moves + intervals * 2:
            self.level_stars = 2
        else:
            self.level_stars = 1
        if self.game_mode == 'Classic':
            if self.stars[self.current_level[self.game_mode] - 1] < self.level_stars:
                self.stars[self.current_level[self.game_mode] - 1] = self.level_stars
            print("Number of stars:", sum(self.stars))

    def reset_board(self):
        self.moves_made = 0
        self.time_elapsed = 0
        self.user_key = "0" * self.rows * self.cols
        if self.game_mode == "Classic":
            self.ids.moves.text = "Moves Made: " + str(self.moves_made)
        else:
            self.ids.moves.text = "Moves Left: " + str(self.max_moves - self.moves_made)

        for tile in self.gridlayout.children:
            tile.background_normal = "../Art/TILE.png"
            tile.background_down = "../Art/TILE_DOWN.png"

    def clear_game(self):
        if self.game_mode == "Expert":
            self.remove_widget(self.answer_button)
        else:
            self.remove_widget(self.hint_button)

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
        if self.game_mode == "Expert":
            self.timer.cancel()
        #self.current_level[self.game_mode] = self.current_level[self.game_mode] + 1
        popup = GameWin()
        popup.set_stars(self.level_stars)
        popup.open()
        self.clear_game()

    def open_lost(self):
        if self.game_mode == "Expert":
            self.timer.cancel()
        popup = GameLose()
        popup.open()
        self.clear_game()

    # shows the answer for 5 seconds
    # need to change the color of the background or the tiles
    def open_answer(self, instance):
        self.answer = ExpertAnswer()
        if instance == "init":
            self.answer.init(self.answerlayout, True)
        else:
            self.answer.init(self.answerlayout, False)
        self.answer.open()

        if instance == "init":
            timer = Timer(5.0, self.answer.clean)
            timer.start()

    def get_hint(self, instance=0):
        #compare the user and answer key and the first place with a difference changes color for 2 seconds
        for i in range(self.rows*self.cols):
            if self.user_key[i] != self.answer_key[i]:
                self.hintloc = i
                break

        self.gridlayout.children[self.hintloc].background_normal = "../Art/TILE_HINT.png"
        timer = Timer(2.0, self.reverse_hint)
        timer.start()

    def reverse_hint(self):
        if self.gridlayout.children[self.hintloc].background_normal == "../Art/TILE_HINT.png":
            if self.gridlayout.children[self.hintloc].background_down == "../Art/TILE_DOWN.png":
                self.gridlayout.children[self.hintloc].background_normal = "../Art/TILE_DOWN.png"
            elif self.gridlayout.children[self.hintloc].background_down == "../Art/TILE.png":
                self.gridlayout.children[self.hintloc].background_normal = "../Art/TILE.png"

    def set_mode(self):
        app = App.get_running_app()
        self.game_mode = app.DIFFICULTY

        if app.STARTLEVEL:
            self.current_level[self.game_mode] = app.STARTLEVEL

        # Initialize what level we are on for each difficulty level
        if self.game_mode not in self.current_level:
            self.current_level[self.game_mode] = 1
        self.ids.moves.text = ""
        if self.game_mode == "Classic":
            self.filename = os.path.join(dirname, '../Levels/Classic.txt')
        elif self.game_mode == "Challenge":
            self.filename = os.path.join(dirname, '../Levels/Challenge.txt')
        elif self.game_mode == "Expert":
            self.filename = os.path.join(dirname, '../Levels/Expert.txt')
            self.start_timer()
        else:
            self.random = True

        with open(self.filename) as f:
            level_info = ""
            for i, line in enumerate(f):
                if i + 1 == self.current_level[self.game_mode]:
                    level_info = line
            # level data in the format col row answerkey
            level_info = level_info.rstrip('\n').split(' ')
            # if no more pre-determined level data, then set to randomized level generation
            self.random = level_info == ['']
            if self.random:
                # if randomized, set defaults (including time limit)
                rows, cols, time_limit = 3, 3, 15
                return
            elif self.game_mode == 'Expert':
                # if expert, set time limit too
                rows, cols, self.answer_key, time_limit = level_info
                self.time_limit = int(time_limit)

                #start timer after any last changes from reading level text files
                self.start_timer()
            else:
                rows, cols, self.answer_key = level_info
            self.rows = int(rows)
            self.cols = int(cols)
        

    def set_level(self):
        app = App.get_running_app()
        level_number = app.STARTLEVEL
        self.current_level[self.game_mode] = level_number
    
    def start_timer(self):
        if self.game_mode == 'Expert':  #MUST have this if statement here
<<<<<<< Updated upstream
            self.ids.extra_settings.text = str(self.time_limit - self.time_elapsed)
=======
            if self.timer:    # make sure only one timer is running at a time
                self.timer.cancel()
            self.ids.extra_settings.text = "Time Left: " + str(self.time_limit - self.time_elapsed)
>>>>>>> Stashed changes
            self.timer = Clock.schedule_interval(partial(self.timer_tick), 1)

    #update the timer every sec
    def timer_tick(self, *largs):
        self.time_elapsed += 1
        self.ids.extra_settings.text = "Time Left: " + str(self.time_limit - self.time_elapsed)
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
