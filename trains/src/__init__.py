import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()


app = Celery("train", broker=os.environ["BROKER_URL"])
app.autodiscover_tasks(["src"])
app.config_from_object("src.celeryconfig")

if __name__ == "__main__":
    app.start()
