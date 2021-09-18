""" This module contains Sudoku AI components. """

from random import choice
from copy import deepcopy


class SudokuAI:

    """Sudoku AI for Hints and Solving using "Maintaining Arc Consistency Algorithm"."""

    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.domains = {
            (i, j): set(k for k in range(1, 10))
            for i in range(1, 10)
            for j in range(1, 10)
        }
        self.initial_moves = set(
            (cell[0], cell[1])
            for cell in self.sudoku.cells.keys()
            if self.sudoku.cells[cell].value != 0
        )

    def solve(self):
        """Solves the problem and returns the solution as a dictionary."""
        assignment = dict()
        arcs_list = []
        for var in self.initial_moves:
            assignment[var] = self.sudoku.cells[var].value
            self.domains[var] = {self.sudoku.cells[var].value}
            arcs = [(neighbor, var) for neighbor in self.neighbors(*var)]
            arcs_list.extend(arcs)
        self.ac3(arcs_list)
        self.solution = self.backtrack(assignment)
        return self.solution

    def neighbors(self, x: int, y: int):
        """Returns the neighbors of the cell."""
        rows = set((x, i) for i in range(1, 10))
        cols = set((j, y) for j in range(1, 10))
        a = (1, 2, 3) if x in (1, 2, 3) else (4, 5, 6) if x in (4, 5, 6) else (7, 8, 9)
        b = (1, 2, 3) if y in (1, 2, 3) else (4, 5, 6) if y in (4, 5, 6) else (7, 8, 9)
        houses = set((i, j) for i in a for j in b)
        neighbors = rows.union(cols).union(houses)
        neighbors.remove((x, y))
        return neighbors

    def hint(self):
        """Returns a random (location, value) pair for an unassigned cell or a wrongly assigned cell."""
        unassigned_vars = list(set(self.solution.keys()) - self.sudoku.revealed)
        if unassigned_vars:
            hint_var = choice(unassigned_vars)
        else:
            wrong_assigned_vars = [
                (i, j)
                for i in range(1, 10)
                for j in range(1, 10)
                if self.sudoku.cells[(i, j)].value != self.solution[(i, j)]
            ]
            hint_var = choice(wrong_assigned_vars)
        hint = self.solution[hint_var]
        return hint_var, hint

    def revise(self, neighbor, var):
        """Revises neighbor's domain according to var value. Returns True if revised False otherwise."""
        revised = False
        to_remove = []
        for val in self.domains[neighbor]:
            consistent = False
            for var_val in self.domains[var]:
                if val != var_val:
                    consistent = True
                    break
            if not consistent:
                to_remove.append(val)
        if to_remove:
            revised = True
        for val in to_remove:
            self.domains[neighbor].remove(val)
        return revised

    def ac3(self, arcs):
        """Make domain values arc consistent with the assignment."""
        while len(arcs):
            neighbor, var = arcs.pop(0)
            if self.revise(neighbor, var):
                if not len(self.domains[var]):
                    return False
                for z in self.neighbors(*neighbor) - {var}:
                    if (z, neighbor) not in arcs:
                        arcs.append((z, neighbor))
        return True

    def order_domain_values(self, var, assignment):
        """Returns domain values of the var ordered with priority."""
        variables = self.neighbors(*var) - (
            set(self.sudoku.cells.keys()) - assignment.keys() - {var}
        )
        values = []
        for val in self.domains[var]:
            count = 0
            for variable in variables:
                if val in self.domains[variable]:
                    count += 1
            values.append((val, count))
        values.sort(key=lambda x: x[1])
        values = [value[0] for value in values]
        return values

    def select_unassigned_variable(self, assignment):
        """Returns an unassigned variable selected with priority."""
        variables = set(self.sudoku.cells.keys()) - set(assignment.keys())
        variables_list = []
        for var in variables:
            variables_list.append((var, len(self.domains[var])))
        return min(variables_list, key=lambda x: x[1])[0]

    def assignment_complete(self, assignment):
        """Checks whether the assignment is complete."""
        return len(assignment) == 81

    def consistent(self, assignment):
        """Checks whether the assignment is consistent."""
        rows = [[set(), 0] for i in range(1, 10)]
        cols = [[set(), 0] for i in range(1, 10)]
        houses = [[set(), 0] for i in range(1, 10)]
        for var in assignment.keys():
            rows[self.sudoku.cells[var].x - 1][0].add(assignment[var])
            rows[self.sudoku.cells[var].x - 1][1] += 1
            cols[self.sudoku.cells[var].y - 1][0].add(assignment[var])
            cols[self.sudoku.cells[var].y - 1][1] += 1
            houses[self.sudoku.cells[var].house - 1][0].add(assignment[var])
            houses[self.sudoku.cells[var].house - 1][1] += 1
        for val, length in rows:
            if len(val) != length:
                return False
        for val, length in cols:
            if len(val) != length:
                return False
        for val, length in houses:
            if len(val) != length:
                return False
        return True

    def backtrack(self, assignment):
        """Backtracking Search interleaved with Arc consistency."""
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        domain_values = deepcopy(self.domains)
        for val in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = val
            if self.consistent(new_assignment):
                arcs = [
                    (neighbor, var)
                    for neighbor in self.neighbors(*var) - new_assignment.keys()
                ]
                self.domains[var] = {val}
                if self.ac3(arcs):
                    result = self.backtrack(new_assignment)
                    if result:
                        return result
                self.domains = domain_values
        return None
