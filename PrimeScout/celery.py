from __future__ import absolute_import, unicode_literals
import os
import celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','PrimeScout.settings')
app = celery.Celery('PrimeScout')
app.config_from_object(settings, namespace='CELERY')
app.conf.timezone = 'America/New_York'
app.autodiscover_tasks()
