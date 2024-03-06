import os
from logging.config import fileConfig

from dotenv import load_dotenv
from kombu import Exchange, Queue

load_dotenv()

fileConfig("logging.ini")

broker_connection_retry_on_startup = True
broker_url = os.environ["BROKER_URL"]

task_serializer = "json"
accept_content = ["json"]
timezone = "Europe/Warsaw"
enable_utc = True
task_acks_late = True
task_soft_time_limit = 30
task_time_limit = 60

task_queues = (
    Queue("speed", Exchange("speed")),
    Queue("station", Exchange("station")),
)

task_routes = {
    "process_speed": {"queue": "speed"},
    "process_station": {"queue": "station"},
}
