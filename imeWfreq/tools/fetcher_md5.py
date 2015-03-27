#!/usr/bin/env python 
#coding=utf-8 
#author:lalala 
import os
import sys
import common
import re
import urllib2
import threading
import multiprocessing 
from multiprocessing.dummy import Pool as ThreadPool  
from urlparse import urlparse
import itertools
import json

from BeautifulSoup import BeautifulSoup

from datetime import date, timedelta, datetime

dup_hostname="http://10.189.226.214"
dup_url="/input/isDup.htm"

logger=common.getLogger("fetcher")
class TheBeginning:

    def __init__(self,arg_date, conf_file_path, func):
        self._downloadFile=func
        self.host_name='http://dumpcenter.aliyun.com:9999'
        self.index_url = '/pangu_web/localcluster/product/sm_db/client/standard_write/main_output/'
        self.arg_date=arg_date
        self.the_date=datetime.strptime(self.arg_date,'%Y%m%d').strftime('%Y-%m-%d')
#self.hours=["00","01","02","03"]
	self.hours=["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]

        self.root_path=""
        self.configure_file=conf_file_path
        self.output_path_home_list=self.initOutPutPathHomeList(conf_file_path)

        self.pool=None
       
    """read the configure file, which indicates the output directory list
        because those download files will be scattered into different disks
    """
    def initOutPutPathHomeList(self, conf_file_path):
	logger.debug(sys.argv[1]+sys.argv[2]+sys.argv[3]);
        conf_file=open(self.root_path+conf_file_path,"r")
        lines=conf_file.readlines()
        output_path_home_list=[]
        for line in lines:
            output_path_home=line.strip()
            output_path_home_list.append(output_path_home)
        return output_path_home_list

    """divides the task 
    divides the 24 hours into part_size parts
    """
    def taskSplit(self,index,part_size):
        divided=len(self.hours)/part_size
        if(divided==0):
            sys.exit(1)
        begin_index=index*divided
        end_index=begin_index+divided
        the_hours=self.hours[begin_index:end_index]
        if begin_index==divided-1:
            the_hours=self.hours[begin_index:]
            end_index=len(self.hours)
        logger.debug("the part of %s to %s hours:"%(str(begin_index), str(end_index)))
        return the_hours

    def initDownloadProcessPool(self,poolSize):
        #TODO: after add the thread pool,this can be delete into *2
        size=poolSize*2
        logger.debug("create a "+ str(size)+" size process pool to download")
        self.pool = multiprocessing.Pool(processes=size) 
        return

    """create output directory date/hours
        like 20141212/23 
    """
    def prepareFileOutPut(self):
        part_size=len(self.output_path_home_list)
        #part_size=1
        logger.debug("step 1:the task will be divided into "+str(part_size)+" parts")
        
        self.initDownloadProcessPool(part_size)
            
        logger.debug("step 2:24 hours will be divided into:")
        for index in range(part_size):
            #create the directory according to the date
            directory=self.root_path+self.output_path_home_list[index]+"/"+self.arg_date+"/"
            if not os.path.exists(directory):
                os.makedirs(directory)
            logger.debug("task batch: %s "%(str(index)))
            the_hours=self.taskSplit(index,part_size)
            #the_hours=["15"]
            #create the directory according to the hours
            for hour in the_hours:
                logger.debug("step 3 %s:"%(hour))
                self.createIndexPage(directory,hour)
                #start a new Process to do this
                logger.debug("submit a process into processing pool: "+hour)
                logger.debug("downloading at %s"%(directory))
                self.pool.apply_async(self._downloadFile,(directory, hour))
                #self.threadPool.apply_aync(self._downloadFile,(output_dir,))

        self.pool.close()
        self.pool.join()
        return

    """download the index page of each hour
    and analyze the download link of each index page, and save them into the index.info
    """
    def createIndexPage(self, output_dir,hour):

        index_file_name=getIndexFileName(output_dir,hour)
        index_file=open(index_file_name,"w")

        url=self.host_name+self.index_url+self.the_date+"/"+hour+"/"
        logger.debug("read the index of "+url)
        response = urllib2.urlopen(url,timeout=180)
        the_page = response.read()

        soup=BeautifulSoup(the_page)
        oper_tds=soup.findAll("td",{"class":"operation"})
        for td in oper_tds:

            if( td.a is not None):
                downloadLink=td.a['href']
                #print(host_name+downloadLink)
                index_file.write(self.host_name+downloadLink+"\n")
        return


    def main():
        return;

argDate=sys.argv[1]
hostNameMap={}
index_page_name="index.txt"

def getIndexFileName(directory,hour):

    output_dir=directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    index_name=output_dir+"/"+hour+"_"+index_page_name
    return index_name
 
def initHostNameMap(hostName_map_file):

    global hostNameMap

    conf_file=open(hostName_map_file,"r")
    lines=conf_file.readlines()
    hostNameMap={}
    for line in lines:
        _arr=re.split(r'\s+', line)
        hostNameMap[_arr[1]]=_arr[0]
#            for key in hostNameMap.keys():
#                print(key)
#                print(hostNameMap[key])
    return

"""somehow, the python 2.x version have the bug of invoke the method in process
first,shoule put the method outside the class
It heards that python 3.x has already fix this
http://stackoverflow.com/questions/1816958/cant-pickle-type-instancemethod-when-using-pythons-multiprocessing-pool-ma
"""
def downloadFile(index_dir,hour):
    logger.debug("step 4:")
    index_file_name=getIndexFileName(index_dir,hour)
    downloadList=open(index_file_name,"r").readlines()
    
    #os.system("./do_download.sh "+input_index +" "+output_dir)
    #os.system("wget -t 1 -T 600 -i "+input_index +" -o " + sys.argv[3] + " -P " +output_dir)
    
   
    output_dir=index_dir
    logger.debug("process start: %s"%(str(os.getpid()),))
    for download_url in downloadList:
    	do_download_split_classify_write_rawtext(download_url,output_dir)
    #map
    #print("thread pool are closed at: %s by %s"%(str(datetime.now()),str(os.getpid())))
    logger.debug("process end: %s"%(str(os.getpid()),))
    #print(the_page)
    return

def handler(url_outPutDir):
    return do_download_split_classify_write_rawtext(*url_outPutDir)

def do_download_split_classify_write_rawtext(download_url,outPutDir):
    try:
        cur_thread=threading.currentThread()
        logger.debug("step 5:download from url %s"%(download_url))
        logger.debug("by the thread %s, %s"%(cur_thread.getName(),cur_thread.ident))
        file_name=download_url.split("/")[-1].strip()
        response = urllib2.urlopen(download_url, timeout=180)
        re=response.read()
        htmls = re.split("[add]")
        logger.debug("step 6:%s has %s htmls" % (file_name,str(len(htmls)-1)))
	
	size=30
	threadPool=initThreadPool(size)
        for html in htmls[1:]:
            threadPool.apply_async(do_split_classify_write_rawtext, args=(html,outPutDir,file_name,htmls.index(html))).get(timeout=300)
	threadPool.close()
	threadPool.join()
    except Exception, e:
        logger.debug("warning: %s at  %s at do_download_split_classify_write_rawtext:"%(str(e),download_url))
        pass
    return

def do_split_classify_write_rawtext(html,outPutDir,file_name, index):
    htmlcss=html.strip()
    url = getUrl(htmlcss)
    logger.debug("step 7: "+url)

    if(url==""):
	logger.debug("warning: %s: this html has no url"% file_name)
	return
    else:
	full_name=createFileFullName(url,outPutDir,file_name,index)
	if(full_name==""):
	    return
	else:
	    try:
		_md5=common.md5(html)
		logger.debug(dup_hostname+dup_url+"?md5="+_md5)
		result_json=common.getRequest(dup_hostname+dup_url+"?md5="+_md5)
		logger.debug(result_json)
		jo=json.loads(str(result_json))
		'''only if the suceess=true and result=true, we can say the page is duplicated, and we continue into next-time loop'''
		if(jo.get("success") is True and jo.get("result") is True):
		     logger.debug("duplicated")
		     return
	    except Exception, e:
		logger.debug(e)
		pass
	    logger.debug("save file %s"%(full_name))
	    newfile=open(full_name, "w")
	    newfile.write(htmlcss)
	    newfile.close()
    return

def getUrl(rawhtml):
    result=re.search(r'PageMeta.NormalizedUrl=\d+:(\S+)',rawhtml)
    if result is None:
        return ""
    else:
        url=result.group(1)
        return url

def createFileFullName(url, output_dir,file_name,index):

    global hostNameMap
    parsed=urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed)
    domain_dir=hostNameMap.get(domain)
    if(domain_dir is None or domain_dir==""):
        logger.debug("warning: hostname is invalid:"+url)
        return "";
    else:
        directory=output_dir+domain_dir+"/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        logger.debug(directory)
        full_name=directory+file_name+"_"+str(index)

        return full_name

def initThreadPool(poolSize):
    size=poolSize
    return ThreadPool(size)

def main():
    return

if __name__=="__main__":
    initHostNameMap(sys.argv[3])
    theBeginning = TheBeginning(sys.argv[1],sys.argv[2], downloadFile)
    theBeginning.prepareFileOutPut()
    """ assign the hotnamemap the default values"""
    #main()
