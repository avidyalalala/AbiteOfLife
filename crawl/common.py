#!/usr/bin/env python
#coding=utf-8

#author:lalala

import os
import sys 

import logging
import logging.handlers

def md5(str):
    import hashlib
    m = hashlib.md5()   
    m.update(str.decode("utf-8"))
    return m.hexdigest()

def getRootPath():
    return "/home/admin/hotWord"

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

'''send mail'''
def sendMail(target_file,timeStamp):
    logger.debug("start to send mail")
    mail_address=open(getRootPath()+"/mail_address.txt","r").readlines()
    mail_address=map(lambda x:x.strip()+" ", mail_address)
    #os.system('cat '+target_file.name)
    logger.debug('uuencode '+target_file.name+' '+str(target_file.name)+'|mail -s "hotWords at '+timeStamp+'" '+"".join(mail_address))
    os.system('uuencode '+target_file.name+' '+str(target_file.name)+'|mail -s "hotWords at '+timeStamp+'" '+"".join(mail_address))
 
def listSubtract(fullList, subtractorList):
    for word in subtractorList:
        fullList.remove(word)


def writeLineResult(line, _file):
    _file.writelines(line+"\r\n")
    return

def writeDictResult(_dict, _file):
    for (word,pinyin) in _dict.items():
        writeLineResult(word+"\t"+pinyin,_file)
    return

def writeListResult(_list, _file):
    for single in _list:
        writeLineResult(single, _file)
    return
 
if __name__=="__main__":
    #_file=open("build.sh","r")
    #sendMail(_file,"2015-03-16")
    print(md5("a"))
