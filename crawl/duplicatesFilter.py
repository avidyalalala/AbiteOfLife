#!/usr/bin/env python
#coding=utf-8

#author:lalala

import os
import sqlite3
import common

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

    def insertWord(self, dateStamp, word, pinyin):
        #"insert into lala values('2015-03-03','中文','zhongwen')"
        if((dateStamp and word and pinyin) is None):
            self.logger.debug("insert kong")
            
        self.logger.debug(self.c.execute("insert into hot_word_auto values('%s','%s','%s')"% (dateStamp,word,pinyin)))
        self.conn.commit()
        return

    def selectAll(self):
        self.c.execute("select * from hot_word_auto")
        self.logger.debug(self.c.fetchall())
        return self.c.fetchall()

if __name__=="__main__":
    dbInstance=SQLiteWrapper()
    #dbInstance.createTable("create table hot_word_auto (date text, word text, pinyin text)")
    dbInstance.insertWord("2015-03-03","啦啦啦","lalala")
    dbInstance.selectAll()
    
