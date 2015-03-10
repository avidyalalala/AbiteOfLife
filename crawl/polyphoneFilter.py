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

logger=common.getLogger("duo yin zi")

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
     #   self.logger.debug(self.hanzi_list[1])
    
    '''
    the word contains duo yin zi will be removed from _list.
    meanwhile, returned the be Removed words list
    '''
    def filterDuoyinzi(self, _list):
        beRemoved=[]
        for word in _list:
            re= self.containDuoyinzi(word)
            if(re):
                beRemoved.append(word)
                _list.remove(word)
        return beRemoved

    def containDuoyinzi(self, word):
        for i in range(0,len(word)):
            if(self.isDuoyinzi(word[i])):
                return True         
        return False

    def isDuoyinzi(self, hanzi):
        try:
            zi=codecs.encode(hanzi,"utf-8")
        except UnicodeDecodeError:
            zi=codecs.encode(hanzi,"gbk")

        if zi in self.hanzi_list:
            return True
        return False

    def initHanziTable(self):
        rootPath=common.getRootPath()

        #_file=open(rootPath+"/duoyinzi.txt","r")   
        _file=codecs.open(rootPath+"/duoyinzi.txt","r","utf-8")
        return map(lambda x:x.strip(), _file.readlines())

def filterDuoyinzi(_list):
    poly=PolyphoneFilter()
    return poly.filterDuoyinzi(_list)

def filterLongerThan7(_list):
    beRemoved=[]
    for word in _list:
        if(len(word)>7):
            _list.remove(word)
            beRemoved.append(word)
    logger.debug("longger than 7:")
    logger.debug(beRemoved)
    return beRemoved

if __name__=="__main__":
    poly=PolyphoneFilter()
    print(poly.filterDuoyinzi([codecs.decode("安吉星娜","utf-8"),codecs.decode("安吉星","utf-8")]))
