from src import app


@app.task
def broadcast_train_speed():
    return "random speed"


@app.task
def broadcast_train_destinations():
    return "random destonation"
