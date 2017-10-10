import time
import os
from bson.objectid import ObjectId
import crawelbank.models as models
import crawelbank.modules as modules
import crawelbank.modules.notify
import crawelbank.models.mongo
from task.celery import  app
from tornado import  template
from datetime import datetime
from tenacity import retry
from tenacity import stop_after_attempt

notify_emails = ["gut@billbear.cn","ruant@billbear.cn","kutaa@billbear.cn"]
notify_emails = []

@app.task
def test(**kwargs):
    e = modules.notify.Email()
    e.sendhtml("test","<a>12</a>")

def get_template_string(path,**kwargs):
    with open(path, "rb") as f:
        data = f.read()
        t = template.Template(data)
        return t.generate(**kwargs)
    return ""

#@retry(stop=stop_after_attempt(3))
def send_404_pages_mail():

    conn = crawelbank.models.mongo.create_mongodb()
    dainslef_db = conn.get_database("dainslef")
    db = conn.get_database("crawelbank")
    act_compare_notify_cc = db.get_collection("act_compare_notify")
    act_cc = dainslef_db.get_collection("act")
    act_compare_cc = db.get_collection("act_compare")

    p_404_pages = act_compare_notify_cc.find({
        '404_notify': True
    })

    print("###start send_404_pages_mail:",p_404_pages.count())
    if p_404_pages.count() > 0:
        act_datas = []
        for page in p_404_pages:
            id = page['_id']
            act_data = act_cc.find_one({'_id':id})
            if not act_data:
                act_data = {}
            act_data_compare = act_compare_cc.find_one({'_id': id})
            act_data['crawel_time'] = 0
            status_right = act_data.get('status') == 50
            if 'crawel_time' in act_data_compare:
                t = datetime.fromtimestamp(act_data_compare['crawel_time'])
                act_data['crawel_time'] = t.strftime('%Y-%m-%d %H:%M:%S')

            if status_right:
                act_datas.append(act_data)

        content = get_template_string("template/404.html",act_datas=act_datas, count=len(act_datas))
        e = modules.notify.Email(send_list=notify_emails)
        subject = "【统计】检测到活动原文链接404（{}）".format(datetime.now())
        e.sendhtml(content=content, subject=subject)

        act_compare_notify_cc.remove({
            '404_notify':True
        })


def send_offline_page_mail():

    conn = crawelbank.models.mongo.create_mongodb()
    db = conn.get_database("crawelbank")
    dainslef_db = conn.get_database("dainslef")
    act_compare_notify_cc = db.get_collection("act_compare_notify")
    act_cc = dainslef_db.get_collection("act")
    act_compare_cc = db.get_collection("act_compare")

    pages = act_compare_notify_cc.find({
        'offline_notify': True
    })

    print("###start send_offline_page_mail:",pages.count())
    if pages.count() > 0:
        act_datas = []
        for page in pages:
            id = page['_id']
            act_data = act_cc.find_one({'_id':id})
            if not act_data:
                act_data = {}
            act_data_compare = act_compare_cc.find_one({'_id': id})
            if act_data_compare:
                act_data['crawel_time'] = 0
                status_right = act_data.get('status') == 50
                if 'crawel_time' in act_data_compare:
                    t = datetime.fromtimestamp(act_data_compare['crawel_time'])
                    act_data['crawel_time'] = t.strftime('%Y-%m-%d %H:%M:%S')

                if status_right:
                    act_datas.append(act_data)

        print("#### act_datas:",act_datas)
        if act_datas:
            content = get_template_string("template/offline.html",act_datas=act_datas, count=len(act_datas))
            e = modules.notify.Email(send_list=notify_emails)
            subject = "【统计】已经下线的商品（{}）".format(datetime.now())
            e.sendhtml(content=content, subject=subject)

        act_compare_notify_cc.remove({
            'offline_notify':True
        })

#@retry(stop=stop_after_attempt(3))
def send_diffence_pages_mail():
    conn = crawelbank.models.mongo.create_mongodb()
    dainslef_db = conn.get_database("dainslef")
    db = conn.get_database("crawelbank")
    act_compare_notify_cc = db.get_collection("act_compare_notify")
    act_cc = dainslef_db.get_collection("act")
    act_compare_cc = db.get_collection("act_compare")
    p_diffence_pages = act_compare_notify_cc.find({
        'diffence_notify':True
    })

    print("###send_diffence_pages_mail len(p_diffence_pages) : %s " % p_diffence_pages.count())
    if p_diffence_pages.count() > 0:
        act_datas = []
        for page in p_diffence_pages:
            id = page['_id']
            #print "#find id:",id
            act_data = act_cc.find_one({'_id': id})
            act_data_compare = act_compare_cc.find_one({'_id': id},{'content':False,'last_content':False})
            if act_data and act_data_compare:
                #act_data = act_data.update(act_data_compare)
                act_data['difference'] = act_data_compare['difference']
                if 'image_difference' in act_data_compare:
                    act_data['image_difference'] = act_data_compare['image_difference']
                else:
                    act_data['image_difference'] = 1.0
                act_data['crawel_time'] = 0
                status_right = act_data.get('status') == 50
                if 'crawel_time' in act_data_compare:
                    t = datetime.fromtimestamp(act_data_compare['crawel_time'])
                    act_data['crawel_time'] = t.strftime('%Y-%m-%d %H:%M:%S')

                if status_right:
                    act_datas.append(act_data)
                #print "####act_data:",act_data

        if act_datas:
            #print "###update diffenerce page act:", act_data
            content = get_template_string("template/diffenerce.html", act_datas = act_datas, count=len(act_datas))

            e = modules.notify.Email(send_list=notify_emails)
            subject = "【统计】检测到活动原文链接内容变化（{}）".format(datetime.now())
            e.sendhtml(content=content, subject=subject)

        ret = act_compare_notify_cc.remove({
            'diffence_notify':True
        })
        print("### remove act_compare_notify_cc")



@retry(stop=stop_after_attempt(3))
def send_file_change_mail():

    conn = crawelbank.models.mongo.create_mongodb()
    db = conn.get_database("crawelbank")
    dainslef_db = conn.get_database("dainslef")
    act_compare_notify_cc = db.get_collection("act_compare_notify")
    act_cc = dainslef_db.get_collection("act")
    act_compare_cc = db.get_collection("act_compare")

    pages = act_compare_notify_cc.find({
        'file_change_notify': True
    })

    print("###start send_file_change_mail:",pages.count())
    if pages.count() > 0:
        act_datas = []
        for page in pages:
            id = page['_id']
            act_data = act_cc.find_one({'_id':id})
            if not act_data:
                act_data = {}
            act_data_compare = act_compare_cc.find_one({'_id': id})
            act_data['crawel_time'] = 0
            status_right = act_data.get('status') == 50
            if 'crawel_time' in act_data_compare:
                t = datetime.fromtimestamp(act_data_compare['crawel_time'])
                act_data['crawel_time'] = t.strftime('%Y-%m-%d %H:%M:%S')
            if status_right:
                act_datas.append(act_data)

        print("#### act_datas:",act_datas)
        if act_datas:
            content = get_template_string("template/file_change.html",act_datas=act_datas, count=len(act_datas))
            e = modules.notify.Email(send_list=notify_emails)
            subject = "【统计】检测到文件变化（{}）".format(datetime.now())
            e.sendhtml(content=content, subject=subject)

        act_compare_notify_cc.remove({
            'file_change_notify':True
        })


@app.task
def email(**kwargs):
    pid = os.getpid()
    print("### email current pid:",pid)

    send_diffence_pages_mail()
    send_404_pages_mail()
    send_offline_page_mail()
    send_file_change_mail()


@app.task
def push_diffence(objectid):

    objectid = ObjectId(objectid)
    conn = crawelbank.models.mongo.create_mongodb()
    db = conn.get_database("crawelbank")
    act_compare_notify_cc = db.get_collection("act_compare_notify")
    ret = act_compare_notify_cc.update({
        '_id':objectid
    },{
        '$set':{
        'diffence_notify': True
    }
    },upsert=True)
    print("###push_diffence ret:",objectid)


