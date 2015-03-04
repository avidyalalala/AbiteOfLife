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

class PinyinGenerator:

    def __init__(self):
        self.logger=common.getLogger("pinyin")
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

    def getPinyinStr(self, words):
        pinyinStr=()
        pinyinStr=self.pinyinDict[codecs.encode(words[0],"utf-8")]
        for i in range(1,len(words)):
            self.logger.debug(words[i].encode("utf-8"))
            self.logger.debug(self.pinyinDict[words[i].encode("utf-8")])
            pinyinStr+="'"+self.pinyinDict[codecs.encode(words[i],"utf-8")]
        self.logger.debug(pinyinStr)
        return pinyinStr

if __name__=="__main__":
    pinyinGenerator=PinyinGenerator()
    print(pinyinGenerator.getPinyinStr(codecs.decode("安吉星")))
