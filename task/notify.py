# -*- coding: utf-8 -*-
import datetime
from bson.objectid import ObjectId

from easycrawl.misc.emails import Email
from easycrawl.misc.store import quotesbotDB
# from task.celery import app
from tornado import template
from tenacity import retry, stop_after_attempt


notify_emails = ["chenyd@billbear.cn"]

#@app.task
def test(**kwargs):
    e = Email()
    e.sendhtml("test","<a>12</a>")


def get_template_string(path,**kwargs):
    with open(path, "rb") as f:
        data = f.read()
        t = template.Template(data)
        return t.generate(**kwargs)
    return ""


@retry(stop=stop_after_attempt(3))
def send_statistics_mail():
    items = quotesbotDB.quotebot.find().limit(10)
    content = get_template_string("../template/statistics.html", items=items, count=items.count())
    e = Email(send_list=notify_emails)
    subject = "【统计】实验数据（{}）".format(datetime.datetime.now())
    e.sendhtml(content=content, subject=subject)


if __name__ == '__main__':
    send_statistics_mail()