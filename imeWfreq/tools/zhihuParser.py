#!/usr/bin/env python
#coding=utf-8

# author:lalala

import os
import sys
import re

from BeautifulSoup import BeautifulSoup

import xml.dom.minidom  
from xml.dom.minidom import Document 
from imp import reload

import codecs

import baseParser
import parserDispatcher

from datetime import date, timedelta, datetime 

class ZhihuPage(baseParser.BasePage):
    def __init__(self,input_path, output_path, least_date):
        #baseParser.BasePage.__init__(self, input_path, output_path, least_date)
        self.input_path=input_path
        self.output_path=output_path
        #output_dir=output_path+timestamp, like output_path/20141217, the timestamp is the date the page's birthday in website
        #not the date be downloaded
        self.output_dir=""
        self.url=""
        self.rawdata=""
        self.content=""
        #birthday is date,not datetime!!!!!
        self.birthday=None
        self.isQualified=False
        self.output_name=""
        self.init(least_date)

    def init(self,least_date):
        return baseParser.BasePage.init(self,least_date)
        
    def initEncoding(self):
        return baseParser.BasePage.initEncoding(self)

    def initRawData(self):
        return baseParser.BasePage.initRawData(self)

    def initUrl(self):
        return baseParser.BasePage.initUrl(self)

    def initBirthDay(self):
        return baseParser.BasePage.initBirthDay(self)

    def initQualified(self,date):
        return baseParser.BasePage.initQualified(self,date)

    def createOutPutDir(self):
        return baseParser.BasePage.createOutPutDir(self)

    def initOutPutName(self):
        #handle the url change into file name
        pattern = re.compile(r'(http:)|(https:)|(\/)|(\?)')
        name= pattern.sub("", self.url)
        return name

    def initContent(self):
        #print(datetime.now())
        soup=BeautifulSoup(self.rawdata)
        text=''
        #这段注释不要删除，提取更精准，但会造成性能下降，单核与find 对比，
        #会多出 将近300ms的处理速度，对于 18万文件，意味着增加 850分钟/实际并行进程数
        #divs=soup.findAll("div",{"class":re.compile("zm-editable-content*")})
        #if(divs is not None and len(divs)>0) :
        #    for content_div in divs:
        #        text=text+''.join(content_div.findAll(text=True))

        #<div id="zh-question-answer-wrap"></div>问答页
        content_div=soup.find("div",{"id":re.compile(r"zh-question-answer-wrap|zh-profile-activity-wrap|zh-topic-feed-list|zh-single-list-page-wrap")})
        if(content_div is not None) :
            text=''.join(content_div.findAll(text=True))
            _soup=BeautifulSoup(text)
            text=''.join(_soup.findAll(text=True))
            self.content=text
            return
            
	#用户主页 http://www.zhihu.com/people/yang-tian-nan
#        content_div=soup.find("div",{"id":"zh-profile-activity-wrap"})

        #topic 页面 http://www.zhihu.com/topic/19554426
#        content_div=soup.find("div",{"id":"zh-topic-top-page-list"})
 
        #collection 页面 http://www.zhihu.com/collection/25501883
#        content_div=soup.find("div",{"id":"zh-single-list-page-wrap"})

        #print(datetime.now())
        return 
     
if __name__=="__main__":
    
   htmlParser=parserDispatcher.ParserDispatcher(sys.argv[1], ZhihuPage, 7)
   htmlParser.doParse()
