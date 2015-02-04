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

class WeiboPage(baseParser.BasePage):
    def __init__(self,input_path, output_path, least_date):
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
        soup=BeautifulSoup(self.rawdata)
        soup=self.removeComments(soup)
	text=""
        #微薄文章页
        content_divs=soup.findAll("div",{"class":"WBA_content"})
        if(content_divs is not None and len(content_divs)>0) :
	    for content_div in content_divs:
	        text=text+''.join(content_div.findAll(text=True))
	else:
	    #个人列表页
	    divs=soup.findAll("div",{"class":"WB_detail"})
	    if(divs is not None and len(divs)>0) :
	        for content_div in divs:
	            text=text+''.join(content_div.findAll(text=True))
        self.content=text
        return 
     
if __name__=="__main__":
    
   htmlParser=parserDispatcher.ParserDispatcher(sys.argv[1], WeiboPage, 7)
   htmlParser.doParse()
