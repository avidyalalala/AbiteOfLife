#!/usr/bin/env python
#coding=utf-8

#author:lalala
import sqlite3
c={}

def initConn():
    global c
    conn=sqlite3.connect("input_platform.db")
    c=conn.cursor()

def createTable():
    global c
    c.execute("create table lala (date text, word text, pinyin text)")

def insertWord():
    global c
    c.execute("insert into lala values('2015-03-03','中文','zhongwen')")
    return

def selectAll():
    global c
    c.execute("select * from lala")
    print(c.fetchall())
    return c.fetchall()

if __name__=="__main__":
    initConn()
    createTable()
    insertWord()
    selectAll()
    
