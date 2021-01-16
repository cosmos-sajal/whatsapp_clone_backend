import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.secrets')
app = Celery()
app.conf.CELERY_ROUTES = {
    'worker.user.send_verification_email.send_verification_email':
        {'queue': 'send_verification_email'},
    'worker.user.send_otp_email.send_otp_email':
        {'queue': 'send_otp_email'},
    'worker.chat.onboard_user.onboard_user':
        {'queue': 'onboard_user'}
}

app.conf.update(settings.CELERY)
