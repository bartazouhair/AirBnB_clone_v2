#!/usr/bin/python3
"""web application must be listening on 0.0.0.0"""
from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def Hbnb():
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_text(text=None):
    sanitize = text.replace("_", " ")
    return f"C {sanitize}"


@app.route('/python', strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def p_text(text="is cool"):
    sanitize = text.replace("_", " ")
    return f"Python {sanitize}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
