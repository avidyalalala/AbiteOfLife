#!/usr/bin/python
#-*- coding=utf-8 -*-
import httplib
import json
import random
import urllib
import time
import hmac
import base64
from optparse import OptionParser
DEBUGE = True

class HotWords:
    def __init__(self):
        self.WUID = 'hotwordsuszd24l0zewkipri'
        self.WKEY = '3yq{g5Mlg_/UOnk15E?>4V`BSse:'
        self.RUID = 'hotwordsauo98spvcobqapub'
        self.RKEY = 'bFamk4hL#LPxGZ`nDbeFfea;1nu:'
        self.APPID = 'hotwords'
        self.TEST_HOST = '127.0.0.1'
        self.PRODUCTION_HOST = '127.0.0.1'# 
        self.host = self.TEST_HOST
        self.conn = None
        self.method = None
        self.content = None
        self.url = None
        self.headers = {}
    def SetServer(self, host):
        self.host = host
    def SetTestServer(self):
        self.host = self.TEST_HOST
    def SetProductionServer(self):
        self.host = self.PRODUCTION_HOST
    def Connect(self):
        if self.conn:
            self.ReleaseConnection()
        self.conn = httplib.HTTPSConnection(self.host)#,timeout=40)
        self.conn.request(self.method, self.url, self.content, self.headers)
        response = self.conn.getresponse()
        print response.status, response.reason
        data = response.read()
        print data
        return data
    def ReleaseConnection(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def ToUnicode(self, message):
        ret = ""
        print len(unicode(message, "utf-8"))
        for c in message.decode('utf-8'):
            ret += "\\\\u%4X" % ord(c)
        return ret

    def Code(self, message):
        result = ""
        index = 0
        for c in message:
            result += chr(ord(c) ^ (index % 10))
            index += 1
        return result

    def UrlEncode(self,massege):
        return urllib.urlencode({'':massege})[1:]
    def GetGMT(self):
#        return "Sun, 06 May 2012 07:43:59 GMT"
        return time.strftime('%a, %d %b %Y %T GMT' ,time.gmtime())

    def hmac_sha1(self, message, key):
        try:
            import hashlib
            ret = hmac.new(key, message, hashlib.sha1).digest()
        except:
            import sha
            ret = hmac.new(key, message, sha).digest()
        return ret

    def GetRandom(self):
#        return '0.8195501836208747'
        return str(random.random())

    def base64_encode(self, message):
        return base64.b64encode(message)

    def SetHeader(self, uid, key, method, host, url):
        self.headers.clear()
        self.headers["Host"] = host
        self.headers["Url"] = url
        self.headers["X-Sync-Nonce"] = self.GetRandom()
        self.headers["X-Sync-Version"] = "1.0"

        getCanonicalizedSyncHeaders = lambda headers:'\n'.join(['%s' % headers[mkey] for mkey in sorted(headers.keys())])

        canonicalizedSyncHeaders = getCanonicalizedSyncHeaders(self.headers)
        contentType = 'application/json; charset=utf-8'
        date = self.GetGMT()
        baseString = '\n'.join([method, contentType, date, canonicalizedSyncHeaders])
        print baseString.replace('\n','^^^^')
        token = self.hmac_sha1(baseString, key)
        self.headers["Authorization"] = "Sync " + uid + ":" + self.base64_encode(token)
        self.headers["Content-Type"] = contentType
        self.headers["Date"] = date

        if DEBUGE:
            for key in self.headers:
                print key, self.headers[key]

    def AddRecord(self, word):
        self.method = "POST"
        self.url = "/" + self.WUID + "/" + self.APPID
        self.content = '{"__data":{"word":"'+ (word) +'","extra":""}}'
        self.SetHeader(self.WUID, self.Code(self.WKEY), self.method, self.host, self.url)
        self.Connect()

    def GetAllDocList(self):
        self.method = "GET"
        self.url = "/" + self.RUID + "/" + self.APPID + "/?meta=false"
        self.content = ""
        self.SetHeader(self.RUID, self.Code(self.RKEY), self.method, self.host, self.url)
        return self.Connect()

    def GetRecordByDocId(self, docid):
        self.method = "GET"
        self.url = "/" + self.RUID + "/" + self.APPID + "/" + docid
        self.content = ""
        self.SetHeader(self.RUID, self.Code(self.RKEY), self.method, self.host, self.url)
        print self.Connect()

    def GetDocListByRange(self, minkey, maxkey):
        self.method = "GET"
        self.url = "/" + self.RUID + "/" + self.APPID + "/?op=paging&meta=false&sort=docid&reverse=false&count=6&minkey=:" + minkey# +"&minkey=:2999-12-32-00-00-00"
        self.content= ""
        self.SetHeader(self.RUID, self.Code(self.RKEY), self.method, self.host, self.url)
        self.Connect()
		
    def DeleteRecordByDocId(self, docid):
        self.method = "DELETE"
        self.url = "/" + self.WUID + "/" + self.APPID + "/" + docid + "?overwrite=true"
        self.content = ""
        self.SetHeader(self.WUID, self.Code(self.WKEY), self.method, self.host, self.url)
        return self.Connect()

    def DeleteAllRecord(self):
        allList = self.GetAllDocList()
        jsonData = json.loads(allList)
        for item in jsonData["ADD"] + jsonData["UPDATE"]:
            self.DeleteRecordByDocId(item["__docid"])
        pass

    def Clean(self, content):
        self.method = "POST"
        self.url = "/" + self.WUID + "/" + self.APPID + "?op=clean"
        self.content = content.replace("\"ADD\"", "\"LOCAL\"").replace("add","clean").replace("update","clean")
        print self.content
        self.SetHeader(self.WUID, self.Code(self.WKEY), self.method, self.host, self.url)
    def UpdateRecord(selfw):
        pass
    def PrintAllDocList(self):
        allList = self.GetAllDocList()
        jsonData = json.loads(allList)
        for item in jsonData["ADD"] + jsonData["UPDATE"]:
            print '*' * 20
            print 'doc_id : %s' % item["__docid"]
            print 'words : %s' % item['__data']['word']
            print '*' * 20

def opt():
    usage = 'usage: %prog -l|-a word1 word2 ...|-d doc_id|-f filename|-c [-s server_ip|-p|-t]'
    parser = OptionParser(usage=usage)
    parser.add_option('-l',
                    '--list',
                    action='store_true',
                    help="List all of the records in server."
                    )
    parser.add_option('-a',
                    '--add',
                    action="store_true",
                    help='Add words, all the words are seperated spaces.'
                    )
    parser.add_option('-f',
                    '--file',
                    action="store_true",
                    help="Add words from the specified file."
                    )
    parser.add_option('-d',
                    '--delete',
                    action="store_true",
                    help="Delete a doc by the doc_id."
                    )
    parser.add_option('-c',
                    '--clear',
                    action="store_true",
                    help="Clear all of the docs in the server."
                    )
    parser.add_option('-s',
                    '--server',
                    dest="server",
                    help="reset the server ip."
                    )
    parser.add_option('-p',
                    '--production',
                    action="store_true",
                    help="Sync through the production server."
                    )
    parser.add_option('-t',
                    '--test',
                    action="store_true",
                    help="Sync through the test server."
                    )
    return parser#.parse_args()
if __name__ == "__main__":
    parser = opt()
    (options, args) = parser.parse_args()#opt()
    hotwords = HotWords()
    '''set server'''
    if options.test:
        hotwords.SetTestServer()
    elif options.production:
        hotwords.SetProductionServer()
    elif options.server:
        hotwords.SetServer(options.server)
    '''set action'''
    if options.list:
        hotwords.PrintAllDocList()
    elif options.add:
        if len(args) > 0:
            hotwords.AddRecord(" ".join(args))
        else:
            print '词呢？？？'
    elif options.delete:
        if len(args) == 1:
            hotwords.DeleteRecordByDocId(args[0])
        else:
            print '删那条啊？？？'
    elif options.clear:
        hotwords.DeleteAllRecord()
    elif options.file:
        words = open(args[0],"r")
        wordStr = ""
        for word in words:
            wordStr += word.rstrip() + " "
        print wordStr
        hotwords.AddRecord(wordStr)
    else:
        parser.print_help()

