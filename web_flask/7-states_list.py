#!/usr/bin/python3
"""web application must be listening on 0.0.0.0"""
from flask import Flask
from flask import render_template
from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def tear_down(self):
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    states = list(storage.all("State").values())
    states.sort(key=lambda x: x.name)
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
