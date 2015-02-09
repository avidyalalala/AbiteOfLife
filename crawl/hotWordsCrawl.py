#!/usr/bin/env python
#coding=utf-8

#author:lalala

import os
import sys 
import re

from BeautifulSoup import BeautifulSoup,Comment

import codecs

from datetime import date, timedelta, datetime 
import cookielib

import pickle
import requests

def save_cookies(requests_cookiejar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f)

def load_cookies(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


#微博热门话题
def weiboTopicParser(html):

    #print(html)
    #html="".join(open("weiboHot.html","r").readlines())
    ls=re.search(r'<script>.*?"domid":"Pl_Discover_Pt6Rank__5"(.*?)<\/script>',html)
    if(ls is not None):
        print("found:")
        ws = re.findall(r'.*?class=\\"S_txt1\\".*?#(.*?)#<\\/a>', ls.group(),re.S)
    #ls=re.findall(r'^<script>.*?"domid":"Pl_Discover_Pt6Rank__5".*?class=\\"S_txt1\\".*?#(.*?)#<\\/a>',html, re.S)
    for _word in ws[0:10]:
        print(_word)
    return

def weiboTopicHandler(link):

    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    
#save cookies

#load cookies and do a request
    opener.addheaders = [
        ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
        ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'),
        ('Pragma','no-cache'),
        ('Cache-Control', 'no-cache'),
#                ('Keep-Alive', '115'),
        ('Connection', 'keep-alive'),
        ('Accept-Encoding:','gzip, deflate, sdch'),
       # ('Cookie',cookies),
       # ("Cookie", 'SUB=_2AkMjVJ3Rf8NhqwJRmPkXyG7kb4V-wg_EiebDAHzsJxJTHnge7FAoF_3pfd_Q-mRirmrrpd3_0f3i; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5bwX5CCSGevosLGKiFWv1z; SINAGLOBAL=5799703761410.659.1409815276676; ULV=1423219971545:3:1:1:5520051170822.918.1423219971481:1413793237690; UOR=,,news.ifeng.com; YF-Page-G0=27b9c6f0942dad1bd65a7d61efdfa013; _s_tentry=-; Apache=5520051170822.918.1423219971481'),
        ('Referer', 'http://weibo.com'),
        ('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36'
)
    ]
                
    response = opener.open('http://weibo.com')

    #opener.addheader('Cookie', cookies)
    response=opener.open(link, timeout=180).read()
    #response = urllib2.urlopen(link, timeout=180)
    cookies=""
    for item in cookie:
        print(item)
        print(item.name)
        print(item.value)
        cookies=item.name+"="+item.value
    print(cookies)

    parser=source_dict[link]
    parser(response)


def baiduHotHandler(link):
    html=requestIt(link, "gbk")
    soup=BeautifulSoup(html)
    outer=soup.find("div",{"class":"mainBody"})
    #取 top 10
    spans=outer.findAll("span",{"class":"icon icon-new"},limit=10)
    for span in spans[:10]:
        word=span.parent.find("a",{"class":"list-title"})
        print(word.string)

    return

#搜狗新词解析
def sougouNewHandler(link):
    html=requestIt(link)
    soup=BeautifulSoup(html)
    outer=soup.find("div",{"id":"newdict_show"})
    tag_divs=[]
    tag_divs=outer.findAll("div",{"id":re.compile(r"^newdict_title_[1-5]")})   
    #tag_divs=tag_divs+outer.findAll("div",{"class":re.compile(r"^newdict_txt_[1-5]")})
    tag_divs=tag_divs+outer.findAll("div",{"class":"newdict_list item"})
    for _div in tag_divs:
        #print(("".join(_div.findAll(text=True)).replace(re.compile(r"\s"),"")))
        print(("".join(_div.findAll(text=True)).replace("\n","")))
    return


#不管网页是什么编码，都返回 utf-8 格式
#网页的解析格式默认采用utf-8 编码
def requestIt(link, encoding='utf-8'):
    r=requests.get(link)
    r.encoding=encoding
    return r.text.encode("utf-8")

def main():
    source_dict={
        #搜狗词库每日新词 (5个)
        "http://pinyin.sogou.com/dict/": sougouNewHandler,
        #微博热门话题 电影类别 top10
#        "http://d.weibo.com/100803_ctg1_100_-_ctg1100?from=faxian_huati&mod=mfenlei": weiboTopicHandler,
        #微博热门话题 社会类别 top10
#        "http://d.weibo.com/100803_ctg1_1_-_ctg11?from=faxian_huati&mod=mfenlei": weiboTopicHandler,
#        #微博热门话题 娱乐八卦 top10
#        "http://d.weibo.com/100803_ctg1_2_-_ctg12?from=faxian_huati&mod=mfenlei": weiboTopicHandler,
#        #百度搜索实时热点排行榜 (取带“新”标签 词)
        "http://top.baidu.com/buzz?b=1&c=513&fr=topbuzz_b1_c513": baiduHotHandler
    }

    for link in source_dict:
        try:
            print(link)
            handler=source_dict[link]
            handler(link)
        except Exception, e:
            print(e)
            raise
    return

if __name__=="__main__":
    encoding="utf-8"
    if(sys.getdefaultencoding()!=encoding):
        reload(sys)
        sys.setdefaultencoding(encoding)
        print("the system encoding is "+sys.getdefaultencoding())
    print("hotWordsCrawl starts at: "+str(datetime.now()))
    main()
    print("hotWordsCrawl ends at: "+str(datetime.now()))
