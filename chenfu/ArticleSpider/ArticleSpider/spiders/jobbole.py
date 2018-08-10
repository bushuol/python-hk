# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from ArticleSpider.utils.common import get_md5
from ArticleSpider.items import JobbleArticleItem, ArticleItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    # def __init__(self):
    #     self.browser = webdriver.Chrome(executable_path="C:/Users/chenfu/Documents/chromedriver.exe")
    #     super(JobboleSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self, spider):
    #     #当爬虫退出的时候关闭chrome
    #     print ("spider closed")
    #     self.browser.quit()

    def parse(self, response):
        urls = response.css(".archive-title::attr(href)").extract()
        for post_url in urls:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)
        next_url = response.css('#archive > div.navigation.margin-20 > a.next.page-numbers::attr(href)').extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
        pass

    def parse_detail(self, response):
        item_loader = ArticleItemLoader(item=JobbleArticleItem(), response=response)
        item_loader.add_xpath("title", '//div[@class="entry-header"]/h1/text()')
        item_loader.add_value("url", response.url)
        item_loader.add_xpath("create_date", "//p[@class='entry-meta-hide-on-mobile']/text()")
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_xpath("praise_nums", "//span[contains(@class, 'vote-post-up')]/h10/text()")
        item_loader.add_xpath("fav_nums", "//span[contains(@class, 'bookmark-btn')]/text()")
        article_item = item_loader.load_item()

        yield article_item
