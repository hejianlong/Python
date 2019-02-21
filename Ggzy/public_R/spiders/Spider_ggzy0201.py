import scrapy
import json
from urllib import request
from public_R.items import PublicRItem
from public_R.settings import headers_post, form,add_link
'''
暂缓，页面改版，页面仍然有问题，如果不是页面真的改版，就是新的反爬机制
采集数据过多时，页面会变成ajax加载？采集少了又正常了，不科学，经测试，只有这一台电脑的谷歌浏览器如此，应该是某种反爬机制
且网站采集时有延迟，所以会导致有时采集不到
全国公共资源交易平台 http://www.ggzy.gov.cn
针对不同的浏览器，可能有限制，还有IP地址上面的限制
'''
class ggzySpider(scrapy.Spider):
    name = 'ggzy0201'
    find_url = 'http://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp'
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/63.0',
        }
    }
    def start_requests(self):
        stage_list = ['0201']
        for stage in stage_list: # 招投、中标
            req_form = form
            req_form['DEAL_STAGE'] = stage
            yield scrapy.FormRequest(self.find_url, method='POST', formdata=req_form, callback=self.parse,
                                     meta={'req_form':req_form,'cookiejar':1,'page':1},
                                         headers=headers_post,dont_filter=True,)
    def parse(self, response):
        page = response.meta['page']
        req_form = response.meta['req_form']
        html = json.loads(response.text)
        total_pn = html['ttlpage']
        news_num = int(html['ttlrow']) # 信息总数
        publicont_list = html['data']  # 页面中每条信息
        if news_num: # 页面获取无错误
            # 详情页
            for news in publicont_list:
                url = news['url'] # 详情地址
                stage = news['stageShow'] # 信息类型
                platform = news['platformName'] # 来源平台
                province = news['districtShow'] # 省
                yield scrapy.Request(url,callback=self.parse_inner,
                                     meta={'province':province,'stage':stage,'platform':platform},headers=headers_post)
            # 翻页
            if news_num >= 1 and page == 1:
                for i in range(2,int(total_pn)+1):
                    req_form['PAGENUMBER'] = str(i)
                    print(i)
                    yield scrapy.FormRequest(self.find_url, method='POST', formdata=req_form, callback=self.parse,
                                         meta={'req_form':req_form,'cookiejar':response.meta['cookiejar'],'page':i},
                                             headers=headers_post,dont_filter=True)
    def parse_inner(self,response):
        stage = response.meta['stage'] # 招投、中标
        province = response.meta['province'] # 省
        platform = response.meta['platform'] # 来源平台名称
        news_list = response.xpath('//ul[@class="fully_list"]/li[@class="li_hover"]')
        for news in news_list:
            title = ''.join(news.xpath('./a/@title').extract())
            url = ''.join(news.xpath('./a/@onclick').extract())
            full_url = request.urljoin(response.url,url.split('\'')[-2])
            yield scrapy.Request(full_url,callback=self.parse_detail,
                                 meta={'title':title,'stage':stage,'province':province,'platform':platform})
    def parse_detail(self,response): # 最终页
        title = response.meta['title']
        stage = response.meta['stage']
        province = response.meta['province']
        platform = response.meta['platform']
        news = response.xpath('//div[@id="mycontent"]') # 新闻主体
        content = add_link(news,response)
        pub_time = response.xpath('//p[@class="p_o"]/span/text()').extract()[0].lstrip('发布时间：')
        source_url = ''.join(response.xpath('//span[@class="detail_url"]/a/@href').extract())
        items = PublicRItem()
        items['url'] = response.url
        items['title'] = title
        items['stage'] = 'tender' # 招标
        items['content'] = content
        items['pub_time'] = pub_time
        items['province'] = province
        items['source_url'] = source_url
        items['source_name'] = platform
        yield items
