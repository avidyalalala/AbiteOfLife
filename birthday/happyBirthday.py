#!/usr/bin/env python 
#coding=utf-8 
# author:lalala 
import os 
import sys
import re
import time
import codecs
from datetime import date, timedelta, datetime 

def sendMail(mails, bingos, wishes,title):
    if(len(bingos)==0):
        return
    for bingo in bingos:
        print(bingo)
        mails.remove(bingo)
        #print('echo "'+wishes+'"|mail -s "'+title+'" '+" ".join(mails))
        os.system('echo "'+wishes+'"|mail -s "'+title+'" '+" ".join(mails))

    return

if __name__=="__main__":
    
    encoding="gbk"
    if(sys.getdefaultencoding()!=encoding):
        reload(sys)
    sys.setdefaultencoding(encoding)
    #cur_year=datetime.strftime(date.today(),"%Y")
    date_7= date.today()+timedelta(7)
    date_str_7=datetime.strftime(date_7,"%m/%d")
    date_str_1=datetime.strftime(date.today()+timedelta(1),"%m/%d")

    mail_map={}
    name_map={}
    birthday_lines=codecs.open(sys.argv[1],'r',"gbk")
    for line in birthday_lines:
        arr=re.split(r'\s+',line)
        key=arr[0]
        #key=time.strptime(arr[0]+"/"+cur_year,"%m/%d/%Y")
        mail_map[key]=arr[1]
        name_map[key]=arr[2]

    bingo_mails_7=[]
    names_7=""
    bingo_mails_1=[]
    names_1=""
    for _date in name_map.keys():
        if(_date==date_str_7):
            _name=name_map[_date]
            names_7=names_7+_name+" "
            title=names_7+"的生日在7天后,"+_date+"，想想如何吃喝吧:)"
            wishes=title
            bingo_mails_7.append(mail_map[_date])
            sendMail(mail_map.values(), bingo_mails_7, title, wishes)   
        if(_date==date_str_1):
            _name=name_map[_date]
            names_1=names_1+_name+" "
            title=names_1+"的生日就在明天啦，吃货们, 选好地点没有？:)"
            wishes=title
            bingo_mails_1.append(mail_map[_date])
            sendMail(mail_map.values(), bingo_mails_1, title, wishes)   
            #sendMail
