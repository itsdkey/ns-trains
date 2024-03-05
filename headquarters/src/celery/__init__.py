import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()


app = Celery("headquarters", broker=os.environ["BROKER_URL"])
app.autodiscover_tasks(["src"])
app.config_from_object("src.celery.celeryconfig")
