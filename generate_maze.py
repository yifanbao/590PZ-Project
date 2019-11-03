"""
Generate Maze

"""
import random


class Maze:

    __marks = {
        'aisle': 0,
        'solution': 0.5,
        'wall': 1
    }

    def __init__(self, mode='easy'):
        if mode == 'easy':
            self.M = 21
            self.N = 41
            self.complexity = 2

        self.board = [[Maze.__marks['wall'] for _ in range(self.N)] for _ in range(self.M)]
        self.start_point = random.choice([
            (0, random.randint(0, (self.N - 2) // 2) * 2 + 1),
            (self.M - 1, random.randint(0, (self.N - 2) // 2) * 2 + 1),
            (random.randint(0, (self.M - 2) // 2) * 2 + 1, 0),
            (random.randint(0, (self.M - 2) // 2) * 2 + 1, self.N - 1)
        ])
        self.end_point = self.generate_path(self.start_point, True)
        for m in range(1, self.M - 1, 2):
            for n in range(1, self.N - 1, 2):
                if self.board[m][n] == Maze.__marks['wall']:
                    self.generate_path((m, n))

    def generate_path(self, start_point: tuple, is_solution=False) -> tuple:
        marks = Maze.__marks
        if is_solution:
            max_length = int(self.complexity * (self.M + self.N))
            target_mark = marks['solution']
            forbidden_mark = {target_mark}
        else:
            max_length = int(self.complexity * (self.M + self.N) / 5)
            target_mark = marks['aisle']
            forbidden_mark = set()

        m, n = start_point
        curt_length = 1

        def check_merging(_m, _n):
            if self.board[_m][_n] == marks['wall']:
                self.board[_m][_n] = target_mark
            else:
                for item in marks:
                    if item != 'wall':
                        forbidden_mark.add(marks[item])

        while curt_length < max_length:
            check_merging(m, n)
            neighbors = self.get_neighbors_coordinates(m, n, forbidden_mark)
            if not len(neighbors):
                break
            m_, n_ = random.choice(neighbors)
            m_in = (m + m_) // 2
            n_in = (n + n_) // 2
            check_merging(m_in, n_in)
            curt_length += 2
            m, n = m_, n_

        return m, n

    def get_neighbors_coordinates(self, m: int, n: int, forbidden_mark=None) -> list:
        neighbors = []
        if forbidden_mark is None:
            forbidden_mark = set()
        for m_, n_ in [(m - 2, n), (m + 2, n), (m, n - 2), (m, n + 2)]:
            if 0 < m_ < self.M \
                    and 0 < n_ < self.N \
                    and self.board[m_][n_] not in forbidden_mark \
                    and self.board[(m + m_) // 2][(n + n_) // 2] not in forbidden_mark:
                neighbors.append((m_, n_))
        return neighbors

    def print(self, show_solution=False):
        pass


if __name__ == '__main__':
    maze = Maze()
    maze.print()
