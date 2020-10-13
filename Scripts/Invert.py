from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.widget import Widget

# creating .py class (inherently calls on .kv class)
class HomeScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class PlaySetScreen(Screen):
    pass

class PlayScreen(Screen):
    rows = 5
    cols = 5
    gridlayout = GridLayout(rows=rows, cols=cols)
    gridgenerated = False
    button_ids = {}
    
    def on_enter(self):
        if self.gridgenerated:
            return
        self.generate_grid()
        self.gridlayout.size_hint = [.75, .75]
        self.gridlayout.pos = (self.width/8, self.height/8)
        self.add_widget(self.gridlayout)
        self.gridgenerated = True

    def generate_grid(self, cols = 5, rows = 5):
        for i in range(rows):
            for j in range(cols):
                button = Button(text="{},{}".format(i, j), background_color=(0,0,0,1))
                button.bind(on_press = self.move_made)
                self.button_ids[button] = "{},{}".format(i, j);
                self.gridlayout.add_widget(button, len(self.gridlayout.children))
    
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

    def get_index_by_tile_id(self, col, row):
        return row * self.cols + col

    def change_tile_color(self, index):
        if self.gridlayout.children[index].background_color == [255,255,255,1]:
                self.gridlayout.children[index].background_color = [0,0,0,1]
        else:
            self.gridlayout.children[index].background_color = [255,255,255,1]
    
    def clear_game(self):
        for tile in self.gridlayout.children:
            tile.background_color = [0,0,0,1]

class ScreenManager(ScreenManager):
    def build(self):
        return

# app class; runs the app
class InvertApp(App):
    def build(self):
        return Builder.load_file('Invert.kv')

if __name__ == '__main__':
    InvertApp().run()
