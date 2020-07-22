from huey import crontab
from huey.contrib.djhuey import (
    db_periodic_task, db_task,
    periodic_task, task
)


@periodic_task(crontab(minute='*/1'))
def say_hello():
    print('Hello, this is a task')