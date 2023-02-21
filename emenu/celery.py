import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emenu.settings')

app = Celery('emenu')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
