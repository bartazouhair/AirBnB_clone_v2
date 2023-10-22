#!/usr/bin/python3
"""web application must be listening on 0.0.0.0"""
from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from models.city import City


app = Flask(__name__)


@app.teardown_appcontext
def tear_down(self):
    storage.close()


@app.route('/states', strict_slashes=False)
def states():
    """Cities by States"""
    states = storage.all(State).values()
    return render_template('9-states.html', states=states, mode="work")


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """Display HTML page with the list of cities of a state"""
    states = storage.all("State").values()
    for state in states:
        if state.id == id:
            return render_template('9-states.html', state=state)
    return render_template('9-states.html', not_found=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
