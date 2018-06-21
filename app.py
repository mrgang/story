#! /usr/bin/python3

from gevent import monkey
monkey.patch_all()
from flask import Flask,request
from gevent.pywsgi import WSGIServer
import requests,json
import urllib.parse as UrlPase
from bs4 import BeautifulSoup
headers = {'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'}
app = Flask(__name__)

@app.route("/")
def mainpage():
    return "Server is Running!"
@app.route('/',methods=['POST','GET'])
def wel():
    return '''<h1 style='text-align:center'>Server is Running.</h1>'''
@app.route('/getPage',methods=['POST','GET'])
def getp():
    path = request.args.get('path')
    resp = requests.get(path, headers=headers, timeout=5)
    proto, rest = UrlPase.splittype(resp.url)
    host, rest = UrlPase.splithost(rest)
    if host == 'm.zwdu.com' or host == 'm.biqubao.com':
        resp.encoding = "GBK"
    else:
        resp.encoding = "utf-8"
    content = resp.text

    return content

@app.route('/Analyzer/<string:action>',methods=['POST','GET'])
def mainPage(action):
    path = request.args.get('path')
    global resp
    resp = False
    try:
        resp = requests.get(path, headers=headers, timeout=5)
    except:
        # 连接超时，第一次重试
        # print('第一次重试', path)
        try:
            resp = requests.get(path, headers=headers, timeout=5)
        except:
            # 连接超时，第二次重试
            # print('第二次重试', path)
            try:
                resp = requests.get(path, headers=headers, timeout=10)
            except:
                # print('第二次失败', path)
                return json.dumps({'success': False})
    if resp and resp.status_code == 200:
        proto, rest = UrlPase.splittype(resp.url)
        host, rest = UrlPase.splithost(rest)
        if host == 'm.zwdu.com' or host == 'm.biqubao.com':
            resp.encoding = "GBK"
        else:
            resp.encoding = "utf-8"
        content = resp.text
        if action == "mainPage":
            return json.dumps({'success': True,"proto":proto,"host":host})
            #return Analyzer.mainPage(proto, host, content)
        elif action == 'menuPage':
            return json.dumps({'success': True, "proto": proto, "host": host})
            #return Analyzer.menuPage(proto, host, content)
        elif action == 'contentPage':
            return json.dumps({'success': True, "proto": proto, "host": host})
            #return Analyzer.contentPage(proto, host,rest, content)
        else:
            return json.dumps({'success': False,'content':'current.there has not deal with,later will done'})
    else:
        print("resp can not read")
@app.route('/Search/<string:keyword>',methods=['POST','GET'])
def search(keyword):
    result = []
    # biqudu搜索
    resp = requests.get("http://zhannei.baidu.com/api/customsearch/searchwap?s=13603361664978768713&q=" + keyword,
                        headers=headers)
    if resp.status_code == 200:
        searchResult = json.loads(resp.text)['results']
        if len(searchResult) > 2:
            for i in range(3):
                url = searchResult[i]['url'].replace('http', 'https').replace('www', 'm')
                name = searchResult[i]['name']
                if keyword in name:
                    result.append({'url': url})
    # m.qu.la搜索
    resp = requests.get("http://zhannei.baidu.com/api/customsearch/searchwap?s=920895234054625192&q=" + keyword,
                        headers=headers)
    if resp.status_code == 200:
        searchResult = json.loads(resp.text)['results']
        if len(searchResult) > 2:
            for i in range(3):
                url = searchResult[i]['url'].replace('http', 'https').replace('www', 'm')
                name = searchResult[i]['name']
                if keyword in name:
                    result.append({'url': url})
    # m.biqudao.com搜索
    resp = requests.get(
        "http://zhannei.baidu.com/api/customsearch/searchwap?s=3654077655350271938&q=" + keyword,
        headers=headers)
    if resp.status_code == 200:
        searchResult = json.loads(resp.text)['results']
        if len(searchResult) > 2:
            for i in range(3):
                url = searchResult[i]['url'].replace('http', 'https').replace('www', 'm')
                name = searchResult[i]['name']
                if keyword in name:
                    result.append({'url': url})
    # m.zwdu.com搜索
    # resp = requests.get(
    #     "https://m.zwdu.com/search.php?keyword=" + keyword,
    #     headers=headers)
    # if resp.status_code == 200:
    #     html = etree.HTML(resp.text)
    #     cps = html.xpath("//div[@class='result-item result-game-item']")
    #     mark = 0
    #     for cpc in cps:
    #         mark += 1
    #         if mark > 3: break
    #         cp = etree.HTML(etree.tostring(cpc))
    #         url = cp.xpath("/html/body/div/div[2]/h3/a")[0].get('href')
    #         name = cp.xpath("/html/body/div/div[2]/h3/a")[0].get('title')
    #         if keyword in name:
    #             result.append({'url': url})
    # https://m.biqubao.com/ 搜索 https://m.biqubao.com/search.php?keyword=%E6%9C%A8
    # resp = requests.get(
    #     "https://m.biqubao.com/search.php?keyword=" + keyword,
    #     headers=headers)
    # if resp.status_code == 200:
    #     html = etree.HTML(resp.text)
    #     cps = html.xpath("//div[@class='result-item result-game-item']")
    #     mark = 0
    #     for cpc in cps:
    #         mark += 1
    #         if mark > 3: break
    #         cp = etree.HTML(etree.tostring(cpc))
    #         url = cp.xpath("/html/body/div/div[2]/h3/a")[0].get('href')
    #         name = cp.xpath("/html/body/div/div[2]/h3/a")[0].get('title')
    #         if keyword in name:
    #             result.append({'url': url})
    return json.dumps(result)


if __name__ == '__main__':
    WSGIServer(('0.0.0.0',8080),app).serve_forever()



