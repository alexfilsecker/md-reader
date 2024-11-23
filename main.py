import eventlet

eventlet.monkey_patch()

import os  # noqa: E402
import time  # noqa: E402
from threading import Thread  # noqa: E402

from flask import Flask, render_template  # noqa: E402
from flask_socketio import SocketIO  # noqa: E402

app = Flask(__name__)
socket = SocketIO(app)


@app.route("/")
def home():
    return render_template("index.html")


def read_markdown(path: str) -> str:
    with open(path, "r") as f:
        text = f.read()

    return text


@socket.on("connect")
def init_socket():
    html = read_markdown("./README.md")
    return socket.emit("file_changed", html)


def is_file_changed(path: str) -> bool:
    past_mod = os.path.getmtime(path)
    time.sleep(1)
    new_mod = os.path.getmtime(path)
    return new_mod > past_mod


def watch(path: str, socket: SocketIO):
    while True:
        if is_file_changed(path):
            print("file changed")
            html = read_markdown(path)
            socket.emit("file_changed", html)


if __name__ == "__main__":
    Thread(target=watch, args=("./README.md", socket), daemon=True).start()
    socket.run(app)
