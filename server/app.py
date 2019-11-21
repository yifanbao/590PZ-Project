from flask import Flask, render_template, redirect

from generate_maze import Maze

app = Flask(__name__)


@app.route('/')
def to_init():
    return redirect('/easy')


@app.route('/<string:mode>')
def init(mode):
    marks = Maze.get_marks()
    maze = Maze(mode=mode)
    columns = len(maze.board[0])

    def parse_position(m, n):
        return m * columns + n

    position = parse_position(*maze.start_point)
    portals = maze.portals
    parsed_portals = {}
    for key in portals.keys():
        parsed_portals[parse_position(*key)] = parse_position(*portals[key])

    return render_template('game.html', marks=marks, maze=maze, columns=str(columns), position=position, portals=parsed_portals)


if __name__ == '__main__':
    app.run()
