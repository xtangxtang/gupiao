# -*- coding: cp936 -*-
# -*- coding:utf-8 -*-

import urllib3
import re
from bs4 import BeautifulSoup 
 
class BlogAttributes:
    def __init__(self,blogId, title, date, readCount, link):
        self.blogId = blogId
        self.title = title
        self.date = date
        self.readCount = readCount
        self.link = link  

    def get_blog_id(self):
        return self.blogId

    def get_title(self):
        return self.title


    def get_date(self):
        return self.date


    def get_read_count(self):
        return self.readCount


    def get_link(self):
        return self.link
 

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  # or whatever

class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()
 
class XLBK:
    def __init__(self,baseUrl,articleTag,fileName):
        self.baseURL=baseUrl
        self.tool=Tool()
        self.file=None
        self.article=1
        self.defaultTitle=u'新浪博客'
        self.articleTag=articleTag
        self.fileName=fileName
 
    def getPage(self,pageNum):
        try:
            url=self.baseURL+str(pageNum)+'.html'
            print("Try to GET: " + url)
            proxy = urllib3.ProxyManager('http://child-prc.intel.com:913/', maxsize=10)
            response= proxy.request('GET',url)
    #             response=conn.urlopen(request)
#             return response.data.decode('utf-8')
            return response.read()
        except TimeoutError as e:
            print ("连接新浪博客失败,错误原因: ",e.reason)
    
    def getTitle(self,page):
        soup = BeautifulSoup(page, 'lxml')
        return soup.title.string
#         pattern = re.compile('blogname.*?blognamespan.*?>(.*?)</span>')
#         spans = soup.find_all('span')
#         for span in spans:
#             result = re.search(pattern,str(span))
#             if result:
#                 print("title:"+result.group(1).strip())
#                 return result.group(1).strip()
#             else:
# #                 print(result)
#                 continue   
#         result = re.search(pattern,page)
#         print("title:"+result.group(1).strip())
#         if result:
#             return result.group(1).strip()
#         else:
#             return None
#  
    def getPageNum(self,page):
        soup = BeautifulSoup(page, 'lxml')
#         print('-------- content ---------------------------------------------------')
#         print(soup.prettify('gb18030'))
#         print('-------- title ---------------------------------------------------')
        spans = soup.find_all('span')
        for span in spans:
#             print(str(span))
            pattern= re.compile('<span style.*?>共(.*?)页</span>')
            result = re.search(pattern,str(span))
            if result:
                print("page numumber:"+result.group(1).strip())
                return result.group(1).strip()
            else:
#                 print(result)
                continue            
#         pattern= re.compile(ur'<span style.*?>共(.*?)页</span>', '.')
#         result = re.search(pattern,page)
#         if result:
#             print("page numumber:"+result.group(1).strip())
#             return result.group(1).strip()
#         else:
#             print(result)
#             return 1
#  
    def getContent(self,page):
        print(page)
        soup = BeautifulSoup(page, 'lxml')
#         print('-------- content ---------------------------------------------------')
#         print(soup.prettify('gb18030'))
#         print('-------- title ---------------------------------------------------')
        divs = soup.find_all('div', attrs={'class': 'articleCell SG_j_linedot1'})
        contents = []
        for div in divs:      
            atc_title_span = div.find('span', attrs={'class': 'atc_title'})
            ahref = atc_title_span.find('a', href=True)
            print(ahref)
            print(ahref.contents[0])
            title = ahref.contents[0]
            link = ahref['href']
            print("title: " + title)
            print("link: " + link)
            
            
            atc_time_span = div.find('span', attrs={'class': 'atc_tm SG_txtc'})
            time = atc_time_span.text
            print("time: " + time)
            
            
            atc_data = div.find('span', attrs={'class':'atc_data'})
            blogId = atc_data.attrs['id']
            blogId = remove_prefix(blogId, 'count_')
            print("blogId: " + blogId)
                        
            print(div)
            
            exit()
        return contents
#  
    def getUrl(self,page):
        pattern =re.compile('<span class="atc_title">.*?<a.*?href="(.*?)">.*?</a>.*?</span>')
        items = re.findall(pattern,page)
        urls = []
        for item in items:
            url = item
            urls.append(url.encode('utf-8'))
            #print url
        return urls
#  
#  
#     def getText(self,url):
#         conn = urllib3.poolmanager()
#         text=conn.request('GET',url).read().decode('utf-8')
#         start=text.find(u"<!-- 正文开始 -->")
#         print(start)
#         end=text.find(u"<!-- 正文结束 -->")
#         print(end)
#         text=text[start:end]
#         text = re.sub(re.compile('<p.*?>'),"\n    ",text)
#         text = re.sub(re.compile('<p>'),"\n    ",text)
#         text=re.sub(r'<(S*?)[^>]*>.*?|<.*? /> ','',text)
#         text=re.sub(r'&[^>]*?\;',' ',text)
#         return text.encode('utf-8')
#  
#     def setFileTitle(self,title):
#         if title is not None:
#             self.file = open(title + ".doc","w")
#         else:
#             self.file = open(self.defaultTitle + ".doc","w")
#  
#  
#     def writeData(self,contents,urls):
#         for item in contents:
#             if self.articleTag == '1':
#  
#                 articleLine = "\n" + str(self.article) + u"--------------------------------------------------------------------------------\n"
#                 self.file.write(articleLine)
#             self.file.write(item)
#             #print item
#             self.file.write(urls[contents.index(item)])
#             #print urls[contents.index(item)]
#             text=self.getText(urls[contents.index(item)])   
#             print(text)
#             self.file.write(str(text))
#             self.article += 1
 
 
    def start(self):
        indexPage = self.getPage(1)
        print("Get index Page: " + indexPage)
        pageNum = self.getPageNum(indexPage)
#         title = self.getTitle(indexPage)
#         self.setFileTitle(self.fileName)
#         if pageNum == None:
#             print("URL已失效，请重试")
#             return
        try:
            print("该博客共有" + str(pageNum) + "页")
            for i in range(int(pageNum)+1, 1, -1):
                print("正在处理第" + str(i) + "页数据")
                page = self.getPage(i)
                contents = self.getContent(page)
#                 urls =self.getUrl(page)
#                 self.writeData(contents,urls)
        except IOError as e:
            print("写入异常，原因" + e.message)
        finally:
            print("写入任务完成")
 
 
 
print("打开一个新浪博客的博文目录\n如http://blog.sina.com.cn/s/articlelist_1866629225_0_1.html \n那么该博客的代号为1866629225_0_   \n请输入博客代号")
baseURL = 'http://blog.sina.com.cn/s/articlelist_1216826604_0_'
articleTag = '1'
fileName='/home/xtang/wu'
xlbk = XLBK(baseURL,articleTag,fileName)
xlbk.start()
