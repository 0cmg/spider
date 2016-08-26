# -*- coding:UTF-8 -*-
#Author:周文康
import time
import requests
import sys
from bs4 import BeautifulSoup
from time import ctime,sleep
import threading
import Queue
import random
import codecs
import json
start = time.clock()
reload(sys)
sys.setdefaultencoding('utf-8')



# Message()

class Message:
    def __init__(self,book_link,name,book_image,book_info,content,booktags,star_dicts,rate_num,rate_peo):
        self.book_link=book_link
        self.name=name
        self.book_image=book_image
        self.book_info = book_info
        self.content=content
        self.booktags=booktags
        self.star_dicts=star_dicts
        self.rate_num=rate_num
        self.rate_peo=rate_peo
        print self.book_link
    def packdd(self):
        try:
            print self.name
        except Exception:
            print 'this is error but it is ok'
        dicts = {}
        dicts["book_link"] = self.book_link
        dicts["book_name"]=self.name
        dicts["book_image"]=self.book_image
        dicts["book_info"]=self.book_info
        dicts["content_intro"]=self.content
        dicts["book_tags"]=self.booktags
        dicts["rate"]={}
        dicts["rate"]['rate_num']=self.rate_num
        dicts["rate"]['rate_peo']=self.rate_peo
        dicts["rate"]['rate_star']=self.star_dicts
        # print dicts
        return dicts

#信息返回格式
#{"bookname":"xxx","book_image":"xxxx","content_intro":"xxx","booktags":"xxx","rate":{"rate_num":"xxx","rate_peo":"xxx","rate_star":{"star_five":"xxx","star_four":"xxx","star_three":"xxx","star_two":"xxx","star_one":"xxx"}}}



def getHtmlInfo(urls,ref):
    global starts
    #简单获取
    ##
    # f = codecs.open('hahaha.html','a+',encoding='UTF-8')
    starts = time.clock()
    headers = [
           {'User-Agent': 'Mozilla/6.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
           {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
           {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
           {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
           {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
    ]
    # url = u'https://book.douban.com/subject/'+str(ids)
    try:
        header = random.choice(headers)
        header['Referer']= ref
        ContentPage_Info = requests.get(urls,headers=header)
    except Exception:
        header = random.choice(headers)
        header['Referer']= ref
        ContentPage_Info = requests.get(urls,headers=header)

    sleep(1)
    print ContentPage_Info.history
    return ContentPage_Info

    #计算网页获取速度
def HandleInfo(Book_Url,ContentPage_Info):
    Page_Html = BeautifulSoup(ContentPage_Info.content)
    #bookname
    try:
        bookname = Page_Html.title.string
    finally:
        bookname = Page_Html.title.string
    #bookimage
    try:
        book_image = Page_Html.select('#mainpic > a')[0].attrs['href']
    except Exception:
        book_image=''
    # print ContentPage_Info
    #书本信息处理后
    # print Page_Html.find_all("div")
    # print Page_Html.select("#info")
    try:
        book_info = Page_Html.select("#info")[0].get_text().replace('-',':').replace(' ','').replace('\n','-').replace('---','').replace('--','-')
        booktags = Page_Html.select('#db-tags-section .indent > span')
    except Exception:
        if str(ContentPage_Info.history[0]) =="<Response [302]>":
            book_info=''
            book_tags=''
        else:
            book_info=''
            book_tags=''
    bookt = []
    for i in xrange(len(booktags)):
        bookt.append(booktags[i].get_text().replace(' ','').replace('\n','').replace(u'\xa0',u''))
    booktags = ','.join(bookt)
    # 书本标签    


    try:
        #评分人数
          rate_peo = Page_Html.select('#interest_sectl > div > div > strong')[0].get_text() 
          #评分
          rate_num= Page_Html.select('#interest_sectl .rating_sum > span > a > span')[0].get_text()
          Page_Htmls = Page_Html.find('div',id='interest_sectl')
          Star_Info  = Page_Htmls.find_all("span")
          star_list=[u'star_five',u'star_four',u'star_three',u'star_two',u'star_one']
          rate_list=[]
          for i in xrange(3,len(Star_Info)):
              if not i%2:
                  rate_list.append(Star_Info[i].get_text().replace('\n','').replace(' ',''))
              # 星星 
          # print star_list
          # print rate_list
          dicts = zip(star_list,rate_list)
    except Exception:
          rate_peo=Page_Html.select('.rating_sum > span > a ')[0].get_text() 
          rate_num=rate_peo
          dicts = {'rate_msg':rate_peo}
    try:
        content = Page_Html.select('#link-report > div .intro')[0].get_text().replace('\n','')
    except IndexError:
        try:
            content=Page_Html.select('.intro')[0].get_text().replace('\n','')
        except Exception:
            content=''
    #书本简要描述

    aa = Message(Book_Url,bookname,book_image,book_info,content,booktags,dicts,rate_num,rate_peo)
    ccc = aa.packdd()
    return ccc



def makeUrl(values):
    url = 'https://book.douban.com/tag/随笔?start='+str((values*20))+'&type=T'
    # print url
    print url
    return url

def getUrl():
    print 'start'
    global queues
    t=0
    while t < 1:
        for z in xrange(17,100):
            sleep(1)
            urls = makeUrl(z)
            a = getUrls(urls)
            if a:
                for i in xrange(0,len(a)):
                    queues.put(a[i].attrs['href'])
            else:
                break
            print queues.qsize()
        t+=1
        
    return 

def getUrls(url):
    headers = [
           {'User-Agent': 'Mozilla/6.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
           {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
           {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
           {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
           {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
           {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
    ]
    # print url
    try:
        r=requests.get(url,headers=random.choice(headers))
    except Exception:
        r=requests.get(url,headers=random.choice(headers))
    else:
        r=requests.get(url,headers=random.choice(headers))
    soup =BeautifulSoup(r.content)
    # print r.content
    if soup.select('.info') !='[]':
        infourl = soup.select('.info > h2 > a')
    else:
        return False
    return infourl


def aaa():
    # sleep(5)
    global starts
    global queues
    while(queues.qsize()>0):
        Url_Page = queues.get()
        ffff = HandleInfo(Url_Page,getHtmlInfo(Url_Page,'https://book.douban.com/tag/%E9%9A%8F%E7%AC%94'))
        f = open('hahaha.txt','a+')
        f.write(json.dumps(ffff,ensure_ascii=False)+'\n')
        f.close()
        ends = time.clock()
        print 'OnePage time: %s Seconds'%(ends-starts)

# url = 'https://book.douban.com/subject/4031698/'
# HandleInfo(url,getHtmlInfo(url,''))
queues = Queue.Queue()
getUrl()
aaa()

# print header
end = time.clock()
print 'Running time: %s Seconds'%(end-start)