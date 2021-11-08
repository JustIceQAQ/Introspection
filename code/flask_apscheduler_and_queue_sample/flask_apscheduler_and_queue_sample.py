from flask import Flask, Response
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
import uuid
import queue

app = Flask(__name__)

# https://docs.python.org/3/library/queue.html
q = queue.Queue()


class Config(object):
    # https://viniciuschiele.github.io/flask-apscheduler/rst/configuration.html
    SCHEDULER_API_ENABLED = True


app.config.from_object(Config())

# https://github.com/viniciuschiele/flask-apscheduler
# https://apscheduler.readthedocs.io/en/3.x/userguide.html
scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Taipei"))


def job():
    if q.empty():
        pass
    else:
        data = q.get()
        print(data ** data)
        # 自己接後面DB 或其他 storage


@app.route("/")
def home():
    return "hi"


@app.route("/job/<int:number>")
def doing_job(number):
    q.put(number)
    return Response(status=201)


if __name__ == '__main__':

    scheduler.init_app(app)
    scheduler.start()
    # set 5 worker
    for _ in range(5):
        scheduler.add_job(func=job, id=uuid.uuid4().hex, trigger='cron', second='*/1')
    app.run()
