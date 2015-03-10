#!/usr/bin/env python
#coding=utf-8

#author:lalala

import os
import sys 
import re

import codecs

from datetime import date, datetime 

import time
import urllib2,urllib
import json

import logging
import common

logger=common.getLogger("admin connector")

hostName="http://10.189.226.214"
#hostName="http://localhost:8080"
isAutoOpenLink="/input/hotword/autoflag.html"
hotWordsCommitLink="/admin/hot/add/json.html"
'''?hotsJson={%22hotWordsList%22:[{%22extra%22:{%22freq%22:1,%22pinyin%22:%22x+in%27q+ing%27m+ing%27sh+ang%27h+e%27t+u%22},%22word%22:%22%E6%96%B0%E6%B8%85%E6%98%8E%E4%B8%8A%E6%B2%B3%E5%9B%BE%22}],%22interval%22:1}
'''

def requestIt(link, encoding='utf-8'):
    opener=urllib2.build_opener()
    r=opener.open(link)
    text=r.read().decode(encoding)
    return text.encode(encoding)

def postRequest(url, paramDict):
    post_data = urllib.urlencode(paramDict)
    req = urllib2.urlopen(url, post_data)
    content = req.read()
    return content

def buidHotJson(_dict):
    _list=[]
    hotsdict={}
    for (word,pinyin) in _dict.items():
        extra={}
        extra["pinyin"]=pinyin
        extra["freq"]=1
        single={"extra":extra,"word":word}
        _list.append(single)
    hotsdict={"hotWordsList":_list,"interval":1}
    return json.dumps(hotsdict)

def isCommitSucccess(jsonStr):
    jo=json.loads(str(jsonStr))
    #print(jo)
    if(jo.get("success")=="true"):
        return True
    else:
        return False

def commitHots(_dict):
    if(len(_dict)==0):
        logger.debug("u commit an empty hot words list")
        return False
    json=buidHotJson(_dict)
    logger.debug(json)
    param={'hotsJson':json}
    url=hostName+hotWordsCommitLink
    #url=hostName+hotWordsCommitLink+"?hotsJson="+urllib.urlencode(json)
    try:
        logger.debug("prepare to commit hot words:")
        logger.debug(url)
        #_re=requestIt(url)
        logger.debug(param)
        _re=postRequest(url, param)
        logger.debug(_re)
        return isCommitSucccess(_re.strip())
    except Exception, err:
        logger.debug(err)
        pass
    return False

'''
0: manual operation;
1: auto operation model
'''
def isAutoOpen():
    flag=0
    try:
        url=hostName+isAutoOpenLink
        logger.debug("visit the auto switch interface:")
        logger.debug(url)
        flag=int(requestIt(url).strip())
        logger.debug(flag)
    except Exception, err:
        logger.debug(err)
        pass
    return flag


if __name__=="__main__":
    #print(commitHots({"啊红包".decode("utf-8"):"* a'h ong'b ao"}))
    isCommitSucccess("")
