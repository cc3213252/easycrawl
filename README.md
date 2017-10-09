一个适合生产环境的爬虫框架
=============

该爬虫框架有如下优点：
1. 一键部署
2. 异步定时执行爬虫脚本，并可查看队列状态
3. 有清晰的代码目录结构
4. url去重
5. 断点续爬
6. cookies等防封杀


### 使用技术
1. python3
2. scrapy
3. supervisor
4. fabric
5. celery

### 依赖服务
1. MongoDB
2. Rabbitmq

### 安装
1. pip install -r requirements.txt


### 运行
1. cd easycrawl
2. scrapy crawl toscrape-css


