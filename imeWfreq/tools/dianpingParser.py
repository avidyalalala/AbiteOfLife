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

class DianpingPage(baseParser.BasePage):
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
	text=""
#soup=self.removeComments(soup)
        #店铺页面,店铺页面所有评论list,用户主页 等页面
        content_div=soup.find("div",{"class":"main"})
	if(content_div is not None):
	    content_div=self.removeScriptTag(content_div)
	    content_div=self.removeComments(content_div)
	    self.content=''.join(content_div.findAll(text=True))
	    return 
	
	
	#店铺页面所有评论list 的单个评论 详情页面
        content_div=soup.find("div",{"class":"content_a"})
	if(content_div is not None):
	    self.content=''.join(content_div.findAll(text=True))
	    return 

	#http://www.dianping.com/search/category/19/80/g5834r16763o8b1	    
        content_div=soup.find("div",{"id":"shop-all-list"})
	if(content_div is not None):
	    self.content=''.join(content_div.findAll(text=True))
	    return 
	return

if __name__=="__main__":
    
   htmlParser=parserDispatcher.ParserDispatcher(sys.argv[1], DianpingPage, 7)
   htmlParser.doParse()
