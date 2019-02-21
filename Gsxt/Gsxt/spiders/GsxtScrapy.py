from scrapy import Spider,Request,FormRequest
import json,time,random
'''
通过手机端app获取接口
1、目前问题，需要代理，否则被封是没跑了
2、请求头看情况需要不需要多弄一些
'''
class GsxtSpider(Spider):
    name = 'gsxt'
    start_urls = []
    allowed_domains = []
    file = './static/公司名称.txt'
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json;charset=utf-8',
                'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; MI 5s Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/64.0.3282.137 Mobile Safari/537.36 Html5Plus/1.0',
                'Host': 'app.gsxt.gov.cn',
                'Accept-Encoding': 'gzip',
                'Connection': 'keep-alive',
        }
    }
    def start_requests(self):

        f = open(self.file,'r',encoding='gbk')
        count = 1
        while True:
            res = f.readline()
            wd = res.strip().replace(' ','')
            url = 'http://app.gsxt.gov.cn/gsxt/cn/gov/saic/web/controller/PrimaryInfoIndexAppController/search?page=1'
            form = {
                "searchword": wd,
                "conditions": {
                    "excep_tab": "0",
                    "ill_tab": "0",
                    "area": "0",
                    "cStatus": "0",
                    "xzxk": "0",
                    "xzcf": "0",
                    "dydj": "0"
                }
            }
            form_json = json.dumps(form,ensure_ascii=False)
            yield FormRequest(url,method='POST',body=form_json.encode('utf-8'),callback=self.parse,meta={'count':count,'wd':wd},dont_filter=False)
            count += 1
            # if count == 10:
            #     break
            if not res:
                break

    def parse(self, response):
        # print('-' * 10,'进入GSXT查询结果界面...','-'*10)
        page = json.loads(response.text)  # 页面信息
        recordsTotal = page['data']['result']['recordsTotal']  # 数据量
        # print('词条：%s 查询结果：%s' % (response.meta['wd'],recordsTotal))

        res_list = page['data']['result']['data']
        for i in res_list:
            # entType nodeNum pripid nodeNum entType 拼接的地址
            entType = i['entType']
            nodeNum = i['nodeNum']
            pripid  = i['pripid']
            # print(entType,nodeNum,pripid)
            url = 'http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-primaryinfoapp-entbaseInfo-{}.html?nodeNum={}&entType={}'.format(pripid,nodeNum,entType)
            time.sleep(random.randrange(2,5))
            yield FormRequest(url,method='POST',callback=self.parse_detail,dont_filter=False)

    def parse_detail(self,response):
        # print(response.text)
        print('-'*50)
        page = json.loads(response.text)  # 页面信息
        try:
            entName = page['result']['entName'] # 公司名称
            regNo = page['result']['regNo'] # 注册号
            uniscId = page['result']['uniscId'] # 信用代码
            name = page['result']['name'] # 法人名称
            regState_CN = page['result']['regState_CN'] # 公司状态
            entType_CN = page['result']['entType_CN'] # 公司类型
            dom = page['result']['dom'] # 公司地址
            opScope = page['result']['opScope'] # 业务描述
            regOrg_CN = page['result']['regOrg_CN'] # 登记机关
            estDate = page['result']['estDate'] # 成立日期
            apprDate = page['result']['apprDate'] # 核准日期
            opFrom = page['result']['opFrom'] # 合伙期限 自
            opTo = page['result']['opTo'] # 合伙期限 止
            regCaption = page['regCaption'] # 注册资金

            item = {
                'entName': entName,
                'regNo': regNo,
                'uniscId': uniscId,
                'name': name,
                'regState_CN': regState_CN,
                'entType_CN': entType_CN,
                'dom': dom,
                'opScope': opScope,
                'regOrg_CN': regOrg_CN,
                'estDate': estDate,
                'apprDate': apprDate,
                'opFrom': opFrom,
                'opTo': opTo,
                'regCaption': regCaption,
            }
            print(item)
        except Exception as e: # 可能刷新过快会产生空值
            print('错误代码：%s，返回结果：%s' % (e,page))
            yield FormRequest(response.url,method='POST',callback=self.parse_detail,dont_filter=False)