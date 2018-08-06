import urllib.request
import urllib.parse
import re
import time


def getSSYPImage():
    x = 0
    page = 1
    s = True
    while s == True:
        url = 'https://movie.douban.com/subject/26588308/comments?start='+str(x)+'&limit=20&sort=new_score&status=P'
        res = urllib.request.urlopen(url)
        html = res.read().decode('utf-8')
        # print(html)
        r = r'<a href=".*?" class="">(.*?)</a>'
        user = re.findall(r,html)
        # print(user)
        r1 = r'<span class="short">(.*?)</span>'
        short = re.findall(r1,html)
        # print(short)
        n = 0
        print('正在保存：第%d页' % page)
        for i in short:
            time.sleep(1)
            f = open('C:\python\死侍2影评\\'+'第'+str(page)+'页短评'+'.txt','a',encoding='utf-8')
            f.write(user[n]+'：'+'\n'+i+'\n'+'-'*100+'\n')
            f.close()
            n += 1

        x += 20
        page += 1
        if x == 200:
            s = False





if __name__ == '__main__':
    getSSYPImage()