# -*- coding: utf-8 -*-
from urllib.parse import quote
import scrapy
from scrapy.http import Request
from urllib import parse
import re
from ArticleSpider.items import DoubanMovieItem, DoubanMovieItemLoader
from ArticleSpider.utils.common import get_md5


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/']
    list = ["热门", "最新", "经典", "可播放", "豆瓣高分", "冷门佳片", "华语",
            "欧美", "韩国", "日本", "动作", "喜剧", "爱情", "科幻", "悬疑",
            "恐怖", "治愈"]

    def parse(self, response):
        json = response.text.replace("\\", "")
        urls = re.findall('https://movie.douban.com/subject/\d+/', json)
        if urls:
            for url in urls:
                yield Request(url=parse.urljoin(response.url, url), callback=self.parse_detail)
        for tag in self.list:
            next_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag={0}&sort=recommend&page_limit=5000&page_start=0'.format(
                quote(tag))
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        item_loader = DoubanMovieItemLoader(item=DoubanMovieItem(), response=response)
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("name", "#content > h1 > span:nth-child(1)::text")
        item_loader.add_css("release_date", '#info > span[property="v:initialReleaseDate"]::text')
        item_loader.add_css("type", '#info > span[property="v:genre"]::text')
        item_loader.add_css("runtime", '#info > span[property="v:runtime"]::text')
        item_loader.add_xpath("synopsis", "//span[@property='v:summary']/text()")
        movie_item = item_loader.load_item()
        yield movie_item

    def start_requests(self):
        return [scrapy.Request('https://accounts.douban.com/login', callback=self.login)]

    def login(self, response):
        response_text = response.text
        match_obj = re.match('.*name="captcha-id" value="(.*?)"', response_text, re.DOTALL)
        captcha_url_obj = re.match('.*id="captcha_image" src="(.*?)"', response_text, re.DOTALL)
        xsrf = ''
        captcha_url = ''
        if match_obj and captcha_url_obj:
            xsrf = (match_obj.group(1))
            captcha_url = (captcha_url_obj.group(1))
        post_data = {
            'source': 'None',
            'redir': 'https://movie.douban.com /',
            'form_email': '*******',
            'form_password': '******',
            'captcha-solution': '',
            'captcha-id': xsrf,
            'remember': 'on',
            'login': '登录'
        }
        yield scrapy.Request(captcha_url, meta={"post_data": post_data}, callback=self.login_after_captcha,
                             dont_filter=True)

    def login_after_captcha(self, response):
        with open("captcha.jpg", "wb") as f:
            f.write(response.body)
            f.close()

        from PIL import Image
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            pass

        captcha = input("输入验证码\n>")

        post_data = response.meta.get("post_data", {})
        post_url = "https://accounts.douban.com/login"
        post_data["captcha-solution"] = captcha
        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            callback=self.check,
            dont_filter=True
        )]

    def check(self, response):
        # 验证服务器的返回数据判断是否成功
        if response.url == 'https://www.douban.com/':
            yield scrapy.Request(response.url, dont_filter=True)
        else:print("登陆失败")
