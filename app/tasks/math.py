from app.tasks.master import app


@app.task
def sum(x, y):
    return x + y


@app.task
def sub(x, y):
    return x - y
