import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.secrets')
app = Celery()
app.conf.CELERY_ROUTES = {
    'worker.user.send_verification_email.send_verification_email':
        {'queue': 'send_verification_email'},
}

app.conf.update(settings.CELERY)
