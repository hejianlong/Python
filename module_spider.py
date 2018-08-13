import pymysql
from urllib import request,parse
from urllib.error import HTTPError,URLError
import fake_useragent
def main(url,headers=None,data=None): # 调用函数
    if not data:
        return get_response(url,headers=headers)
    else:
        return get_response(url,headers=headers,data=data)

def get_response(url,data=None,headers=None):
    if not headers:
        headers = {'User-Agent':get_agent()}
    try:
        if data:
            data = parse.urlencode(data)
            data = bytes(data,encoding='utf-8')
            req = request.Request(url, data=data, headers=headers)
        else:
            req = request.Request(url,headers=headers)
        response = request.urlopen(req)
        data = response.read().decode()
        return data # 返回数据

    except HTTPError as e: # 总的错误信息，不适合用于调试
        print(e)
    except URLError as e:
        print(e)

def get_agent(table=None):
    table = 'p_useragent'
    conn = pymysql.connect('127.0.0.1', 'root', '123456', 'PaChong', charset='utf8')
    cursor = conn.cursor()
    sql = 'SELECT * FROM {} WHERE id >= ((SELECT MAX(Id) FROM {})-(SELECT MIN(Id) FROM {})) * RAND() + (SELECT MIN(Id) FROM p_useragent)  LIMIT 1'.format(
        table, table, table)
    rwo = cursor.execute(sql)
    useragent = cursor.fetchall()[0][1]
    return useragent

if __name__ == '__main__':
    url = 'http://fanyi.baidu.com/sug'
    data = {'kw':'中国'}
    import json
    res = json.loads(main(url,data=data))
    print(res)

    # url = 'http://www.baidu.com'
    # res = main(url)
    # print(res)

