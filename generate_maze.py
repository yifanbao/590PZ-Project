"""
Generate Maze

"""
import random


class Maze:

    __symbols = {
        'aisle': 0,
        'solution': 0.5,
        'wall': 1
    }

    def __init__(self, mode='easy'):
        if mode == 'easy':
            self.M = 21
            self.N = 41
            self.complexity = 2

        self.board = [[Maze.__symbols['wall'] for _ in range(self.N)] for _ in range(self.M)]
        self.start_point = random.choice([
            (0, random.randint(0, self.N - 1)),
            (self.M - 1, random.randint(0, self.N - 1)),
            (random.randint(0, self.M - 1), 0),
            (random.randint(0, self.M - 1), self.N - 1)
        ])
        self.end_point = self.generate_path(self.start_point, True)
        for m in range(1, self.M - 1, 2):
            for n in range(1, self.N - 1, 2):
                if self.board[m][n] == Maze.__symbols['wall']:
                    self.generate_path((m, n))

    def generate_path(self, start_point: tuple, is_solution=False) -> tuple:
        pass

    def print(self, show_solution=False):
        pass


if __name__ == '__main__':
    maze = Maze()
    maze.print()
