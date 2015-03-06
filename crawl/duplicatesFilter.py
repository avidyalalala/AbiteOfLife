#!/usr/bin/env python
#coding=utf-8

#author:lalala

import os
import sqlite3
import common
import datetime

class SQLiteWrapper:
    
    def __init__(self):
        common.initEncoding("utf-8")
        self.logger=common.getLogger("db")
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

    def insertWord(self, word, pinyin,freq):
        #"insert into lala values('2015-03-03','中文','zhongwen')"
        if((word and pinyin) is None):
            self.logger.debug("insert kong")
            #TODO: throw Exception
            return
        if(freq is None):
            freq=1
        #date("now") and the datetime("now") the built-in method of SQLite
        #to keep date("now") is becuase it is the unite-primary key with word, which means, at the same day, it is forbidden to insert same word
        self.logger.debug(self.c.execute("""insert into hot_word_auto values(date("now"),'%s','%s','%s',datetime("now"))"""% (word,pinyin,freq)))
        self.conn.commit()
        return

    def selectAll(self):
        self.c.execute("select * from hot_word_auto")
        self.logger.debug(self.c.fetchall())
        return self.c.fetchall()

    def selectWordsDeltaDaysAfter(self, delta): 
        date="'"+str(datetime.date.today()-datetime.timedelta(delta))+" 00:00:00'"  
        sql="select * from hot_word_auto where gmt_modified > %s"%(date)
        self.logger.debug(sql)
        self.c.execute(sql)
        self.logger.debug(self.c.fetchall())
        return self.c.fetchall()


if __name__=="__main__":
    dbInstance=SQLiteWrapper()
    try:
        dbInstance.insertWord(word="啦啦啦",pinyin="la la la",freq=1)
    except sqlite3.IntegrityError:
        pass
    #dbInstance.selectAll()
    dbInstance.selectWordsDeltaDaysAfter(7)
