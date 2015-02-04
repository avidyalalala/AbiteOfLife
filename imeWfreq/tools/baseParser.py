#!/usr/bin/env python
#coding=utf-8

#author:lalala

import os
import sys
import re

from BeautifulSoup import BeautifulSoup,Comment

import xml.dom.minidom  
from xml.dom.minidom import Document 
from imp import reload

import codecs

import parserDispatcher

from datetime import date, timedelta, datetime 

class BasePage:
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

    def initEncoding(self):
        return self._initEncoding('utf-8')

    def _initEncoding(self, encoding):
        #all the file should be outputted by utf-8 encoding
        if(sys.getdefaultencoding()!=encoding):
            reload(sys)
            sys.setdefaultencoding(encoding)
            print("the system encoding is "+sys.getdefaultencoding())
        return

    def init(self,least_date):
	self.initEncoding()
        self.initRawData()
        #check if this file exist,and be opened, and is it empty
        if(self.rawdata):
            self.initUrl()
            self.initBirthDay()
            self.initQualified(least_date)
            #check if this file's birth date is satisfied
            if(self.isQualified):
                self.output_dir=self.createOutPutDir()
                self.output_name=self.initOutPutName()
                self.initContent()
        return

    def readRawText(self):
        buffer = []
        fh = codecs.open(self.input_path, "r", "utf-8")
        buffer.append(fh.read())
        fh.close()
        print repr(buffer)

    def initRawData(self):
        #self.readRawText()
        try:
            self.rawdata=codecs.open(self.input_path,"r","gbk").read()
        except UnicodeDecodeError:
            try:
                self.rawdata=codecs.open(self.input_path,"r","utf-8").read()
            except:
                print("warning: %s cannot be decode"%self.input_path)
            #except UnicodeDecodeError:
            #    self.rawdata=open(self.input_path,"r").read()
                #print("cannot decode this file "+ self.input_path)
        except IOError:
            print("warning:this file is not exist "+ self.input_path)

        return

    def initUrl(self):
        urls=re.findall(r'PageMeta.NormalizedUrl=\d+:(\S+)',self.rawdata,re.S)

        #every input_path is one htmlpage
        if(urls):
            self.url=urls[0]
            #print("the url of this page is: ")  
            print(self.url)
        else:
            print("warning:cannot find url in this file:"+self.input_path)
            return
        return

    def initBirthDay(self):
        self.birthday=date.today() - timedelta(1)
        return self.birthday

    def initQualified(self,date):
        self.isQualified=True
        return

    def createOutPutDir(self):
#timeStampDirectory=datetime.strftime(self.birthday,'%Y%m%d')
        the_dir=self.output_path+"/"
        if not os.path.exists(the_dir):
            os.makedirs(the_dir)
        self.output_dir=the_dir
        #print(self.output_dir)
        return self.output_dir

    def initOutPutName(self):
        #return self.input_path.split("/")[-1]
        pattern = re.compile(r'(http:)|(https:)|(\/)|(\?)')
        name= pattern.sub("", self.url)
        return name

    #strip all the comments
    def removeComments(self, soup):
        comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        [comment.extract() for comment in comments]
        return soup

    #strip all the style tag
    def removeStyleTag(self,soup):
        styles=soup.findAll("style")
        for style_tag in styles:
            style_tag.extract()
        return soup
    
    #strip all the script tag
    def removeScriptTag(self,soup):
        scripts=soup.findAll("script")
        for script_tag in scripts:
            #script_tag.replaceWith("")
            script_tag.extract()
        return soup

    def removeLinkNoContent(self,soup):
        onclicks=soup.findAll(onclick=True)
        notLinks=soup.findAll(href="#")
        for _a in onclicks+notLinks:
            _a.extract()
        return soup

    def getTextFromHtmlNodes(self, nodes):
	text=""
    	if(nodes is not None and len(nodes)>0) :
	    for node in nodes:
		text=text+''.join(node.findAll(text=True))
	return text.strip()

    def initContent(self):
        #in case the file includes multiple htmls
        htmls=self.rawdata.split("[add]")
        text=''
        for html in htmls:
            soup=BeautifulSoup(html)
            soup=self.removeComments(soup)
            soup=self.removeStyleTag(soup)
            soup=self.removeScriptTag(soup)
            content_body=soup.find("body")
            if(content_body is not None):
                content = content_body
                text=text+''.join(content.findAll(text=True))
        self.content=text
        return 
     
       

def main():
    return

if __name__=="__main__":
    print(datetime.now())
    htmlParser=parserDispatcher.ParserDispatcher(sys.argv[1], BasePage,7)
    htmlParser.doParse()
