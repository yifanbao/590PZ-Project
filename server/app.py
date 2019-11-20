from flask import Flask, render_template
import json

from generate_maze import Maze

app = Flask(__name__)


@app.route('/<string:mode>')
def init(mode):
    mode = mode or 'easy'
    marks = Maze.get_marks()
    maze = Maze(mode=mode)
    return render_template('game.html', maze=maze, marks=marks, columns=str(len(maze.board[0])))


if __name__ == '__main__':
    app.run()
