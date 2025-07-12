import os
from time import sleep
from django.conf import settings

from celery import Celery
from celery.utils.log import get_task_logger

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")


app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

logger = get_task_logger(__name__)


@app.task(bind=True)
def debug_task(self) -> None:
    print(f"Request: {self.request!r}")


@app.task(bind=True)
def debug_task_returning(self, a: int) -> None:
    """Useful to see if the results backend is working."""
    for i in range(a):
        sleep(1)
        logger.info(f"Task at {i} loops")
        self.update_state(state="PROGRESS", meta={"process_percent": i * 10})
    logger.info(f"Task completed after {i} loops")
    return f"Task completed after {a} loops"
