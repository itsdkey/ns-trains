import os

from dotenv import load_dotenv

load_dotenv()

broker_connection_retry_on_startup = True
broker_url = os.environ["BROKER_URL"]

task_serializer = "json"
accept_content = ["json"]
timezone = "Europe/Warsaw"
enable_utc = True
task_acks_late = True
task_soft_time_limit = 30
task_time_limit = 60

beat_schedule = {
    "broadcast-train-speed": {
        "task": "broadcast_train_speed",
        "schedule": 10.0,
    },
    "broadcast-train-destination": {
        "task": "broadcast_train_destinations",
        "schedule": 180.0,
    },
}

task_routes = {
    "process_speed": {"queue": "speed"},
    "process_station": {"queue": "station"},
}
