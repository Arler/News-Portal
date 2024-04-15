from celery.schedules import crontab
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
	'send_weekly_email': {
		'task': 'posts.tasks.weekly_posts_email',
		'schedule': crontab(minute=0, hour=8, day_of_week='monday'),
		'args': (),
	}
}

app.autodiscover_tasks()