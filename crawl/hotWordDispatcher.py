#!/usr/bin/env python
#coding=utf-8

#author:lalala
import common
from datetime import date, datetime 
import time
import sys
import codecs

import crawler
import pinyinGenerator
import polyphoneFilter
import adminConnector
import duplicatesFilter

logger=common.getLogger("dispatcher")

def writeFileAndSend(send_mail_dict,_file,timeStamp):
    common.writeDictResult(send_mail_dict, _file)
    _file.close()
    '''send mail'''
    common.sendMail(_file, timeStamp)

def doDispatch():

    timeStamp=str(time.strftime("%Y-%m-%d-%H", time.localtime()))

    words_list=crawler.doCrawl(timeStamp)
    '''test code'''
    if(len(sys.argv)>1):
        _file=codecs.open(sys.argv[1],"r","utf-8")
        words_list=map(lambda x:x.strip(), _file.readlines())
    '''test code finish'''
    rootPath=common.getRootPath()
    target_file=open(rootPath+"/hotWords."+timeStamp+".txt","w")
    '''the words will be commited into the hotword admin'''
    words_dict={}
    '''the words will be sent to mail'''
    send_mail_dict={}

    '''filter the words longer than 7'''
    send_mail_dict=polyphoneFilter.filterLongerThan7(words_list)
    '''filter the words list which contains duo yinzi out of the words_list'''
    send_mail_dict.update(polyphoneFilter.filterDuoyinzi(words_list))
    logger.debug("send mail dict:")
    logger.debug(send_mail_dict)

    '''zhuyin'''
    words_dict=pinyinGenerator.zhuyin(words_list)

    '''merge the dict which cannot be zhu yin'''
    copy=words_dict.copy()
    for(word,pinyin) in copy.items():
        if(pinyin==""):
            send_mail_dict[word]="cannot be zhuyin"
            del words_dict[word]
               
    '''is Auto commit switch open'''
    if(adminConnector.isAutoOpen()==0):
        '''manual model'''
        send_mail_dict.update(words_dict)

        writeFileAndSend(send_mail_dict, target_file, timeStamp)
    else:
        '''auto model'''   
        send_mail_dict.update(duplicatesFilter.findDuplicateWords(words_dict))  
        logger.debug("after duplicatesFilter, the words_dict remain:")
        logger.debug(words_dict)
        logger.debug("save words into db:")
        _re=adminConnector.commitHots(words_dict)
        if(_re is True):
            duplicatesFilter.saveHotWords(words_dict)
        else:
            logger.debug("cannot commit hotWords")

        writeFileAndSend(send_mail_dict, target_file, timeStamp)




if __name__=="__main__":

    logger.debug("hotWords starts at: "+str(datetime.now()))
    doDispatch()
    logger.debug("hotWords ends at: "+str(datetime.now()))
