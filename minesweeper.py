from tkinter import *
from tkinter import ttk
import random


class Board:
    """
    Board class will set up the game board,
    performing tasks such as placing mines.
    Board will be 8x8 with 10 mines.
    """
    def __init__(self, window):
        self.window = window
        self.tile_matrix = [[0 for x in range(8)] for x in range(8)]
        self.mine_count = 10
        self.mine_location = []

    def form_board(self):
        """
        Create buttons for each tile
        """
        self.place_mines()
        self.fill_numbers()
        for column in range(0, 8):
            for row in range(0, 8):
                self.add_tile(column, row)
        global game
        game = Game(self.window, self.tile_matrix)
        #game.display_mines_remaining()

    def add_tile(self, col, row):
        """
        Compiles information to form a Tile object
        """
        count = 0
        # check self.tile_matrix for mine signifier
        if self.tile_matrix[col][row] == "m":
            is_mine = 1
        else:
            is_mine = 0
            count = self.tile_matrix[col][row]
        tile = Tile(self.window, col, row, is_mine, count)
        self.tile_matrix[col][row] = tile

    def place_mines(self):
        """
        Randomize x,y coordinates and marks which tiles
        should be mines
        """
        to_place = 10
        while to_place > 0:
            # random coordinate
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            # if coordinate not already a mine, mark as a mine
            if self.tile_matrix[y][x] != "m":
                to_place -= 1
                self.tile_matrix[y][x] = "m"

    def fill_numbers(self):
        """
        Finds the appropriate number to be displayed
        on clicked tiles
        """
        for col in range(8):
            for row in range(8):
                if self.tile_matrix[col][row] != "m":
                    self.tile_matrix[col][row] = self.count_adjacent_mines(col, row)

    def count_adjacent_mines(self, col, row):
        """
        Collects a count of mines touched by a tile.
        """
        count = 0
        if col < 7 and self.tile_matrix[col + 1][row] == "m":
            count += 1
        if col > 0 and self.tile_matrix[col - 1][row] == "m":
            count += 1
        if row < 7 and self.tile_matrix[col][row + 1] == "m":
            count += 1
        if row > 0 and self.tile_matrix[col][row - 1] == "m":
            count += 1
        if col < 7 and row < 7 and self.tile_matrix[col + 1][row + 1] == "m":
            count += 1
        if col < 7 and row > 0 and self.tile_matrix[col + 1][row - 1] == "m":
            count += 1
        if col > 0 and row < 7 and self.tile_matrix[col - 1][row + 1] == "m":
            count += 1
        if col > 0 and row > 0 and self.tile_matrix[col - 1][row - 1] == "m":
            count += 1
        return count

    def get_tile_matrix(self):
        return self.tile_matrix


class Game:
    """
    Main mechanics for player to use. Helps to keep
    Board updated after player action.
    """
    def __init__(self, window, tile_matrix):
        self.window = window
        self.tile_matrix = tile_matrix
        self.flags_placed = 10

    ### VERIFICATION ALGORITHM ###

    def tile_outcome(self, is_mine):
        if is_mine == 1:
            return self.game_over()
        self.check_win()

    def check_win(self):
        """
        Checks that all tiles are revealed or flagged
        """
        win = True
        for column in self.tile_matrix:
            for tile in column:
                if tile.flagged_or_revealed != 1:
                    win = False
        if win and self.flags_placed == 10:
            game_won = ttk.Label(self.window, text="YOU WIN!")
            game_won.grid(column=0, columnspan=8, row=len(self.tile_matrix)+1)
            game_won.configure(font=("Courier", 15, "bold"))

    ### END VERIFICATION ALGORITHM ###

    def game_over(self):
        for column in self.tile_matrix:
            for tile in column:
                tile.reveal_tile()
        game_over_label = ttk.Label(self.window, text="GAME OVER")
        game_over_label.grid(column=0, columnspan=8, row=len(self.tile_matrix)+1)
        game_over_label.configure(font=("Courier", 15, "bold"))

    def display_mines_remaining(self):
        mine_count_label = ttk.Label(self.window, text="Mines remaining: ")
        mine_count_label.grid(column=1, row=0)
        mine_number_label = ttk.Label(self.window, text=self.mines_remaining)
        mine_number_label.grid(column=2, row=0)

    def flag_placed(self):
        self.flags_placed += 1
        self.check_win()

    def flag_removed(self):
        self.flags_placed -= 1


class Tile:
    """
    Controls tile representations and tile status.
    """
    def __init__(self, window, column, row, is_mine, touching_mines):
        self.window = window
        self.text = StringVar()
        self.tile = Button(
            self.window,
            textvariable=self.text,
            command=lambda: self.reveal_and_check_tile(),
            height=1,
            width=2)
        self.tile.bind("<Button-3>", self.right_click)
        self.tile.bind("<Double-Button-3>", self.double_right)
        self.tile.grid(column=column, row=row+1)
        self.is_mine = is_mine   # 0 if not mine, 1 if mine
        self.touching_mines = touching_mines
        self.flagged_or_revealed = 0

    def reveal_and_check_tile(self):
        """Display either the mine, or the number
        of adjacent mines.
        Button is set to stay pressed"""
        if self.is_mine == 1:
            self.text.set("M")
        else:
            self.text.set(self.touching_mines)
        self.tile.config(relief=SUNKEN)
        self.flagged_or_revealed = 1
        game.tile_outcome(self.is_mine)

    def reveal_tile(self):
        if self.is_mine == 1:
            self.text.set("M")
        else:
            self.text.set(self.touching_mines)
        self.tile.config(relief=SUNKEN)

    def right_click(self, event):
        if self.tile["relief"] == SUNKEN:
            return
        self.text.set("F")
        self.flagged_or_revealed = 1
        game.flag_placed()
        game.check_win()

    def double_right(self, event):
        if self.tile["relief"] == SUNKEN:
            return
        self.text.set("")
        self.flagged_or_revealed = 0
        game.flag_removed()

"""
def main():
    window = Tk()
    window.title = "Minesweeper"
    start = Board(window)
    start.form_board()
    window.mainloop()


if __name__ == '__main__':
    main()
"""