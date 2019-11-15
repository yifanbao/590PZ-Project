from flask import Flask, render_template
import json

from generate_maze import Maze

app = Flask(__name__)


@app.route('/')
def init():
    marks = Maze.get_marks()
    maze = Maze()
    return render_template('game.html', maze=maze, marks=marks)


if __name__ == '__main__':
    app.run()
