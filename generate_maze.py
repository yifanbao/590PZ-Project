"""
Generate Maze

"""
import random
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as pyplot
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


class Maze:
    __marks = {
        'aisle': 0,
        'solution': 0.4,
        'key': 0.5,
        'door': 0.55,
        'portal': 0.6,
        'portal_solution': 0.65,
        'start': 0.8,
        'end': 0.9,
        'wall': 1,
    }

    def __init__(self, mode='easy', num_rows=31, num_columns=41, complexity=0.5, num_portals=0, has_key=False):
        # set up board size and difficulty
        self.M = num_rows
        self.N = num_columns
        self.complexity = complexity
        self.num_portals = num_portals
        self.has_key = has_key
        if mode == 'easy':
            self.M = 31
            self.N = 41
            self.complexity = 0.6
            self.num_portals = 0
            self.has_key = True
        elif mode == 'median':
            self.M = 41
            self.N = 61
            self.complexity = 0.65
            self.num_portals = 1
            self.has_key = False
        elif mode == 'hard':
            self.M = 61
            self.N = 81
            self.complexity = 0.8
            self.num_portals = 1
            self.has_key = True
        else:
            if type(num_rows) != int or num_rows % 2 == 0 or num_rows <= 0:
                raise ValueError("Oops, the number of rows should be positive odd number")
            if type(num_columns) != int or num_columns % 2 == 0 or num_columns <= 0:
                raise ValueError("Oops, the number of columns should be positive odd number")
            if type(complexity) != float or complexity <= 0 or complexity >= 1:
                raise ValueError("Oops, the complexity should be more than 0 and less than 1")
            if type(num_portals) != int or num_portals < 0:
                raise ValueError("Oops, the number of portals should be non-negative integer")
            if type(has_key) != bool:
                raise ValueError("Oops, the has_key parameter should be a boolean")

        # initialize board
        self.board = [[Maze.__marks['wall'] for _ in range(self.N)] for _ in range(self.M)]
        self.solution_length = int(self.complexity * self.M * self.N / 8)
        self.solution = []
        self.start_point = None
        self.end_point = None

        self.portals = {}
        self.keys = []
        sequence = ['portal'] * self.num_portals
        if self.has_key:
            sequence += ['key']
            random.shuffle(sequence)
        sequence += ['end']

        self.generate_board(sequence)

    @staticmethod
    def get_marks():
        return Maze.__marks

    def generate_board(self, sequence: list):
        # randomly choose a start point on the outer border
        self.start_point = random.choice([
            (0, random.randint(0, (self.N - 2) // 2) * 2 + 1),
            (self.M - 1, random.randint(0, (self.N - 2) // 2) * 2 + 1),
            (random.randint(0, (self.M - 2) // 2) * 2 + 1, 0),
            (random.randint(0, (self.M - 2) // 2) * 2 + 1, self.N - 1)
        ])

        marks = Maze.__marks

        # generate solution according to the sequence
        start_point = self.start_point
        path_contain_key = False
        for i, item in enumerate(sequence):
            if item == 'key':
                path_contain_key = True
                continue
            max_length = (self.solution_length - len(self.solution)) / (len(sequence) - i)
            end_point = self.generate_path(start_point, is_solution=True, max_length=max_length)
            # add a pair of portals
            if item == 'portal':
                self.board[end_point[0]][end_point[1]] = marks['portal_solution']
                start_point = (
                    random.randint(0, (self.M - 2) // 2) * 2 + 1,
                    random.randint(0, (self.N - 2) // 2) * 2 + 1
                )
                while self.board[start_point[0]][start_point[1]] != marks['wall']:
                    start_point = (
                        random.randint(0, (self.M - 2) // 2) * 2 + 1,
                        random.randint(0, (self.N - 2) // 2) * 2 + 1
                    )
                self.portals[end_point] = start_point
                self.portals[start_point] = end_point
            elif item == 'end':
                self.end_point = end_point
            if path_contain_key:
                len_key_to_end = int(max_length // 2)
                m, n = self.solution[-len_key_to_end]
                self.board[m][n] = marks['key']
                self.keys.append((m, n))
                path_contain_key = False

        # mark special items on the board
        self.board[self.start_point[0]][self.start_point[1]] = marks['start']
        self.board[self.end_point[0]][self.end_point[1]] = marks['end']
        for m, n in self.portals:
            self.board[m][n] = marks['portal_solution']

        # generate branches from the solution path
        num_branches = int(len(self.solution) * self.complexity / 4)
        count_branches = 0
        branch_start_points = self.solution.copy()
        random.shuffle(branch_start_points)
        while count_branches < num_branches and len(branch_start_points):
            m, n = branch_start_points.pop()
            end = self.generate_path((m, n))
            if end != (-1, -1):
                count_branches += 1

        # fill the board
        for m in range(1, self.M - 1, 2):
            for n in range(1, self.N - 1, 2):
                if self.board[m][n] == marks['wall']:
                    self.generate_path((m, n), avoid_visited=False, max_length=self.solution_length, min_length=1)

    def generate_path(self, start_point: tuple, is_solution=False, avoid_visited=True, max_length=None, min_length=None) -> tuple:
        marks = Maze.__marks

        # reset if do not meet min length requirement
        initial_board = deepcopy(self.board)
        initial_solution = self.solution.copy()

        # set up default parameters
        if is_solution:
            max_length = max_length or self.solution_length
            min_length = min_length or int(max_length * 0.75)
            target_mark = marks['solution']
            forbidden_depth = 3
        else:
            max_length = max_length or int(self.solution_length * self.complexity / 3)
            min_length = min_length or int(max_length * 0.4)
            target_mark = marks['aisle']
            forbidden_depth = 1
        forbidden_mark = set()
        if avoid_visited:
            for item in marks:
                if item != 'wall':
                    forbidden_mark.add(marks[item])

        m, n = start_point
        curt_length = 0
        curt_path = set()

        # move one cell first if start from a border
        if start_point == self.start_point:
            self.board[m][n] = target_mark
            if m == 0:
                m += 1
            elif m == self.M - 1:
                m -= 1
            elif n == 0:
                n += 1
            else:
                n -= 1

        # generate path
        # move one step (two cells) each time, until meeting max length or no allowed movement
        while curt_length < max_length:
            # mark current cell
            if self.board[m][n] == marks['wall']:
                self.board[m][n] = target_mark
                curt_length += 1
                curt_path.add((m, n))
            if is_solution:
                self.solution.append((m, n))

            # get neighbors
            neighbors = self.get_neighbors_coordinates(m, n, curt_path, forbidden_mark, forbidden_depth)
            if not len(neighbors):
                break

            # choose a neighbor and break the wall in-between
            m_, n_ = random.choice(neighbors)
            self.board[(m + m_) // 2][(n + n_) // 2] = target_mark

            # if the neighbor is a wall, replicate the above operations for the neighbor
            if self.board[m_][n_] == marks['wall']:
                m, n = m_, n_
            # otherwise, update forbidden marks and find another neighbor for the current cell
            else:
                for item in marks:
                    if item != 'wall':
                        forbidden_mark.add(marks[item])
        if self.board[m][n] == marks['wall']:
            self.board[m][n] = target_mark

        # reset if do not meet min length requirement
        if curt_length < min_length:
            self.board = initial_board
            self.solution = initial_solution
            if is_solution:
                m, n = self.generate_path(start_point, is_solution, avoid_visited, max_length, min_length - 1)
            else:
                return -1, -1

        # return the coordinate of the last cell in current path
        return m, n

    def get_neighbors_coordinates(self, m: int, n: int, forbidden_cell=None, forbidden_mark=None, forbidden_depth=1) -> list:
        # set up default parameters
        if forbidden_cell is None:
            forbidden_cell = set()
        if forbidden_mark is None:
            forbidden_mark = set()

        # find neighbors with a step of 2
        neighbors = []
        for m_, n_ in [(m - 2, n), (m + 2, n), (m, n - 2), (m, n + 2)]:
            # skip invalid neighbors
            if not 0 < m_ < self.M or not 0 < n_ < self.N:
                continue
            if (m_, n_) in forbidden_cell:
                continue
            if forbidden_depth > 0 and self.board[m_][n_] in forbidden_mark:
                continue
            if forbidden_depth > 1 and not len(self.get_neighbors_coordinates(m_, n_, forbidden_cell, forbidden_mark, forbidden_depth - 1)):
                continue

            neighbors.append((m_, n_))

        return neighbors

    def print(self, show_solution=False):
        figure = pyplot.figure(figsize=(10, 5))
        viridis = pyplot.cm.get_cmap('viridis', 256)
        new_colors = viridis(np.linspace(0, 1, 256))
        pink = np.array([248 / 256, 24 / 256, 148 / 256, 1])
        new_colors[:25, :] = pink
        new_cmp = ListedColormap(new_colors)
        # pyplot.imshow(self.board, cmap=new_cmp, interpolation='nearest')
        pyplot.imshow(self.board, cmap=pyplot.cm.get_cmap('viridis_r', 256), interpolation='nearest')
        pyplot.xticks([]), pyplot.yticks([])
        figure.show()


if __name__ == '__main__':
    maze = Maze()
    maze.print()
