import scrapy
from urllib import request
from public_R.items import PublicRItem
from public_R.settings import add_link,time_01

'''
公共资源交易网  www.sinopr.org
做好统一采集后，做一个按天采集任务就OK了
'''
class SpiderSinopr(scrapy.Spider):
    name = 'sino'
    headers_detail = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_f074ed4925444f15879d71d5eab3cc73=1540523808; UM_distinctid=166ae5fd71d1361-0f4fddd5db0a0a-5701732-1fa400-166ae5fd71e181; _yggc_session=BAh7CUkiD3Nlc3Npb25faWQGOgZFVEkiJWNjYzI5YzM3MzViM2RlZGFmOTFhMzQwMjQ3YWYyOGE1BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMXVndUszNk14bnVpM1h2QWdxNlMxaVNuNTVMRWUyYjdiU0VSd1RZaFMvc1U9BjsARkkiDGNhcHRjaGEGOwBGSSIJN01KRAY7AFRJIhl3YXJkZW4udXNlci51c2VyLmtleQY7AFRbB1sGaQLsUUkiIiQyYSQxMCR6ODN5M0ZUZnl2b01Yby5DVFFxMG0uBjsAVA%3D%3D--8042781037114ff6ac7e8ffb8daddfe2a3b2de12; CNZZDATA1000446276=1725275219-1540521293-%7C1541638823; Hm_lpvt_f074ed4925444f15879d71d5eab3cc73=1541643258',
        'Host': 'www.sinopr.org',
        'If-None-Match': 'W/"49575d97684f1a68a121f6aae5fd1b10"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
    }
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Mobile Safari/537.36',
        }
    }
    base_url = 'https://www.sinopr.org/infos.html?utf8=✓&d=2&i={type}&date={t_s}&page={p}'
    def start_requests(self):
        t_s, t_e = time_01()
        for t in range(int(t_s), int(t_e)):
            for i in [4,10]:
                full_url = self.base_url.format(type=i,t_s=t,p=1)
                yield scrapy.Request(full_url,callback=self.parse,meta={'type':i,'p':1,'t_s':t})
    def parse(self, response):
        tpe,p,t_s = response.meta['type'],response.meta['p'],response.meta['t_s']
        count = int(''.join(response.xpath('//span[@class="accord_2"]/text()').extract()))
        if p == 1: # 翻页
            for i in range(2,int(count/30)+2):
                full_url = self.base_url.format(type=tpe,t_s=t_s,p=i)
                yield scrapy.Request(full_url, callback=self.parse, meta={'type': tpe, 'p': i, 't_s': t_s})
        # 详情页
        news_list = response.xpath('//ul[@id="listter"]/li')
        for news in news_list:
            url = news.xpath('.//div[@class="names"]/a/@href').extract()[0]
            full_url = request.urljoin(response.url,url)
            title = news.xpath('.//div[@class="names"]/a/@title').extract()[0]
            province = ''.join(news.xpath('.//div[@class="region"]/text()').extract()).strip()
            yield scrapy.Request(full_url,callback=self.parse_detail,meta={'title':title,'province':province,'tpe':tpe},headers=self.headers_detail)
    # 详情页
    def parse_detail(self, response):
        pub_time = ''.join(response.xpath('//div[@class="time tc"]/text()').extract()).strip().strip('更新时间')
        source_url = response.xpath('//div[@class="time tc"]/span/span/a/@href').extract()[0]
        news = response.xpath('//div[@class="out_content"]')
        content = add_link(news,response)

        items = PublicRItem()
        items['url'] = response.url
        items['title'] = response.meta['title']
        items['stage'] = str(response.meta['tpe']).replace('4','tender').replace('10','winning')
        items['content'] = content
        items['pub_time'] = pub_time
        items['province'] = response.meta['province']
        items['source_url'] = source_url
        yield items
