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
    
    '''if any of hanzi cannot be zhu yin, the whole word's pinyin will be empty string'''
    def getPinyinStr(self, word):
        pinyinStr=""
        for i in range(0,len(word)):
#            self.logger.debug(word[i].encode("utf-8"))
#            self.logger.debug(self.pinyinDict[word[i].encode("utf-8")])
            pinyin=self.pinyinDict[codecs.encode(word[i],"utf-8")]
            '''if any of hanzi cannot be zhu yin, the whole word's pinyin will be empty string'''
            if(pinyin is None or pinyin ==''):
                return ""   
            pinyinStr+="'"+pinyin
        pinyinStr=pinyinStr[1:len(pinyinStr)]   
        self.logger.debug(pinyinStr)
        return pinyinStr

    def zhuyin(self, _list):
        wors_pinyin_dict={}
        for word in _list:
            pinyin=self.getPinyinStr(word)
            wors_pinyin_dict[word]=pinyin
        self.logger.debug(wors_pinyin_dict)
        return wors_pinyin_dict
                

def zhuyin(_list):
    pinyinGenerator=PinyinGenerator()
    return pinyinGenerator.zhuyin(_list)

if __name__=="__main__":
    pinyinGenerator=PinyinGenerator()
    
    print(pinyinGenerator.zhuyin([codecs.decode("安吉星娜"),codecs.decode("安吉星")]))

