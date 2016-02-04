#!/usr/bin/python
#coding=utf-8

import os
import json
import sys
from datetime import datetime
import codecs

def handleCSV(provincePre, providerId, lines, car_prefix_index, vin_index,cen_index, cid_index=None,cpy_index=None):

    for line in lines:

        cells=line.split(",")
        
        _len=len(cells)
        #第三位是车牌号前两位:京A
        prefix2=cells[car_prefix_index]
        
        len_pre=len(prefix2.strip().decode("utf-8"))

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
        #车牌号前两位的前缀对应的规则等 map
        provincePre[provincePrefix]=provincePre.get(provincePrefix,{})
        licenseMap=provincePre[provincePrefix]
        #rules即{"渝":A:{"vin":{0:99,1:4},"cen":{0:5,1:6},"cpy":{2:"chongqing"},cid:4}}中 A字对应的map
        rules=licenseMap.get(licenseLetter2,{})
        licenseMap[licenseLetter2]=rules

        #合并车型易和微车的校验规则，微车是-1 代表输入全部号码，车型易是99代表输入全部号码,
        #车轮的空，代表全部处理成99
        if cells[vin_index]==str(-1) or cells[vin_index].strip()=="":
            cells[vin_index]="99"
        if cells[cen_index]==str(-1) or cells[cen_index].strip()=="":
            cells[cen_index]="99"
        #车轮的csv里居然给的是负整数，需要求绝对值
        vin_rule=abs(int(cells[vin_index]))
        en_rule=abs(int(cells[cen_index]))
        
        rules["vin"]=rules.get("vin",{})
        rules["vin"][providerId]=vin_rule

        rules["cen"]=rules.get("cen",{})
        rules["cen"][providerId]=en_rule
            
        if cpy_index is not None:
            rules["cpy"]=rules.get("cpy",{})
            rules["cpy"][providerId]=cells[cpy_index]

        if cid_index is not None:
            rules["cid"]=cells[cid_index]

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

    chelun_lines=codecs.open("./lib/chelun.csv","r","utf-8").readlines()
    provincePre=handleCSV(provincePre,2,chelun_lines,6,5,4,cid_index=None,cpy_index=2)
    
    dest=open("./json_chexingyi.html","w")
    dest.write("<script>var json='"+json.dumps(provincePre)+"';console.log(json)</script>")
    dest.close()
