#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from celery.schedules import crontab

CELERY_TIMEZONE = 'Asia/Shanghai'

from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'add-every-5-minutes': {
         'task': 'task.execute.crawel',
         'schedule': timedelta(seconds= 60 * 5 ),
         'args': ()
    }
}

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
BROKER_URL = 'redis://127.0.0.1:6379/2'


