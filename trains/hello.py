import os

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world() -> str:
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    app_port = int(os.environ["APP_PORT"])
    app.run(host="0.0.0.0", port=app_port)
