import os

from src.create_app import create_app

app = create_app()

if __name__ == "__main__":
    app_port = int(os.environ["APP_PORT"])
    app.run(host="0.0.0.0", port=app_port)
