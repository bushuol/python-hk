# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime
import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Identity, Join


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def data_convert(value):
    try:
        value = datetime.datetime.strptime(value, "%Y/%m/%d")
    except Exception as e:
        value = datetime.datetime.now().date()
    return value


def getNumbers(nums):
    match_re = re.match(".*?(\d+).*", nums)
    if match_re:
        nums = match_re.group(1)
    else:
        nums = 0
    return nums


def remove_splash(value):
    return value.replace("/", "")


def return_value(value):
    return value


def trim(str):
    str = str.strip().replace('\r', '').replace('\n', '')
    return str


class ArticleItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class JobbleArticleItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(data_convert),
    )
    url_object_id = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(getNumbers)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(getNumbers)
    )

    def get_insert_sql(self):
        insert_sql = """insert into jobbole_article(title, url, create_date,praise_nums,fav_nums)
            VALUES (%s, %s,%s,%s,%s)"""

        params = (
            self["title"], self["url"], self["create_date"], self["praise_nums"], self["fav_nums"]
        )
        return insert_sql, params


class LagouJobItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class LagouJobItem(scrapy.Item):
    # 拉勾网职位信息
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )

    def get_insert_sql(self):
        insert_sql = """
            insert into lagou_job(title, url, url_object_id, salary, job_city) 
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            self["title"], self["url"], self["url_object_id"], self["salary"], self["job_city"]
        )

        return insert_sql, params


class DoubanMovieItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class DoubanMovieItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    release_date = scrapy.Field(
        output_processor=Join("/"),
    )
    type = scrapy.Field(
        output_processor=Join("/"),
    )
    runtime = scrapy.Field()
    synopsis = scrapy.Field(
        input_processor=MapCompose(trim),
    )

    def get_insert_sql(self):
        insert_sql = """
            insert ignore into movies(url_object_id,name, url, release_date, type, runtime,synopsis) 
            VALUES (%s, %s, %s, %s, %s,%s,%s) 
        """
        params = (
            self["url_object_id"],self["name"],self["url"], self["release_date"],self["type"],self["runtime"], self["synopsis"]
        )

        return insert_sql, params
