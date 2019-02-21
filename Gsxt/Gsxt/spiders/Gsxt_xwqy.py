import requests
import re,json,time
import urllib
from urllib import parse

'''
主要是想要搞定滑动验证码的问题
'''
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'xwqy.gsxt.gov.cn',
    'Origin': 'http://xwqy.gsxt.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'http://xwqy.gsxt.gov.cn/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}

def get_page(kw):
    kw_encode = parse.quote(kw).encode('utf-8')

    form_data = {
        'organId':'100000',
        'textfield':kw_encode,
        'fwId':'1400',
        'searchOrganId':'',
        'channelId':'99',
        'captcha':'',
        'geetest_challenge':'d82c8d1619ad8176d665453cfb2e55f0d0',
        'geetest_validate':'11155ee5157cc36_5e1ee5e15c230_5e111111555e28',
        'geetest_seccode':'11155ee5157cc36_5e1ee5e15c230_5e111111555e28|jordan',
    }
    url = 'http://xwqy.gsxt.gov.cn/mirco/micro_lib'
    response = requests.post(url,data=form_data,headers=headers)
    try:
        comp_info = eval(re.compile(r'var objTbody = \[(.*)\]').findall(response.text)[0])
        for i in comp_info:
            entname = i['entname']      # 公司名称
            regno = i['regno']          # 社会统一代码
            cptltotal = i['cptltotal']  # 资金数额
            enttype = i['enttype']      # 公司类型
            regorganid = i['regorganid']# 登记机关
            # entid = i['entid']          # 下一个页面解析需要的元素，但下个页面里只多了一个成立日期，所以先不解析
            form = {
                'entname' : entname,
                'regno' : regno,
                'cptltotal' : cptltotal,
                'enttype' : enttype,
                'regorganid' : regorganid,
            }
            yield form
    except Exception as e:
        print('解析失败',e)
def get_key_city(): # 获取城市列表
    key_cities = []
    f= open('../static/city.json','r',encoding='utf-8')
    cities = f.read()
    cities = json.loads(cities)
    cities = (cities['data']['cityList'])
    for i in cities:
        key_cities.append(i['name']) # 省
        city_list = i['subLevelModelList']
        for ii in city_list:
            key_cities.append(ii['name']) # 市
    return key_cities


if __name__ == '__main__':
    kw_list = set(get_key_city())
    for kw in kw_list:
        print('-'*100)
        print('当前关键词',kw)
        for form in get_page(kw):
            print(form['entname'])
            break