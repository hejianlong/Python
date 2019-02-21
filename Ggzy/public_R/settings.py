# -*- coding: utf-8 -*-

# Scrapy settings for public_R project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'public_R'

SPIDER_MODULES = ['public_R.spiders']
NEWSPIDER_MODULE = 'public_R.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'public_R (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 12

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'public_R.middlewares.PublicRSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'public_R.middlewares.PublicRDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'public_R.pipelines.PublicRPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'



# 全部运行
COMMANDS_MODULE = 'public_R.Runall'
# ------------------------------
import time,datetime
from urllib import request

# 超时
# DOWNLOAD_TIMEOUT = 3
# 重试
RETRY_ENABLED = True
RETRY_TIMES = 3


# ------------------------------
def add_link(news, response):  # 为文章添加链接
    content = ''.join(news.extract())
    link_list = news.xpath('.//@src|.//@href').extract()
    if link_list:
        for link in link_list:
            link_url = request.urljoin(response.url, link)
            content = content.replace(link, link_url)
    return content

# 时间格式，同等于gov_data scrapy 框架的时间格式设置=
t_end_now_01 = datetime.datetime.now().strftime('%Y%m%d')
t_end_now_02 = datetime.datetime.now().strftime('%Y-%m-%d')

yesterday = datetime.date.today()-datetime.timedelta(days=1)

def time_01(): # 格式一  # 格式： 20181001,20181019
    # 内蒙古、江苏自定时间
    t_start,t_end = t_end_now_01[:-2]+'01',t_end_now_01
    t_start,t_end = yesterday.strftime('%Y%m%d'),t_end_now_01

    return t_start, t_end
def time_02(): # 格式二  # 格式： '2018-10-01','2018-10-19'
    # 安徽 国务院国有资产监督管理委员会 今日中国
    # t_start, t_end = t_end_now_02[:-3]+'-01',t_end_now_02
    t_start, t_end = str(yesterday),t_end_now_02
    return t_start, t_end
headers_post = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection':'keep-alive',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie':'JSESSIONID=1ddc96da856e0114a12…=1ddc96da856e0114a1246b9ac6e5',
    'Host':'deal.ggzy.gov.cn',
    'Referer':'http://deal.ggzy.gov.cn/ds/deal/dealList.jsp',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/63.0',
    'X-Requested-With':'XMLHttpRequest',
}
t_start, t_end = time_02()
form = {
    'TIMEBEGIN_SHOW': t_start,
    'TIMEEND_SHOW': t_end,
    'TIMEBEGIN': t_start,
    'TIMEEND': t_end,
    'DEAL_TIME': '06',
    'DEAL_CLASSIFY': '02',
    'DEAL_STAGE': '',
    'DEAL_PROVINCE': '0',
    'DEAL_CITY': '0',
    'DEAL_PLATFORM': '0',
    'DEAL_TRADE': '0',
    'isShowAll': '1',
    'PAGENUMBER': '1',
    'FINDTXT': '',
    'validationCode': '',
}
