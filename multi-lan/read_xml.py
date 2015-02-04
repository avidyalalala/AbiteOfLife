#!/usr/bin/env python
#coding=utf-8

# author:lalala

import os
import sys
import re

import xml.dom.minidom  
from xml.dom.minidom import Document 
from imp import reload

def main():
	if(sys.getdefaultencoding()!='utf-8'):
		reload(sys)
		sys.setdefaultencoding('utf-8')

	print ("你好 世界")
	print (sys.getdefaultencoding())  
	
	path="./input/"

	files = os.listdir(path)
	dest_file=open("lalala.csv","w")
	for name in files:
		if(name.endswith(".xml")):
			print (name)
			doc=xml.dom.minidom.parse(path+name)
			for node in doc.getElementsByTagName("string"):
				attri=node.getAttribute("name")
				while(node is not None and node.nodeType!=node.TEXT_NODE):
					node=node.firstChild
				## this if expression is for handling this kind of situation:  <string name="reg_success_desc2"></string>
				if(node is not None):
					value=node.data
				print(value)
				dest_file.write(attri+","+value+"\n")
	dest_file.close()
	return;


if __name__=="__main__":
	main()

