
from task.celery import app

@app.task
def crawel(**kwargs):
    print("## run  crawel")
    from scrapy import cmdline
    print("## start crawel")
    cmdline.execute("scrapy crawl toscrape-css".split())

