#!/usr/bin/env python
#coding=utf-8

#author:lalala

import os
import sys 
import re

import codecs

from datetime import date, datetime 
import time

import logging
import logging.handlers
from collections import defaultdict

class PinyinGenerator:
    global logger

    def __init__(self):
        self.initEncoding("utf-8")
        self.pinyinDict=self.initPinyinDict()
        logger.debug(len(self.pinyinDict))
        
    def initPinyinDict(self):
        pinyinFile=open("./GB18030heteronym.txt","r")   
        pinyinDict=defaultdict(str)

        for line in pinyinFile.readlines():
            arr=re.split(r"\t+",line)
            pinyinDict[arr[0]]=arr[1]

        return pinyinDict

    def getPinyinStr(self, words):
        pinyinStr=()
        pinyinStr=self.pinyinDict[codecs.encode(words[0],"utf-8")]
        for i in range(1,len(words)):
            logger.debug(words[i].encode("utf-8"))
            logger.debug(self.pinyinDict[words[i].encode("utf-8")])
            pinyinStr+="'"+self.pinyinDict[codecs.encode(words[i],"utf-8")]
        logger.debug(pinyinStr)
        return pinyinStr


    def initEncoding(self,encoding):
        if(sys.getdefaultencoding()!=encoding):
            reload(sys)
            sys.setdefaultencoding(encoding)
            logger.debug("the system encoding is "+sys.getdefaultencoding())
        return

logger={}

def initLogging():
    global logger
    LOG_FILE = 'hotWords.log'
    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024) # 实例化handler 
    logger = logging.getLogger('pinyin')    # 获取名为pinyin的logger

    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
    formatter = logging.Formatter(fmt)   # 实例化formatter
    handler.setFormatter(formatter)      # 为handler添加formatter

    logger.addHandler(handler)           # 为logger添加handler
    logger.setLevel(logging.DEBUG)

    return
    
if __name__=="__main__":
    initLogging()
    pinyinGenerator=PinyinGenerator()
    print(pinyinGenerator.getPinyinStr(codecs.decode("安吉星")))
