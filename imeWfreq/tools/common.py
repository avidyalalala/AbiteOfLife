#!/usr/bin/env python
#coding=utf-8

#author:lalala

import os
import sys 

import logging
import logging.handlers

import urllib2
import urllib

from datetime import date, timedelta, datetime

def getRootPath():
    return "/disk4/nemo/imeWfreq"

def getLogger(logName):

    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
    formatter = logging.Formatter(fmt)   # 实例化formattertte

    LOG_FILE = getRootPath()+'/log/ime.log.'+str(date.today())
#handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024) # 实例化handler ler
    handler=logging.handlers.TimedRotatingFileHandler(LOG_FILE,"D",1,30)
    handler.suffix="%Y%m%d"
    handler.setFormatter(formatter)      # 为handler添加formattertte

    logger = logging.getLogger(logName)    # 获取名为pinyin的loggergger
    logger.addHandler(handler)           # 为logger添加handlerdle
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

def initRawData(str):
    try:
	rawdata=str.decode("gbk")
    except Exception,e:
	logger.debug(e)
    	try:
	    rawdata=str.decode("utf-8")
    	except Exception, e:
	    logger.debug(e)

    return rawdata
	
def md5(str):
    import hashlib
    m = hashlib.md5()   
    try:
	#why do i need encode again? that is wired
        m.update(initRawData(str).encode("utf-8"))
	md5=m.hexdigest()
    except Exception,e:
	logger.debug(e)
    return md5


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

def getRequest(link, encoding='utf-8'):
    opener=urllib2.build_opener()
    r=opener.open(link)
    text=r.read().decode(encoding)
    return text.encode(encoding)

def postRequest(url, paramDict):
    post_data = urllib.urlencode(paramDict)
    req = urllib2.urlopen(url, post_data)
    content = req.read()
    return content


