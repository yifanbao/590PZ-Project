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
        'portal': 0.6,
        'portal_solution': 0.65,
        'start': 0.8,
        'end': 0.9,
        'wall': 1
    }

    def __init__(self, mode='easy'):
        # TODO: Add default settings for different modes
        # set up board size and difficulty
        num_portals = 0
        if mode == 'easy':
            self.M = 31
            self.N = 41
            self.complexity = 0.5
            num_portals = 1

        # initialize board
        self.board = [[Maze.__marks['wall'] for _ in range(self.N)] for _ in range(self.M)]
        self.solution_length = int(self.complexity * self.M * self.N / 8)
        self.solution = []
        self.start_point = None
        self.end_point = None

        # TODO: Initial setup for doors & keys
        self.portals = {}
        self.doors_keys = {}
        sequence = ['portal'] * num_portals + ['end']

        self.generate_board(sequence)

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
        for i, item in enumerate(sequence):
            max_length = (self.solution_length - len(self.solution)) / (len(sequence) - i)
            end_point = self.generate_path(start_point, is_solution=True, max_length=max_length)
            # add a pair of portals
            if item == 'portal':
                self.board[end_point[0]][end_point[1]] = marks['portal']
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
            # TODO: Add key & door
            elif item == 'key':
                pass
            elif item == 'door':
                pass
            # add an end point
            elif item == 'end':
                self.end_point = end_point
                break

        # mark special items on the board
        self.board[self.start_point[0]][self.start_point[1]] = marks['start']
        self.board[self.end_point[0]][self.end_point[1]] = marks['end']
        for m, n in self.portals:
            self.board[m][n] = marks['portal']

        # generate branches from the solution path
        for i in range(int(self.complexity * len(self.solution) / 4)):
            m, n = random.choice(self.solution)
            end = self.generate_path((m, n))
            while end == (-1, -1):
                m, n = random.choice(self.solution)
                end = self.generate_path((m, n))

        # fill the board
        for m in range(1, self.M - 1, 2):
            for n in range(1, self.N - 1, 2):
                if self.board[m][n] == marks['wall']:
                    self.generate_path((m, n), avoid_visited=False, min_length=1)

    def generate_path(self, start_point: tuple, is_solution=False, avoid_visited=True, max_length=None, min_length=None) -> tuple:
        initial_board = deepcopy(self.board)
        initial_solution = self.solution.copy()
        marks = Maze.__marks
        if is_solution:
            max_length = max_length or self.solution_length
            min_length = min_length or int(max_length * 0.75)
            target_mark = marks['solution']
            forbidden_depth = 3
        else:
            max_length = max_length or int(self.solution_length * self.complexity / 3)
            min_length = min_length or int(max_length * 0.5)
            target_mark = marks['aisle']
            forbidden_depth = 1
        forbidden_mark = set()
        if avoid_visited:
            for item in marks:
                if item != 'wall':
                    forbidden_mark.add(marks[item])

        m, n = start_point
        curt_length = 0

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

        while curt_length < max_length:
            if self.board[m][n] == marks['wall']:
                self.board[m][n] = target_mark
            else:
                for item in marks:
                    if item != 'wall':
                        forbidden_mark.add(marks[item])
            curt_length += 1
            if is_solution:
                self.solution.append((m, n))

            neighbors = self.get_neighbors_coordinates(m, n, forbidden_mark, forbidden_depth)
            if not len(neighbors):
                break
            m_, n_ = random.choice(neighbors)
            self.board[(m + m_) // 2][(n + n_) // 2] = target_mark
            m, n = m_, n_
        if self.board[m][n] == marks['wall']:
            self.board[m][n] = target_mark

        if curt_length < min_length:
            self.board = initial_board
            self.solution = initial_solution
            if is_solution:
                m, n = self.generate_path(start_point, is_solution, avoid_visited, max_length, min_length)
            else:
                return -1, -1

        return m, n

    def get_neighbors_coordinates(self, m: int, n: int, forbidden_mark=None, forbidden_depth=1) -> list:
        neighbors = []
        if forbidden_mark is None:
            forbidden_mark = set()
        for m_, n_ in [(m - 2, n), (m + 2, n), (m, n - 2), (m, n + 2)]:
            if not 0 < m_ < self.M or not 0 < n_ < self.N:
                continue
            if forbidden_depth > 0 and self.board[m_][n_] in forbidden_mark:
                continue
            if forbidden_depth > 1 and not len(self.get_neighbors_coordinates(m_, n_, forbidden_mark, forbidden_depth - 1)):
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
