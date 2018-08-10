import requests,bs4,os
#os库专门对文档进行操作
for pn in range (1):#设置爬取三页图片

    url = 'https://tieba.baidu.com/f?ie=utf-8&kw=%E5%8A%A8%E6%BC%AB%E5%9B%BE%E7%89%87&pn=' + str(pn*50)
    response=requests.get(url)

    dirName='imagefile'#文件夹
    os.makedirs(dirName ,exist_ok= True)
    soup=bs4.BeautifulSoup (response.text,'html.parser')
    imageTab=soup.select(".thumbnail  img ")

    if not imageTab  :
       print("没有找到这个图片的标签")
    else:
       for imageUrl in imageTab  :
             imagePath=imageUrl.get('bpic')
             print('图片的路径：',imagePath )

             split=imagePath.split('/')
             imageName=os.path.basename(split[len(split)-1 ])
             print('图片名称：',imageName )

             filePath=os.path.join(dirName ,imageName)

             if not os.path.exists(filePath) :  #检查文件路径是否存在
                 rePath= requests.get( imagePath)
                 print("请求：",rePath)
                 rePath.raise_for_status()
                 imageFile=open(filePath,'wb')
                 for images in rePath .iter_content(1000):
                    #把每次遍历文件全部写进文件中
                    imageFile.write(images )
                 imageFile.close()






