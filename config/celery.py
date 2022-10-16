import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-monday-morning': {
        'task': 'api.tasks.additional_task',
        'schedule': crontab(hour=0, minute=0)
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
