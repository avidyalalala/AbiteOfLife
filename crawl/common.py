#!/usr/bin/env python
#coding=utf-8

#author:lalala

import os
import sys 

import logging
import logging.handlers

def getRootPath():
    return "/home/lina.hou/hotWord"

def getLogger(logName):
    LOG_FILE = getRootPath()+'/hotWords.log'
    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024) # 实例化handler 
    logger = logging.getLogger(logName)    # 获取名为pinyin的logger

    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
    formatter = logging.Formatter(fmt)   # 实例化formatter
    handler.setFormatter(formatter)      # 为handler添加formatter

    logger.addHandler(handler)           # 为logger添加handler
    logger.setLevel(logging.DEBUG)

    return logger

logger=getLogger("common")

def initEncoding(encoding):
    global logger
    if(sys.getdefaultencoding()!=encoding):
        reload(sys)
        sys.setdefaultencoding(encoding)
        logger.debug("the system encoding is "+sys.getdefaultencoding())
    return




