import os
from time import sleep

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")


app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self) -> None:
    print(f"Request: {self.request!r}")


@app.task(bind=True)
def debug_task_returning(self, a: int) -> None:
    """Useful to see if the results backend is working."""
    for i in range(a):
        sleep(1)
        self.update_state(state="PROGRESS", meta={"process_percent": i * 10})
    return f"Task completed after {a} loops"
