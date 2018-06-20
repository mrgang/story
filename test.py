#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml import etree
import urllib.parse as UrlPase
import requests,json
from HtmlAnalyzer import Analyzer
keyword = "牧神"
headers = {'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'}
action = "menuPage"
path = "https://m.zwdu.com/book/23488/"
path1 = "https://m.zwdu.com/book/23488/13302398.html"
resp = requests.get(path, headers=headers, timeout=5)
if resp and resp.status_code == 200:
    proto, rest = UrlPase.splittype(resp.url)
    host, rest = UrlPase.splithost(rest)
    if host == 'm.zwdu.com' or host == 'm.biqubao.com':
        resp.encoding = "GBK"
    else:
        resp.encoding = "utf-8"
    content = resp.text
    if action == "mainPage":
        print(Analyzer.mainPage(proto, host, content))
    elif action == 'menuPage':
        print(Analyzer.menuPage(proto, host, content))
    elif action == 'contentPage':
        print(Analyzer.contentPage(proto, host, rest, content))
    else:
        print(json.dumps({'success': False, 'content': 'current.there has not deal with,later will done'}))
