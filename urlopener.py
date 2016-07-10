# -*- coding:utf-8 -*- 
'''
Created on 2016/07/10
中文会乱码？！！？？？

@author: lenovo
'''

import urllib,urllib2,cookielib
import json
from bs4 import BeautifulSoup
from checkgoods import printlist
from string import strip


class MyDataCatcher():
    def __init__(self):
        self.__urldata=json.load(file('urldata.json'),'utf-8')
        self.__url1=self.__urldata.get('dataurl').get('url1')
        
    def getcontent(self,sendurl=''):
        return urllib2.urlopen(self.__url1).read()
    
    def evaluatelogin(self):
        #登录的主页面  
        hosturl = self.__urldata.get('hosturl')
        #post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据）  
        posturl = self.__urldata.get('posturl') 
          
        #设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie  
        cj = cookielib.LWPCookieJar()  
        cookie_support = urllib2.HTTPCookieProcessor(cj)  
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
        urllib2.install_opener(opener)  
          
        #打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功）  
        urllib2.urlopen(hosturl)  
          
        #构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。  
        headers  = self.__urldata.get('headers')
        #构造Post数据，他也是从抓大的包里分析得出的。  
        postData = self.__urldata.get('postData')  
          
        #需要给Post数据编码  
        postData = urllib.urlencode(postData)  
          
        #通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程  
        request = urllib2.Request(posturl, postData, headers)
        urllib2.urlopen(request)  
 
    def beautifulsouphtml(self,htmlcontent=''):   
        soup = BeautifulSoup(file('data.html')) 
        names=list()
        data=dict()
        for tt in soup.body.children:
            if tt.name=='div' and tt.thead!=None:
                for mm in tt.thead.tr:
                    if mm.string!=None:
                        names.append(strip(str(mm.string)))
                for nn in tt.tbody.children:
                    try:
                        templist=list()
                        for qq in nn:
                            if strip(str(qq.string)) not in ['','\n','None']:
                                templist.append(strip(str(qq.string)))
                        data[templist[0]]=templist[1:]
                    except:
                        continue
        printlist(names)
        print '\r'
        for i in data:
            print i,
            printlist(data[i])
            print '\r'
                