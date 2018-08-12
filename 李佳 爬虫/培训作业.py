#!/usr/bin/env python
import urllib
import urllib.request
import urllib.parse
from lxml import etree
import os
import requests
import sys
def loadPage(url,kw):
    """
        作用：根据url发送请求，获取服务器响应文件
        url: 需要爬取的url地址
    """
    request = urllib.request.Request(url)
    html = urllib.request.urlopen(request).read()
    # 解析HTML文档为HTML DOM模型
    content = etree.HTML(html)
    #print content
    # 返回所有匹配成功的列表集合
    link_list = content.xpath('//div[@class="t_con cleafix"]/div/div/div/a/@href')
    #link_list = content.xpath('//a[@class="j_th_tit"]/@href')
    for link in link_list:
        fulllink = "http://tieba.baidu.com" + link
        # 组合为每个帖子的链接
        #print link
        loadImage(fulllink,kw)
# 取出每个帖子里的每个图片连接
def loadImage(link,kw):
    headers = {"User-Agent" : "Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0;"}
    request = urllib.request.Request(link, headers = headers)
    html = urllib.request.urlopen(request).read()
    # 解析
    content = etree.HTML(html)
    # 取出帖子里每层层主发送的图片连接集合
    #link_list = content.xpath('//img[@class="BDE_Image"]/@src')
    link_list = content.xpath('//div/img[@class="BDE_Image"]/@src')
    #link_list = content.xpath('//img[@class="BDE_Image"]/@src')
    # 取出每个图片的连接
    for link in link_list:
        #print(link)
        writeImage(link,kw)
def writeImage(link,kw):
    """
        作用：将html内容写入到本地
        link：图片连接
    """
    #print "正在保存 " + filename
    headers = {"User-Agent" : "Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0;"}
    # 文件写入
    #request = urllib.request.Request(link, headers = headers)
    request = requests.get(link,headers=headers,stream=True)
    # 图片原始数据
    #image = urllib.request.urlopen(request)
    #image1 = image.read()
    #print(image.headers['content-length'])
    # 取出连接后10位做为文件名
    filename = link[-10:]
    if kw not in os.listdir():
        os.mkdir(kw)
    # 写入到本地磁盘文件内
    filename = os.path.join(kw,filename)
    size = 0
    chunk_size = 1024
    content_size = int(request.headers['content-length'])
    sys.stdout.write('[文件大小]:%0.2f MB\n' % (content_size / chunk_size / 1024))
    with open(filename,'wb') as file:
        for data in request.iter_content(chunk_size=chunk_size):
            file.write(data)
            size += len(data)
            file.flush()
            sys.stdout.write('[下载进度]:%.2f%%' % float(size / content_size * 100) + '\r')
            sys.stdout.flush()
    print("已经成功下载 "+ filename)
def tiebaSpider(url, beginPage, endPage,kw):
    """
        作用：贴吧爬虫调度器，负责组合处理每个页面的url
        url : 贴吧url的前部分
        beginPage : 起始页
        endPage : 结束页
    """
    for page in range(beginPage, endPage + 1):
        pn = (page - 1) * 50
        #filename = "第" + str(page) + "页.html"
        fullurl = url + "&pn=" + str(pn)
        #print fullurl
        loadPage(fullurl,kw)
        #print html
        print("谢谢使用")
def hello():
    print('=' * 100)
    print('\t\t\t\t贴吧图片下载')
    print('\t\t作者：八戒,为师想吃猪头肉')
    print('=' * 100)
if __name__ == "__main__":
    hello()
    kw = input("请输入需要爬取的贴吧名:")
    beginPage = int(input("请输入起始页："))
    endPage = int(input("请输入结束页："))
    url = "http://tieba.baidu.com/f?"
    key = urllib.parse.urlencode({"kw": kw})
    fullurl = url + key
    tiebaSpider(fullurl, beginPage, endPage,kw)