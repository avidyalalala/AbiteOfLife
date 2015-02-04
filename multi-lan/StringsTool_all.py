#!/usr/bin/env python
#coding=utf-8

# Copyright(c) 2013 LeWaTek CO., LTD.
# Author: George Zhu(cjzhu@lewatek.com)
#
# All rights are reserved by LeWaTek CO., LTD., whether the whole or
# part of the source code including any modifications.
#
# attention:
#   1. install xdrlib, xlrd, xlwt
#   2. copy zh-rCN to target language
# ChangeLog:
# 2013-8-5 first verion, support one by one module
# 2013-8-7 add directory support
# 2013-8-8 add dir prefix for strings.xls

import xdrlib ,sys
import xlrd
import xlwt
import os
import sys
import re

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import xml.dom.minidom
from xml.dom.minidom import Document

def listApps(lst ,dir):
    files = os.listdir(dir)
    for name in files:
        fullname = os.path.join(dir,name)
        if(os.path.isdir(fullname)):
            lst.append(fullname)

def listFiles(lst ,dir ,wildcard ,recursion):
    exts = wildcard.split(" ")
    files = os.listdir(dir)
    for name in files:
        fullname = os.path.join(dir,name)
        if(os.path.isdir(fullname) and recursion):
            listFiles(lst,fullname,wildcard,recursion)
        else:
            for ext in exts:
                if(name.endswith(ext)):
                    lst.append(name)
                    break

def findApps():
    appList = []
    listApps(appList,'./')
    for app in appList:
        print app


'''
support multi lang and must has base lang (english)
'''
class SourceLoader:
    def __init__(self, path = '.'):
        self.path = path

    def getNameAndValues(self, filename = None):
        '''
        string or array
        <string name="show_dev_countdown">You are now <xliff:g id="step_count">%1$d</xliff:g> steps away from being a developer.</string>
        <string-array name="date_format_values" translatable="false">
            <!-- The blank item means to use whatever the locale calls for. -->
            <item></item>
            <item>MM-dd-yyyy</item>
            <item>dd-MM-yyyy</item>
            <item>yyyy-MM-dd</item>
            <item>EE-MMM-d-yyyy</item>
            <item>EE-d-MMM-yyyy</item>
            <item>yyyy-MMM-d-EE</item>
        </string-array>
        '''

        root = ET.parse(filename).getroot()
        arrayLst = root.findall('string-array')
        stringLst = root.findall('string')

        stringDict = {}

        for elem in arrayLst:
            lst = []
            stringDict[elem.attrib['name']] = lst

            lst.append(elem.text)
            items = elem.findall('item')
            for item in items:
                lst.append(item.text)

        for elem in stringLst:
            stringDict[elem.attrib['name']] = elem.text

        return stringDict

    def listLangFiles(self, dir ,wildcard ,recursion):
        lst = []
        subs = wildcard.split(" ")

        try:
            files = os.listdir(dir)
        except OSError:
            os.mkdir(dir)
            files = os.listdir(dir)
        for name in files:
            fullname=os.path.join(dir,name)
            if(os.path.isdir(fullname) and recursion):
                #print "Test"
                self.listLangFiles(lst,fullname,wildcard,recursion)
            else:
                #print "Jay"
                for sub in subs:
                    if(name.count(sub) > 0 ):
                        lst.append(fullname)
                        break
        return lst


    def loadLangFiles(self, exts = ['','-zh-rCN','-zh-rTW'], base = '', subs = 'string array'):
        self.langDict = {}
        self.base = base

        for ext in exts:
            lst = self.listLangFiles(self.path + '/res/values' + ext + '/', subs, False)
            dct = {}
            for f in lst:
                #key is res/values-zh-rCN/strings.xml
                key = f[f.rindex('res'):]
                dct[key] = self.getNameAndValues(f)

            self.langDict[ext] = dct;

        ###
        ###'./res/values-zh-rCN/strings.xml' 'app_name' 'App Store'
        ###
        print self.langDict
        return self.langDict

    def saveToExcel(self):
        if None == self.langDict:
            print 'None langDict'

        file = xlwt.Workbook();
        sheetName='sheet1'
        table = file.add_sheet(sheetName,cell_overwrite_ok=True)

        col = 0
        row = 1

        baseMap = {}
        print self.base
        baseDct = self.langDict[self.base]
        print '+++++++++baseDct+++++++++++++'
        print baseDct
        print '============================='
        if True:
            dct = baseDct
            print dct.keys()
            for f in dct.keys():
                #file path
                col = 0
                table.write(row, col, f)
                row = row + 1

                lang = dct[f]
                if True:
                    col = 1
                    #string name
                    for key in lang.keys():
                        val = lang[key]

                        if isinstance(val,list):
                            # array
                            print 'baseMap',baseMap
                            baseMap[key] = row #key positin
                            print 'baseMap[key]',baseMap[key]
                            table.write(row, col, key)
                            col = col + 1
                            for value in val:
                                table.write(row, col, value)
                                row = row + 1
                            col = col - 1
                        else:
                            # string
                            baseMap[key] = row

                            table.write(row, col, key)
                            col = col + 1
                            table.write(row, col, val)
                            row = row + 1
                            col = col - 1

        col = 2
        for l in self.langDict.keys():
            dct = self.langDict[l]
            if dct != baseDct:
                col = col + 1
                table.write(0, col, l[1:])
                for f in dct.keys():
                    #file path
                    lang = dct[f]
                    #string name
                    for key in lang.keys():
                        val = lang[key]

                        if baseMap.has_key(key):
                            if isinstance(val,list):
                                # array
                                row = baseMap[key]
                                for value in val:
                                    table.write(row, col, value)
                                    row = row + 1
                            else:
                                # string
                                row = baseMap[key]
                                table.write(row, col, val)

        fullpath = self.path + '/' + getModuleName(self.path) + '_strings.xls'
        file.save(fullpath)
        print 'done! export to ' + fullpath
    #if len(l) == 0:
    #   file.save('strings.xls')
    #else:
    #   file.save(l[1:] + '_strings.xls')


'''
support only one target Lang
'''
class TargetCreator:
    def __init__(self, path = '.', source = 'strings.xls'):
        self.source = source
        self.path = path
        print 'import from ' + self.source + ' to ' + self.path 

    def loadFromExcel(self,targetLang):
        self.target = targetLang

        self.langDict = {}
        try:
            data = xlrd.open_workbook(self.source)
        except:
            print '%s not exists, ignored!' % self.source
            return
        table = data.sheets()[0]

        nrows = table.nrows #行数
        ncols = table.ncols

        #print ncols,nrows

        #
        # langDict = path(2,x) key(x,1) (string/list)(x,?)
        #
        pathMap = {}
        rowbase = 1;

        targetCol = 2
        for colnum in range(2,ncols):
            val = table.cell(0,colnum).value
            if targetLang[1:] == val:
                targetCol = colnum
                break
        #print targetCol

        val = table.cell(1,0).value
        for rowindex in range(2,nrows + 1):
            #print nrows,rowindex
            try:
                valn = table.cell(rowindex,0).value
            except:
                valn = ''
            if len(valn) > 0:
                pathMap[val] = [rowbase,rowindex]
                rowbase = rowindex
                val = valn

        pathMap[val] = [rowbase,nrows]

        for f in pathMap.keys():
            rowbase = pathMap[f][0]
            rowend  = pathMap[f][1]
            #print nrows, rowbase, rowend

            stringDict = {}
            for rowindex in range(rowbase + 1,rowend):
                try:
                    key = table.cell(rowindex,1).value
                except:
                    key = ''

                s = table.cell(rowindex,2).value
                isList =  (len(s.strip()) == 0)
                #print rowindex, s.strip()

                if len(key) > 0:
                    #print rowindex, nrows
                    val = table.cell(rowindex,targetCol).value
                    # TODO:last string
                    #if len(nextkey) > 0 or (rowindex + 1)== nrows:
                    if isList:
                        #array
                        lst = []
                        isInValid = True
                        #TODO
                        for i in range(rowindex + 1,rowindex + 10):
                            try:
                                nextkey = table.cell(i,1).value
                            except:
                                nextkey = ''

                            if len(nextkey) > 0:
                                break

                            try:
                                val = table.cell(i,targetCol).value
                                lst.append(val)
                                if isInValid and len(val) > 0:
                                    isInValid = False
                            except:
                                pass

                        if len(lst) > 0 and not isInValid:
                            stringDict[key] = lst

                    else:
                        #string
                        stringDict[key] = val

            self.langDict[f] = stringDict
        #print stringDict
        #print '------------------------'
        #print f
        #print self.langDict['./res/values/array.xml']

    def __targetFileFromBase(self, basePath):
        if True:
            prefix = basePath[:basePath.index('values') + 6]
            postfix = basePath[basePath.rfind('/'):]
            s = prefix + self.target + postfix
            return s
        return None

    ##
    # Indents an element structure in place.
    #
    # @param elem Element structure.
    def __indent(self, elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            for e in elem:
                self.__indent(e, level+1)
            if not e.tail or not e.tail.strip():
                e.tail = i
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

    '''
    copy from base Lang xml then replace it
    '''
    def saveToXMLs(self):
        # TODO
        # replace and append （copy from base language）
        for base in self.langDict.keys():
        #for base in ['./res/values/array.xml']:
            target = self.path + '/' + self.__targetFileFromBase(base)
            stringDict = self.langDict[base]

            #print base,target,stringDict
            try:
                root = ET.parse(target).getroot()
            except:
                print target + " not exists!!!"
                continue
            tree = ET.ElementTree(root)

            arrayLst = root.findall('string-array')
            stringLst = root.findall('string')

            elementMap = {}

            for elem in arrayLst:
                #print elem.attrib
                name = elem.attrib['name']
                elementMap[name] = elem

            for elem in stringLst:
                name = elem.attrib['name']
                elementMap[name] = elem

            #print len(elementMap)
            #print len(stringDict)

            # let's update
            for key in stringDict.keys():
                if elementMap.has_key(key):
                    e = elementMap[key]
                else:
                    e = None

                val = stringDict[key]
                isList =  isinstance(val,list)
                #print key
                if e == None:
                    ''' if isList:
                        e = ET.Element('string-array')
                    else:
                        e = ET.Element('string')
                    e.attrib['name'] = key
                    root.append(e) '''
                # TODO
                else:
                    # update value
                    if isList:
                        for child in e.getchildren():
                            e.remove(child)

                        lst = val
                        #print lst
                        for i in lst:
                            item = ET.Element('item')
                            item.text = i
                            e.append(item)
                    else:
                        if len(val) > 0:
                            e.text = val

            self.__indent(root)
            tree.write(target, encoding="utf-8",xml_declaration=True)

            # TODO:indent xml
            # xmlfile =
            # xmldoc = minidom.parse(xmlfile)

            print 'done with '+ target
        #self.__saveXML(root, target)


def doExport(path, langList):
    loader = SourceLoader(path)
    lst = ['']
    lst[1:] = langList
    loader.loadLangFiles(lst)
    loader.saveToExcel()

def  doImport(path, source, lang):
    creator = TargetCreator(path, source)
    creator.loadFromExcel(lang)
    creator.saveToXMLs()

def getModuleName(s):
    try:
        mname =  s[s.rindex('/') + 1:]
    except:
        mname = ''
    return mname

def getSourcePath(list,dir):
    if os.path.isdir(dir):
        for item in os.listdir(dir):

            if item == "res":
                list.append(dir)
                return list
                break
            else:
                path = os.path.join(dir,item)
                local = getSourcePath(list,path)
    return list


def main():
    print 'CommandLine:'
    print sys.argv

    #print getModuleName("./apps/Settings")

    if len(sys.argv) <= 2:
        print '''Usage:
import to Android resource file: python StringsTool.py ./apps/SystemClean -i -zh-rTW
export to string.xls: python StringsTool.py ./apps/SystemClean -e -zh-rCN -zh-rTW
by George Zhu 2013-8-5'''

    else:
        if sys.argv[1] == '-e' or sys.argv[1] == '-i':
            path = os.getcwd()
            if not os.path.exists("%s/temp" % path):
                print "%s/temp" % path
                os.makedirs("%s/temp" % path)
            list = []
            path_list = getSourcePath(list,dir=path)
            print path
            print path_list
            for p in path_list:
                if sys.argv[1] == '-e':
                    doExport(p,sys.argv[2:])
                    os.system('mv %s/*.xls %s/temp'% (p,path ))
                elif sys.argv[1] == '-i':
                    doImport(p, ("%s/%s_strings.xls" % (sys.argv[3], getModuleName(p))), sys.argv[2])
        else:
            path = sys.argv[1]
            if path[len(path) - 1] == '/':
                path = path[:len(path) - 1]

            if sys.argv[2] == '-i' and len(sys.argv) == 4:
                doImport(path, sys.argv[3])
            elif sys.argv[2] == '-e' and len(sys.argv) >=4 :
                doExport(path, sys.argv[3:])

    return

if __name__=="__main__":
    main()


