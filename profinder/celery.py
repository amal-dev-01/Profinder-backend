from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "profinder.settings")
app = Celery("adminpanel")

app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule ={
    'send_mail_every_day':{
        'task':'adminpanel.tasks.send_mail_func',
        # 'schedule':crontab(hour=13,minute=45)
        'schedule':crontab(hour=15,minute=32),

        # 'schedule': crontab(day_of_month=27, hour=0, minute=1),

        
    },
    'block_professional_due_payment':{
        'task':'adminpanel.tasks.over_due_block',
        'schedule':crontab(
                hour=15,
                minute=34,
                # day_of_month='*',
                # month_of_year='*',
            )
    }
}


app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")



# celery -A profinder.celery worker --pool=solo -l INFO
# celery -A profinder.celery beat -l INFO