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
    print(dbInstance.selectAll())
