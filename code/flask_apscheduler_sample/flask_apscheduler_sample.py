from flask import Flask, Response
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
import datetime
import uuid

# https://flask.palletsprojects.com/en/2.0.x/
app = Flask(__name__)


class Config(object):
    # https://viniciuschiele.github.io/flask-apscheduler/rst/configuration.html
    SCHEDULER_API_ENABLED = True


app.config.from_object(Config())

scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Taipei"))


def job(a):
    r = a ** a
    # 自己接後面DB 或其他 storage
    print(r)


@app.route("/")
def home():
    return "hi"


@app.route("/job/<int:number>")
def doing_job(number):
    scheduler.add_job(func=job, id=uuid.uuid4().hex, args=(number,),
                      next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=12))
    return Response(status=201)


if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    app.run()
