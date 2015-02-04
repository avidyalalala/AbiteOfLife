#!/usr/bin/env python
#coding=utf-8

#author:lalala

import os
import sys
import re

from imp import reload

import codecs

from datetime import date, timedelta, datetime 
from multiprocessing.dummy import Pool as ThreadPool  


class ParserDispatcher:

    def __init__(self,task_file_name, Parser,howmanydaysago):
        self.task_file_name=task_file_name
        self.paser_class=Parser
        print(Parser)
        self.least_date = date.today() - timedelta(howmanydaysago)
        self.least_date_string = datetime.strftime(self.least_date,'%Y-%m-%d')

        self.init()
        
    def init(self):
    
        print("we are trying to read html file path from "+self.task_file_name)
        #print(self.dest_file)

#self.initEncoding()
	return

    def initEncoding(self):
        if(sys.getdefaultencoding()!='gbk'):
            reload(sys)
            sys.setdefaultencoding('gbk')
            print("the system encoding is "+sys.getdefaultencoding())
        return
    
    def parsePage(self,input_path, outPut_path, least_date):
        ##TODO:do the dispatch according to the host
        the_page=self.paser_class(input_path, outPut_path, least_date)    
        return the_page

    def openTaskFIle(self):
        ##read the task file
        try:
            lines=open(self.task_file_name,"r").readlines()
        except IOError:
            print("cannot find the taskfile ,the program will exit")
            sys.exit(1)
        return lines

    def initThreadPool(self,size):
        return ThreadPool(size)

    def _doParse(self,line):
        try:
	    #print(line)
            re_splits=re.split(r"\s+", line)
	    #print(re_splits)
            input_path=re_splits[0].strip()
            output_path=re_splits[1].strip()
            
            the_page=self.parsePage(input_path, output_path, self.least_date)
	 
	    if(the_page.isQualified is False):
		print("this page is not qualified: %s"%(input_path))
		return
	
	    if(the_page.content.strip()==""):
	    	print("this page is blank: %s"%(input_path))
	    	return

	    #print(the_page.content)
	    #print(the_page.url)
	    #handle the url change into file name
	    #pattern = re.compile(r'(http:)|(https:)|(\/)|(\?)')
	    #name= pattern.sub("", the_page.url)
	    try:
	        output_file=open(the_page.output_dir+the_page.output_name,"w")
	        output_file.write(the_page.content)
	        output_file.close()
	    except UnicodeEncodeError:
	        print("warning:cannot write the result, dueing to encode problem: "+name+"\r\n")
            print("write content into "+output_file.name+" finish!!\r\n")
        except Exception, e:
            print("warning: Error %s for handling this file:%s"%(e,line))
        return

    def doParse(self):
        
        lines=self.openTaskFIle()
	print("process %s threads start at: %s"%(os.getpid(),datetime.now()))
        pool= self.initThreadPool(2)
	for line in lines:
		pool.apply(self._doParse, args=(line,))
#		self._doParse(line)
#pool.map(self._doParse, lines)
	pool.close()
	pool.join()
        print("process %s threads ends at: %s"%(os.getpid(),datetime.now()))
        return;


