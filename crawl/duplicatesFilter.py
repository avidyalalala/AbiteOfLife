#!/usr/bin/env python
#coding=utf-8

#author:lalala

import os
import sqlite3
import common
import datetime

logger=common.getLogger("db")
class SQLiteWrapper:
    
    def __init__(self):
        common.initEncoding("utf-8")
        self.logger=logger
        DB_NAME=common.getRootPath()+"/input_platform.db"
        self.conn=self.initConn(DB_NAME)
        self.c=self.conn.cursor()

    def initConn(self,db_name):
        conn=sqlite3.connect(db_name)
        return conn

    def createTable(self, createTableSQL):
        #"create table lala (date text, word text, pinyin text)"
        self.c.execute(createTableSQL)

    def dropTable(self, tableName):
        self.c.execute("'drop table "+tableName+"'")
    
    def insertHotWordsDict(self,_dict):
        if(len(_dict)==0):
            logger.debug("there is no item in _dict")
        for (k,v) in _dict.items():
            self.logger.debug(self.c.execute("""insert into hot_word_auto values(date("now"),?,?,?,datetime("now"))""",(k,v,1)))
        self.conn.commit()
        return
            

    def insertWord(self, word, pinyin,freq):
        #"insert into lala values('2015-03-03','中文','zhongwen')"
        if((word and pinyin) is None):
            self.logger.debug("insert empty?! why")
            #TODO: throw Exception
            return
        if(freq is None):
            freq=1
        '''date("now") and the datetime("now") the built-in method of SQLite
        to keep date("now") is becuase it is the unite-primary key with word, which means, at the same day, it is forbidden to insert same word
        '''
        #self.logger.debug(self.c.execute("""insert into hot_word_auto values(date("now"),'%s','%s','%s',datetime("now"))"""% (word,pinyin,freq)))
        self.logger.debug(self.c.execute("""insert into hot_word_auto values(date("now"),?,?,?,datetime("now"))""",(word,pinyin,freq)))
        self.conn.commit()
        return

    def selectAll(self):
        self.c.execute("select * from hot_word_auto")
        self.logger.debug(self.c.fetchall())
        return self.c.fetchall()
    '''
    select delta days ago 
    '''
    def selectWordsDeltaDaysAgo(self, delta): 
        date="'"+str(datetime.date.today()-datetime.timedelta(delta))+" 00:00:00'"  
        sql="select * from hot_word_auto where gmt_modified > %s"%(date)
        self.logger.debug(sql)
        self.c.execute(sql)
        _list=self.c.fetchall()
        self.logger.debug(_list)
        return _list
    
    def findRecentWordsList(self):
        _list=self.selectWordsDeltaDaysAgo(7)
        return _list

dbInstance=SQLiteWrapper()

def saveHotWords(_dict):
    return dbInstance.insertHotWordsDict(_dict)
    
def findRecentWords():
    words=[]
    _list=dbInstance.findRecentWordsList()
    for _tuple in _list:
        words.append(_tuple[1])
    logger.debug(words)
    return words

def findDuplicateWords(fullDict):
    oldWords=findRecentWords()   
    duplicates={}
    for old in oldWords:
        if(fullDict.has_key(old)):
            del fullDict[old]
            duplicates[old]="duplicate with week"
    logger.debug("find the duplicate word in 7 days:")
    logger.debug(duplicates)
    return duplicates

if __name__=="__main__":
    dbInstance=SQLiteWrapper()
    try:
        dbInstance.insertWord(word="红包".decode("utf-8"),pinyin="h ong'b ao",freq=1)
    except sqlite3.IntegrityError:
        pass
    #dbInstance.selectAll()
    #findDuplicateWords({"啊红包".decode("utf-8"):"* a'h ong'b ao"})
