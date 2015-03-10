#!/usr/bin/env python
#coding=utf-8

#author:lalala

import os
import sys 
import re

from BeautifulSoup import BeautifulSoup,Comment

import codecs

from datetime import date, datetime 

import time
import cookielib
import urllib2

import pickle
import logging
import common

import pinyinGenerator
import polyphoneFilter
import adminConnector
import duplicatesFilter

logger=common.getLogger("crawler")

def loadCookies():
    global logger

    cookies={"SUB":"_2AkMjVJ3Rf8NhqwJRmPkXyG7kb4V-wg_EiebDAHzsJxJTHnge7FAoF_3pfd_Q-mRirmrrpd3_0f3i",
        "SUBP":"0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5bwX5CCSGevosLGKiFWv1z", 
        "SINAGLOBAL":"5799703761410.659.1409815276676",
        "ULV":"1423219971545:3:1:1:5520051170822.918.1423219971481:1413793237690",
        "UOR":",,news.ifeng.com",
        "YF-Page-G0":"27b9c6f0942dad1bd65a7d61efdfa013",
        "_s_tentry":"-",
        "Apache":"5520051170822.918.1423219971481"}
    try:
        f=open("weibocookie","r")
        lastVisit="".join(f.readlines())
        if(lastVisit.strip()!=""):
           logger.debug(lastVisit) 
    except IOError:
        logger.debug("cannot find weibo cookie file")
        pass

    return cookies

def saveCookies(cookies):
    global logger
    if(len(cookies.keys())>0):
        f=open("weibocookie","w")
        for name in cookies.keys():
            f.write(name+":"+cookies[name]+",")
            logger.debug(name+":"+cookies[name]+",")
        cookies=cookies[0:-2]
    return

#微博热门话题
def weiboTopicHandler(link):
    #writeResult(link)
    cookies=loadCookies()
    html,cookies=requestIt(link, cookies=cookies)
    #save cookies
    ls=re.search(r'<script>.*?"domid":"Pl_Discover_Pt6Rank__5"(.*?)<\/script>',html)
    if(ls is not None):
        ws = re.findall(r'.*?class=\\"S_txt1\\".*?#(.*?)#<\\/a>', ls.group(),re.S)
    #ls=re.findall(r'^<script>.*?"domid":"Pl_Discover_Pt6Rank__5".*?class=\\"S_txt1\\".*?#(.*?)#<\\/a>',html, re.S)
    #TODO：save cookies
    saveCookies(cookies)
    return ws[:10]

#百度热词
def baiduHotHandler(link):
    #writeResult(link)
    hots=[]
    html,cookies=requestIt(link, "gbk")
    soup=BeautifulSoup(html)
    outer=soup.find("table",{"class":"list-table"})
    #取 top 10
    spans=outer.findAll("span",{"class":"icon icon-new"},limit=10)
    for span in spans[:10]:
        word=span.parent.find("a",{"class":"list-title"})
        hots.append(word.string)
    return hots

#百度电影
def baiduMovieHandler(link):
    #writeResult(link)
    hots=[]
    html,cookies=requestIt(link, "gbk")
    soup=BeautifulSoup(html)
    outer=soup.find("table",{"class":"list-table"})
    #取 top 5
    spans=outer.findAll("span",{"class":"icon-rise"},limit=5)
    for span in spans[:5]:
        word=span.parent.parent.find("a",{"class":"list-title"})
        hots.append(word.string)
    return hots

'''搜狗新词解析
    没使用搜狗来源
'''
def sougouNewHandler(link):
    #writeResult(link)
    html,cookies=requestIt(link)
    soup=BeautifulSoup(html)
    outer=soup.find("div",{"id":"newdict_show"})
    tag_divs=[]
    tag_divs=outer.findAll("div",{"id":re.compile(r"^newdict_title_[1-5]")})   
    #tag_divs=tag_divs+outer.findAll("div",{"class":re.compile(r"^newdict_txt_[1-5]")})
    tag_divs=tag_divs+outer.findAll("div",{"class":"newdict_list item"})
    for _div in tag_divs:
        #print(("".join(_div.findAll(text=True)).replace(re.compile(r"\s"),"")))
        filterResult("".join(_div.findAll(text=True)).replace("\n",""))
    return


#不管网页是什么编码，都返回 utf-8 格式
#网页的解析格式默认采用utf-8 编码
def requestIt(link, encoding='utf-8',cookies={}):
    opener=urllib2.build_opener()
    opener.addheaders = [
        ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
        ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'),
        ('Pragma','no-cache'),
        ('Cache-Control', 'no-cache'),
        ('Keep-Alive', '115'),
        ('Connection', 'keep-alive'),
#        ('Accept-Encoding:','gzip, deflate, sdch'),
        ("Cookie", 'SUB=_2AkMjVJ3Rf8NhqwJRmPkXyG7kb4V-wg_EiebDAHzsJxJTHnge7FAoF_3pfd_Q-mRirmrrpd3_0f3i; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5bwX5CCSGevosLGKiFWv1z; SINAGLOBAL=5799703761410.659.1409815276676; ULV=1423219971545:3:1:1:5520051170822.918.1423219971481:1413793237690; UOR=,,news.ifeng.com; YF-Page-G0=27b9c6f0942dad1bd65a7d61efdfa013; _s_tentry=-; Apache=5520051170822.918.1423219971481'),
        ('Referer', 'http://weibo.com'),
        ('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36')
    ]
        
    r=opener.open(link)
    text=r.read().decode(encoding)
    return text.encode("utf-8"),{}

def filterResult(word):
    return writeLineResult(line)
        
def writeLineResult(line, target_file):
    target_file.writelines(line+"\r\n")
    return

def writeDictResult(_dict, target_file):
    for (word,pinyin) in _dict.items():
        writeLineResult(word+"\t"+pinyin,target_file)
    return

def writeListResult(_list, target_file):
    for single in _list:
        writeLineResult(single, target_file)
    return
    
def main():
    global target_file,logger

    timeStamp=str(time.strftime("%Y-%m-%d-%H", time.localtime()))
    rootPath=common.getRootPath()
    target_file=open(rootPath+"/hotWords"+timeStamp+".txt","w")

    common.initEncoding("utf-8")
    source_map={
        #搜狗词库每日新词 (5个)
        #"http://pinyin.sogou.com/dict/": sougouNewHandler,
        #百度电影类别 即将上映 搜索上升阶段 top5
        "http://top.baidu.com/buzz?b=659&c=1&fr=topcategory_c1": baiduMovieHandler,
        #百度电影类别 正在热映 搜索上升阶段 top5
        "http://top.baidu.com/buzz?b=661&c=1&fr=topbuzz_b659_c1": baiduMovieHandler,
        #微博热门话题 社会类别 top10
        #"http://d.weibo.com/100803_ctg1_1_-_ctg11?from=faxian_huati&mod=mfenlei": weiboTopicHandler,
        #微博热门话题 娱乐八卦 top10
        #"http://d.weibo.com/100803_ctg1_2_-_ctg12?from=faxian_huati&mod=mfenlei": weiboTopicHandler,
        #百度搜索实时热点排行榜 (取带“新”标签 词)
        "http://top.baidu.com/buzz?b=1&c=513&fr=topbuzz_b1_c513": baiduHotHandler
    }

    words_list=[]
    for link in source_map:
        try:
            handler=source_map[link]
            words_list+=handler(link)
        except Exception, e:
            logger.debug(e)
            raise
    logger.debug(words_list)

    '''the words will be commited into the hotword admin'''
    words_dict={}
    '''the words will be sent to mail'''
    send_mail_dict={}
    send_mail_list=[]

    '''filter the words longer than 7'''
    send_mail_list=polyphoneFilter.filterLongerThan7(words_list)
    '''filter the words list which contains duo yinzi out of the words_list'''
    send_mail_list+=polyphoneFilter.filterDuoyinzi(words_list)
    logger.debug("send mail list:")
    logger.debug(send_mail_list)

    '''zhuyin'''
    words_dict=pinyinGenerator.zhuyin(words_list)

    '''merge the dict which cannot be zhu yin'''
    for(word,pinyin) in words_dict.items():
        if(pinyin==""):
            send_mail_dict[word]=""
            del words_dict[word]
               
    for word in send_mail_list:
        send_mail_dict[word]=""

    '''is Auto commit switch open'''
    if(adminConnector.isAutoOpen()==0):
        '''manual model'''
        send_mail_dict.update(words_dict)
        writeDictResult(send_mail_dict, target_file)
        target_file.close()
        '''send mail'''
        common.sendMail(target_file, timeStamp)
    else:
        '''auto model'''   
        oldWords=duplicatesFilter.findDuplicateWords(words_dict)  
        logger.debug("after duplicatesFilter, the words_dict remain:")
        logger.debug(words_dict)
        logger.debug("save words into db:")
        _re=adminConnector.commitHots(words_dict)
        if(_re is True):
            duplicatesFilter.saveHotWords(words_dict)
        else:
            logger.debug("cannot commit hotWords")

        return


target_file=None   

if __name__=="__main__":
    logger.debug("hotWordsCrawl starts at: "+str(datetime.now()))
    main()
    logger.debug("hotWordsCrawl ends at: "+str(datetime.now()))
