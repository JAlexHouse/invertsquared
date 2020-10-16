from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.core.window import Window

Window.size = (540, 960)

from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
import random


# creating .py class (inherently calls on .kv class)
#alphabetical order ish
class GameOverScreen(Screen):
    pass

class GameWinScreen(Screen):
    pass

class HomeScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


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
    rows = 2
    cols = 2
    gridlayout = GridLayout(rows=rows, cols=cols)
    answerlayout = GridLayout(rows=rows, cols=cols, spacing = 2)
    button_ids = {}
    random= True
    resume=False
    gridgenerated=False

    def on_enter(self):
        if not self.resume:
            # generate answer key
            self.generate_answer()
            self.answerlayout.size_hint = [.2, .2]
            self.answerlayout.pos = (0, 0)  # Not sure where to place this
            with self.answerlayout.canvas.before:
                Color(.5, .5, .5, 1)
                self.rect = Rectangle(size=[.2 * self.width + 2, .2 * self.height + 2], pos=self.answerlayout.pos)
            self.add_widget(self.answerlayout)
            self.resume = True
        if not self.gridgenerated:
            #generate game board
            self.generate_grid()
            self.gridlayout.size_hint = [.5, .5]
            self.gridlayout.pos = (self.width/4, self.height/4)
            self.add_widget(self.gridlayout)
            self.gridgenerated=True



    def generate_grid(self):
        self.gridlayout = GridLayout(rows=self.rows, cols=self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                button = Button(text="{},{}".format(i, j), background_color=(0,0,1,1))
                button.bind(on_press = self.move_made)
                self.button_ids[button] = "{},{}".format(i, j)
                self.gridlayout.add_widget(button, len(self.gridlayout.children))

    def generate_answer(self):
        self.answerlayout = GridLayout(rows=self.rows, cols=self.cols, spacing=2)  # Reset it
        if random:
            for i in range(self.rows):
                for j in range(self.cols):
                    button = Button()
                    color = random.randint(0, 1)
                    if color:
                        button.background_color=(0,0,1,1)
                    else:
                        button.background_color=(255,255,255,1)
                    button.disabled = True
                    button.background_disabled_down=''
                    button.background_disabled_normal=''
                    self.answerlayout.add_widget(button, len(self.answerlayout.children))

    def move_made(self, instance):
        row, col = (int(d) for d in self.button_ids[instance].split(','))
        index = self.get_index_by_tile_id(col, row)

        self.change_tile_color(index)
        print("Pressed button {},{}".format(row, col))

        #check if NOT top row
        if (row < self.rows - 1):
            top_index = self.get_index_by_tile_id(col, row+1)
            self.change_tile_color(top_index)
        #check if NOT bottom row
        if (row > 0):
            bottom_index = self.get_index_by_tile_id(col, row-1)
            self.change_tile_color(bottom_index)
        #check if NOT left column
        if (col < self.cols - 1):
            left_index = self.get_index_by_tile_id(col+1, row)
            self.change_tile_color(left_index)
        #check if NOT right column
        if (col > 0):
            right_index = self.get_index_by_tile_id(col-1, row)
            self.change_tile_color(right_index)

        self.goal_reached()

    def get_index_by_tile_id(self, col, row):
        return row * self.cols + col

    def change_tile_color(self, index):
        if self.gridlayout.children[index].background_color == [255,255,255,1]:
                self.gridlayout.children[index].background_color = [0,0,1,1]
        else:
            self.gridlayout.children[index].background_color = [255,255,255,1]


    def goal_reached(self):
        for i in range(self.cols):
            for j in range(self.rows):
                index=self.get_index_by_tile_id(i, j)
                print(index)
                if self.gridlayout.children[index].background_color != self.answerlayout.children[index].background_color:
                    return
        print("Yay, won")
        app.root.current="GameWin"
        self.clear_game()


    def reset_board(self):
        for tile in self.gridlayout.children:
            tile.background_color = [0,0,1,1]
    
    def clear_game(self):
        self.reset_board()
        self.remove_widget(self.answerlayout)
        self.resume=False
        self.remove_widget(self.gridlayout)
        self.gridgenerated=False

    def open_pause(self):
        popup = Pause()
        popup.open()

class ScreenManager(ScreenManager):
    def build(self):
        return

# app class; runs the app
class InvertApp(App):
    def build(self):
        pass
    #the previous call to include file caused a widget error

if __name__ == '__main__':
    app=InvertApp()
    app.run()
