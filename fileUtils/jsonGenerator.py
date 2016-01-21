#!/usr/bin/python
#coding=utf-8

import os
import json
import sys
from datetime import datetime
import codecs

def handleCSV(provincePre, providerId, lines, car_prefix_index, vin_index,cen_index, cid_index):

    for line in lines:

        cells=line.split(",")
        _len=len(cells)
        #第三位是车牌号前两位:京A
        prefix2=cells[car_prefix_index]
        
        len_pre=len(prefix2.decode("utf-8"))

        if 0>len_pre>2:
            print(len_pre)
            print(prefix2)
            sys.exit(1)

        provincePrefix=prefix2[0]
        #直辖市
        if len_pre==1:
            licenseLetter2="all"
            print(provincePrefix)
        else:
            licenseLetter2=prefix2[1]

        #车牌号第一位与第二位的对应关系 
        #licenseMap即{"渝":A:{"vin":{0:99...}}}中 渝字对应的map
        licenseMap=provincePre.get(provincePrefix,{})
        if licenseMap =={} or licenseMap.get(licenseLetter2,"")=="":
            rules={}
            temp={}
            temp[providerId]=cells[vin_index]
            rules["vin"]=temp
            temp1={}
            temp1[providerId]=cells[cen_index]
            rules["cen"]=temp1

            rules["cid"]=cells[cid_index]

            licenseMap[licenseLetter2]=rules
        else:
            #"渝": { "A": { "vin": {0: 99, 1: -1}, "cen": {0: 8, 1: 8}, "ci": 70, "cn": "南京" },
            #rules 即 A 对应的map
            rules=licenseMap.get(licenseLetter2)
            rules.get("vin")[providerId]=cells[vin_index]
            rules.get("cen")[providerId]=cells[cen_index]
            licenseMap[licenseLetter2]=rules
       
        #车牌号前两位的前缀对应的规则等 map
        provincePre[provincePrefix]=licenseMap
    return provincePre

if __name__=="__main__":
    if(sys.getdefaultencoding()!='utf-8'):
        reload(sys)
        sys.setdefaultencoding('utf-8')
    chexingyi_lines=codecs.open("./lib/chexingyi.csv","r","utf-8").readlines()
    #最外层以省前缀开头的字典map
    provincePre={}
    providerId=0
    provincePre=handleCSV(provincePre,providerId,chexingyi_lines,3,5,6,4)
    weiche_lines=codecs.open("./lib/weiche.csv","r","utf-8").readlines()
    provincePre=handleCSV(provincePre,1,weiche_lines,6,0,1,7)

       #dest=open("./json_chexingyi"+str(datetime.now()).split(" ")[1]+".html","w")
    dest=open("./json_chexingyi.html","w")
    dest.write("<script>var json='"+json.dumps(provincePre)+"';console.log(json)</script>")
    dest.close()
