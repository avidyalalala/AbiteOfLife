#!/usr/bin/env python 
#coding=utf-8 
# author:lalala 
import os 
import sys

def main():
    directory="/home/lina/sharedHOME/admin/input-platform/delete_info/0108/"
    files=os.listdir(directory)
    num=0
    #files.sort()
    dest=open("/home/lina/sharedHOME/admin/input-platform/delete_info/0108/deleteInfo1","a")
    for the_file in files:
        print(the_file)
        lines=open(directory+the_file,"r").readlines()
        print(len(lines))
        num=num+len(lines)
        for line in lines:
            line=line.strip()
            dest.write(line+"\r\n")
    dest.close()
    print(num)
    return;

def createFileList(date):
    hostType="sinaEnt"

    tar_dir="/home/lina/sharedHOME/pythonws/temp/"
    tar_file_name=tar_dir+"html.lst."+hostType
    tar=open(tar_file_name,"w")

    input_dir="/home/lina/sharedHOME/pythonws/temp/textDB/html/0/"+date+"/"+hostType
    files=os.listdir(input_dir)
    for _file in files:
        tar.write(input_dir+"/"+_file+"\t"+input_dir.replace("html","rawText")+"\r\n")
        
    print("sucess %s"%(tar_file_name))
    return

def checkMap():
    _map={"a":0,"b":1,"c":2}
    if(_map.get("d") is None):
        print("None")
    if(_map.get("d")==""):
        print("blank")
    return

class Solution:
    def initMap(self):
        self.parenth={'{':'}','(':')','[':']'}
        return
# @return a boolean
    def isValid(self, s):
        s=s.strip()
        if(len(s)<=1):
            return False
        self.initMap()
        for i in range(len(s))[0:len(s)-1]:
            if(i%2==0):
                print(s[i+1])
                print(s[i])
                if(s[i+1]!=self.parenth.get(s[i])):
                    return False
                i=i+1
        return True     

if __name__=="__main__":
    #checkMap()
    #main()
    #createFileList(sys.argv[1])
    s=Solution()
    print(s.isValid("(("))

