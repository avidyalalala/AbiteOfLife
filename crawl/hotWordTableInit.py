#!/usr/bin/env python
#coding=utf-8

#author:lalala

import os
import sqlite3
import common
import duplicatesFilter

def initHotWordTable():
    return

if __name__=="__main__":
    dbInstance=duplicatesFilter.SQLiteWrapper()
    dbInstance.createTable('''create table hot_word_auto (date text NOT NULL,
        word text NOT NULL, 
        pinyin text NOT NULL,
        freq int,
        gmt_modified text not null,
        constraint pk_t2 primary key (date,word)
       )''')
    
