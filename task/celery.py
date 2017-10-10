from __future__ import absolute_import
from celery import Celery, platforms

app = Celery('task', include=['task.execute'])

app.config_from_object('task.config')
platforms.C_FORCE_ROOT = True

if __name__ == '__main__':
    app.start()