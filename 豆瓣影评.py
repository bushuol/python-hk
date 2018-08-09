#爬取《西虹市首富》的前十页长影评
import requests
import time
import re
from lxml import etree


with open('豆瓣影评.txt','w',encoding='utf-8') as f:
    count=0                                          #爬取进度初始化
    for i in range(10):                              #获取前10页的影评
        start_url='https://movie.douban.com/subject/27605698/reviews?start='+str(i*20)
        try:
            #proxies = {'http':'http://118.190.95.35','https':'https://60.6.241.72'}
            kv={"user-agent":"Mozilla/5.0"}
            r=requests.get(start_url,headers=kv,timeout=20)
            r.raise_for_status()
            r.encoding='utf-8'
            html=r.text
        except:
            print("访问错误！")
            
        pagecode=re.findall(r'data-cid="\d+"',html)   #获取完整影评的一个号码
        time.sleep(2)
       
        for k in range(20):                            #获取每一页的完整影评

            N="第{}页第{}篇影评".format(i+1,k+1)
            f.write(N.center(50,"="))
       
            final_url='https://movie.douban.com/j/review/'+pagecode[k][-8:-1]+'/full'
            #print(pagecode[k][-8:-1])
            
            #获得标题
            s=etree.HTML(html)
            b='//*[@id="{}"]/div/h2/a/text()'.format(pagecode[k][-8:-1])
            title=s.xpath(b)

            #获取文本内容
            final_html=requests.get(final_url).text
            text=re.findall(r'body.*vote_',final_html)
            
            author=re.findall(r'data-author=\\".*?\\"',text[0])
            firstp=re.findall(r'<p>.*?<\\/p>',text[0])
            tip=re.findall(r'<p class=.*?<\\/p>',text[0])
            if len(tip)>0:                             #判断剧透提示是否为空
                f.write("\n\n标题：{}\n作者：{}\n提示：{}\n".format(title[0],author[0][14:-2],tip[0][30:-15]))
            else:
                f.write("\n\n标题：{}\n作者：{}\n".format(title[0],author[0][14:-2]))
            time.sleep(2)
            #打印当前爬取进度
            count+=1
            print("\r当前进度：{:.2f}%".format(count/200*100),end='')

            #把每一个<p><\p>中的内容写入正文
            for line in firstp:
                excep1=re.findall(r'<span .*?">',line[3:-5])    #去掉<span>标签
                excep2=re.findall(r'<\\/span>',line[3:-5])
                
                if len(excep1)>0:                   #判断是否有<span>标签
                    lines=line[3:-5].strip(excep1[0]).strip(excep2[0])
                    f.write("{}\n".format(lines))
                else:
                    f.write("{}\n".format(line[3:-5]))
            
            



