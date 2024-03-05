import os

from dotenv import load_dotenv
from kombu import Exchange, Queue

load_dotenv()

broker_connection_retry_on_startup = True
broker_url = os.environ["BROKER_URL"]

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "Europe/Warsaw"
enable_utc = True

task_queues = (
    Queue("speed", Exchange("speed")),
    Queue("destination", Exchange("destination")),
)

task_routes = {
    "process_speed": {"queue": "speed"},
    "process_destination": {"queue": "destination"},
}
