#!/usr/bin/env python
#coding=utf-8

#author:lalala

import os
import sys 
import re

from BeautifulSoup import BeautifulSoup,Comment

import codecs

from datetime import date, timedelta, datetime 
import urllib2

#搜狗新词解析
def sougouNewParser(html):
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

#微博热门话题
def weiboTopicParser(html):
    soup=BeautifulSoup(html)
    outer=soup.find("ul",{"class":"pt_ul clearfix"})
    #取 top 10
    divs=out.findAll("div",{"class":"title W_autocut"},text=True,limit=10)
    for div in divs:
        print(div)
    return

def baiduHotParser(html):
    soup=BeautifulSoup(html)
    outer=soup.find("ul",{"class":"pt_ul clearfix"})
    #取 top 10
    divs=out.findAll("span",{"class":"icon icon-new"},text=True,limit=10)

    return

def main():
    source_dict={
        #微博热门话题 电影类别 top10
        "http://d.weibo.com/100803_ctg1_100_-_ctg1100?from=faxian_huati&mod=mfenlei#": weiboTopicParser,
        #微博热门话题 社会类别 top10
        "http://d.weibo.com/100803_ctg1_1_-_ctg11?from=faxian_huati&mod=mfenlei#": weiboTopicParser,
        #微博热门话题 娱乐八卦 top10
        "http://d.weibo.com/100803_ctg1_2_-_ctg12?from=faxian_huati&mod=mfenlei#": weiboTopicParser,
        #搜狗词库每日新词 (5个)
        "http://pinyin.sogou.com/dict/": sougouNewParser,
        #百度搜索实时热点排行榜 (取带“新”标签 词)
        "http://top.baidu.com/buzz?b=1&c=513&fr=topbuzz_b1_c513": "baiduHotParser"
    }

    for link in source_dict:
        try:
            response = urllib2.urlopen(link, timeout=180)
            parser=source_dict[link]
            parser(response)
        except Exception, e:
            print(e)
            pass
    return

if __name__=="__main__":
    print("hotWordsCrawl starts at: "+str(datetime.now()))
    main()
    print("hotWordsCrawl ends at: "+str(datetime.now()))
