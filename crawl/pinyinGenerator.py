#!/usr/bin/env python
#coding=utf-8

#author:lalala

import os
import sys 
import re

import codecs

from datetime import date, datetime 
import time

from collections import defaultdict

import common

logger=common.getLogger("pinyin")

'''
duo yin zi Filter
多音字过滤器
'''
class PolyphoneFilter:
    def __init__(self):
        global logger
        self.logger=logger
        common.initEncoding("utf-8")
        self.hanzi_list=self.initHanziTable()
        self.logger.debug(self.hanzi_list[1])

    def containDuoyinzi(self, word):
        for i in range(0,len(word)):
            if(self.isDuoyinzi(word[i])):
                return True         
        return False

    def isDuoyinzi(self, hanzi):
        try:
            _index=self.hanzi_list.index(codecs.encode(hanzi,"utf-8"))
            if(_index>=0):
                return True
        except Exception, err:
            self.logger.debug(Exception)
            self.logger.debug(err)
        return False
                

    def initHanziTable(self):
        rootPath=common.getRootPath()

        #_file=open(rootPath+"/duoyinzi.txt","r")   
        _file=codecs.open(rootPath+"/duoyinzi.txt","r","utf-8")
        return map(lambda x:x.strip(), _file.readlines())
'''
pinyin 
'''
class PinyinGenerator:
    global logger

    def __init__(self):
        self.logger=logger
        common.initEncoding("utf-8")
        self.pinyinDict=self.initPinyinDict()
        self.logger.debug(len(self.pinyinDict))
        
    def initPinyinDict(self):
        pinyinFile=open("./GB18030heteronym.txt","r")   
        pinyinDict=defaultdict(str)

        for line in pinyinFile.readlines():
            arr=re.split(r"\t+",line)
            pinyinDict[arr[0]]=arr[1]

        return pinyinDict

    def getPinyinStr(self, word):
        pinyinStr=()
        pinyinStr=self.pinyinDict[codecs.encode(word[0],"utf-8")]
        for i in range(1,len(word)):
            self.logger.debug(word[i].encode("utf-8"))
            self.logger.debug(self.pinyinDict[word[i].encode("utf-8")])
            pinyinStr+="'"+self.pinyinDict[codecs.encode(word[i],"utf-8")]
        self.logger.debug(pinyinStr)
        return pinyinStr
        

if __name__=="__main__":
    pinyinGenerator=PinyinGenerator()
    
    print(pinyinGenerator.getPinyinStr(codecs.decode("安吉星娜")))
    print(pinyinGenerator.getPinyinStr(codecs.decode("安吉星")))

    poly=PolyphoneFilter()
    print(poly.containDuoyinzi(codecs.decode("安吉星娜","utf-8")))
    print(poly.containDuoyinzi(codecs.decode("安吉星","utf-8")))
