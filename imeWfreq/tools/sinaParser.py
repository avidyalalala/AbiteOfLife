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

class SinaPage(baseParser.BasePage):
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
        match_re=re.match(r'\S+\/(\d{4}-\d{1,2}-\d{1,2})\/', self.url)
        if(match_re):
            self.birthday=datetime.date(datetime.strptime(match_re.groups()[0],'%Y-%m-%d'))
        else:
            second_re=re.match(r'\S+\/(\d{8})\/',self.url)
            if(second_re):
                self.birthday=datetime.date(datetime.strptime(second_re.groups()[0],'%Y%m%d'))
                
        #print(self.birthday)
        return self.birthday

    def initQualified(self,date):
        if(self.birthday is None):
            print("Warning:cannot find the birth date of this file:"+self.input_path)
            return
        if(self.birthday>=date):
            self.isQualified=True
        return

    def createOutPutDir(self):
        return baseParser.BasePage.createOutPutDir(self)

    def initOutPutName(self):
        #handle the url change into file name
        pattern = re.compile(r'(http:)|(https:)|(\/)|(\?)')
        name= pattern.sub("", self.url)
        return name

    def initContent(self):
        soup=BeautifulSoup(self.rawdata)
        content_div=soup.find("div",{"id":"artibody"})
        if(content_div is not None):
            content_ps=content_div.findAll("p")
            text=''
            for content_p in content_ps:
                text=text+''.join(content_p.findAll(text=True))
            self.content=text
        return 
     
if __name__=="__main__":
    
   htmlParser=parserDispatcher.ParserDispatcher(sys.argv[1], SinaPage, 7)
   htmlParser.doParse()
