""" This modulme contains Sudoku game components."""

from os import listdir
from os.path import join
from random import choice


class Sudoku:

    """Sudoku game."""

    def __init__(self, *, mode="easy", puzzle={}):
        self.puzzle_path = None
        self.puzzle = puzzle
        if mode in ["easy", "medium", "hard"]:
            self.instanciate_fields()
            self.get_puzzle(mode)
            self.initialize()
        elif mode == "custom":
            self.instanciate_fields()
            if self.puzzle:
                self.initialize()

    def get_puzzle(self, mode):
        """Gets a random puzzle's path."""
        puzzles_path = f"assets/puzzles/{mode}/"
        puzzles = [
            puzzle for puzzle in listdir(puzzles_path) if puzzle.endswith(".txt")
        ]
        puzzle = choice(puzzles)
        self.puzzle_path = join(puzzles_path, puzzle)
        return

    def instanciate_fields(self):
        """Initialises necessary fields."""

        self.houses = {i: set() for i in range(1, 10)}
        self.rows = {i: dict() for i in range(1, 10)}
        self.cols = {i: dict() for i in range(1, 10)}
        self.cells = dict()
        self.value_counts = 0
        self.conflict_counts = 0
        self.revealed = set()

        # Initialises cells with their respective associations
        for row in range(1, 10):
            for col in range(1, 10):

                r = 1 if row in [1, 2, 3] else 2 if row in [4, 5, 6] else 3
                c = 1 if col in [1, 2, 3] else 2 if col in [4, 5, 6] else 3
                house = 3 * (r - 1) + c

                cell = Cell(row, col, house, 0)
                self.rows[row][col] = cell
                self.cols[col][row] = cell
                self.houses[house].add(cell)
                self.cells[(row, col)] = cell

    def initialize(self):
        """Initialises game cells with default values of puzzle from puzzle file or puzzle dictionary."""
        if self.puzzle:
            for location, value in self.puzzle.items():
                self.add_value(*location, value, 0)
        elif self.puzzle_path is not None:
            with open(self.puzzle_path) as puzzle:
                row_count = 1
                for row in puzzle.read().split("\n"):
                    col_count = 1
                    for cell in row.replace(" ", ""):
                        if cell != "#":
                            self.add_value(row_count, col_count, int(cell), 0)
                        col_count += 1
                    row_count += 1
        return

    def add_value(self, x, y, value=0, color=1):
        """Adds/updates value of the cell."""
        assert (
            type(x) == type(1) and type(y) == type(1) and type(value) == type(1)
        )  # Reconfirm this step after
        if not (0 < x < 10 and 0 < y < 10 and 0 <= value < 10):
            raise ValueError("Invalid Argument.")
        if self.cells[(x, y)].value == value:
            return
        if not self.cells[(x, y)].value and value:
            self.value_counts += 1
        self.cells[(x, y)].value = value
        self.cells[(x, y)].color = color
        self.revealed.add((x, y))
        self.update_conflicts(x, y)
        return

    def add_default_value(self, x, y, value):
        """Adds value of cell as a default value."""
        self.add_value(x, y, value, 0)

    def delete_value(self, x, y):
        """Deletes value of the cell."""
        if self.cells[(x, y)].color == 0:
            return
        self.add_value(x, y)
        self.value_counts -= 1
        self.revealed.discard((x, y))
        self.update_conflicts(x, y)
        return

    def update_conflicts(self, x, y):
        """Updates the conflict list of all cells related to the current cell."""

        cell = self.cells[(x, y)]
        before_update = cell.get_conflicts_count()

        for c in self.houses[cell.get_house()]:
            if cell.get_value() == c.get_value() and cell != c:
                cell.add_conflict(c)
                c.add_conflict(cell)
            else:
                cell.delete_conflict(c)
                c.delete_conflict(cell)

        for c in self.rows[cell.get_row()].values():
            if cell.get_value() == c.get_value() and cell != c:
                cell.add_conflict(c)
                c.add_conflict(cell)
            else:
                cell.delete_conflict(c)
                c.delete_conflict(cell)

        for c in self.cols[cell.get_col()].values():
            if cell.get_value() == c.get_value() and cell != c:
                cell.add_conflict(c)
                c.add_conflict(cell)
            else:
                cell.delete_conflict(c)
                c.delete_conflict(cell)
        after_update = cell.get_conflicts_count()
        self.conflict_counts += before_update - after_update
        return

    def check_goal_state(self):
        """Checks whether this state of the game is the goal."""
        if self.value_counts == 81 and self.conflict_counts == 0:
            return True
        return False

    def get_cell_conflicts(self, x, y):
        """Returns the conflicts of that cell."""
        return self.cells[(x, y)].get_conflicts()

    def get_cells(self):
        """Returns cells dictionary."""
        return self.cells

    def get_cell(self, x, y):
        """Returns the cell located at (x, y), where x is the row number and y is the column number."""
        return self.cells[(x, y)]

    def reset(self):
        """Resets the game with the default puzzle values."""
        self.instanciate_fields()
        self.initialize()


class Cell:

    """Sudoku Cell data structure."""

    def __init__(self, x, y, house, value):
        self.x = x
        self.y = y
        self.house = house
        self.value = value
        self.color = 1  # 0 for default cell, 1 for user cell, 2 for hint cell
        self.conflicts = set()

    def get_value(self):
        return self.value

    def get_color(self):
        return self.color

    def get_house(self):
        return self.house

    def get_row(self):
        return self.x

    def get_col(self):
        return self.y

    def get_house_conflicts(self):
        """Returns the conflicts present in the house of this cell."""
        house_conflicts = set()
        for conflict in self.conflicts:
            if self.house == conflict.get_house():
                house_conflicts.add(conflict)
        return house_conflicts

    def row_conflicts(self):
        """Returns the conflicts present in the row of this cell."""
        row_conflicts = set()
        for conflict in self.conflicts:
            if self.house == conflict.get_row():
                row_conflicts.add(conflict)
        return row_conflicts

    def col_conflicts(self):
        """Returns the conflicts present in the column of this cell."""
        col_conflicts = set()
        for conflict in self.conflicts:
            if self.house == conflict.get_col():
                col_conflicts.add(conflict)
        return col_conflicts

    def get_location(self):
        """Returns the location tuple (row, col) of this cell."""
        return (self.x, self.y)

    def get_conflits(self):
        """Returns the conflicts list of this cell."""
        return self.conflicts

    def get_conflicts_count(self):
        """Returns the conflict count."""
        return len(self.conflicts)

    def add_conflict(self, other):
        """Adds the other cell to conflict list."""
        if not isinstance(other, Cell):
            raise TypeError(
                f'Argument must be type "Cell" got instead type "{type(other)}".'
            )
        if self.value != 0 and other.value != 0:
            self.conflicts.add(other)
        return

    def delete_conflict(self, other):
        """Deletes the other cell from conflict list, if doesn't exist do nothing."""
        if not isinstance(other, Cell):
            raise TypeError(
                f'Argument must be type "Cell" got instead type "{type(other)}".'
            )
        self.conflicts.discard(other)
        return

    def __eq__(self, other):
        return self.value == other.value and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((str(self.x), str(self.y)))

    def __repr__(self):
        return f"Cell: (x, y) = ({self.x}, {self.y}) value = {self.value}"

    def __str__(self):
        return f"Cell: (x, y) = ({self.x}, {self.y}) value = {self.value}"
