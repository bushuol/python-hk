#爬取百度贴吧的图片
import requests
import time
import os
import re

'''
//*[@id="post_content_121346016057"]/img[1]
贴吧：https://tieba.baidu.com/f?kw=秦时明月&ie=utf-8&pn=50
贴吧某贴：'https://tieba.baidu.com/p/'+tie_code+'?pn=2'
tie_code:  //*[@id="thread_list"]/li[9]/div/div[2]/div[1]/div[1]/a/@href
//*[@id="thread_list"]/li[15]/div/div[2]/div[1]/div[1]/a
//*[@id="thread_list"]/li[33]/div/div[2]/div[1]/div[1]/a
图片：//*[@id="post_content_121239415051"]/img[5]
图片链接：pic_link=re.findall(r'"BDE_Image" .*?jpg')[i][18:]
存储：path=piclink.split('/')[-1]
评论：//*[@id="post_content_120779535517"]
re.findall(r'j_d_post_content.*?>
'''
#获取网页内容
def getHtmlText(url):
    try:
        kv={"User-Agent":"Mozilla/5.0"}
        r=requests.get(url,headers=kv,timeout=30)
        r.raise_for_status
        r.encoding="utf-8"
        return r.text
    except:
        print("访问出错！")

#解析某个贴吧网页，提取信息，获得每个帖的url
#贴吧的每个帖子的url中有一个十位数的号码，我们获取这一种号码，以此来构成每个帖的url
def getTie_code(kw,tie_code,start_pn=0,end_pn=1):
    base_url='https://tieba.baidu.com/f?kw='+kw+'&ie=utf-8&pn='
    
    for i in range(start_pn,end_pn):       #遍历某个贴吧的每一页
        time.sleep(1)
        url=base_url+str(i*50)
       
        html=getHtmlText(url)
        
        codetext=re.findall(r'/p/\d{10}',html)     #获得每个贴的url的号码
        
        for k in codetext:               #将获取的所有url的号码存入一个列表
            tie_code.append(k)               

        #code=set(tie_code)     #去掉重复的
        #tie_code=list(code)
            
        #print(tie_code)
        #print(len(codetext))
   
    
#根据每个帖的URL中的号码，构成每个帖子完整的URL，访问这个URL，
#并从每个帖的代码中获取评论的图片链接，并把这些链接放到一个列表中
def get_image(tie_code):
    img_list=[]
    for code in tie_code:    #访问每一个帖子
        for pn in range(1):         #访问每个帖子的第一页
            tie_url='https://tieba.baidu.com'+code+'?pn='+str(pn)    #每个帖子的URL
            tie=getHtmlText(tie_url)
            pic_link=re.findall(r'"BDE_Image" .*?jpg',tie)       #帖子主体部分图片的部分
            for k in pic_link:               #找到其中图片的URL，并存入列表
                pic_url=re.findall(r'https.*jpg',k)
                img_list.append(pic_url[0])
                
            #print(img_list)
            #time.sleep(1)
    #print(img_list)
    return img_list
    

#保存图片
def save_image(img_list):
    
    count=0
    for url in img_list:      #遍历每个图片的链接
        count+=1
        root='贴吧图片\\'
        path=root+url.split('/')[-1]#str(count)+'.jpg'
        if not os.path.exists(root):
            os.mkdir(root)
        
        try:
            if not os.path.exists(path):
                r=requests.get(url)
                with open (path,'wb') as f:
                    f.write(r.content)
                    f.close()
                    
        except:
            print("图片获取失败！")
            
                  #输出进度
        print('\r当前进度：{:.2f}%'.format(count/len(img_list)*100),end='')

    print("全部图片爬取完毕！")
            
def main():
    print("="*70)
    print("百度图片爬取".center(70,'-'))
    print("="*70)
    print('仅限爬取每个帖子的第一页！爬取速度有点慢，请耐心等待.......\n')
    kw=input("请输入你想要访问的贴吧名：")
    start_pn=eval(input("请输入初始页（从0开始）："))
    end_pn=eval(input("请输入最后页（不包括最后一页）："))
    print("\n开始爬取..............\n")
    
    tie_code=[]
    getTie_code(kw,tie_code,start_pn,end_pn)
    img_list=get_image(tie_code)
    #print(img_list)
    save_image(img_list)

main()
