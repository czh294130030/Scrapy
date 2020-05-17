import json

import scrapy
from scrapy import Request

# cmd到scrapy.cfg所在的目录，如（E:\Study\Python\Scrapy\tutorial）
# scrapy crawl ajax_spider
# scrapy crawl ajax_spider -o ajax_spider.json


class ajax_spider(scrapy.Spider):
    name = "ajax_spider"
    # 登录接口
    token_url = 'http://myerp.zoina.cn:5679/api/Authorization/GetApiToken?authcode=dfffbb2c16f3c8f537cd88a342436f48'
    # 获取房间接口
    base_url = 'http://myerp.zoina.cn:5679//api/DataV/GetApiData/RoomToMDMFromMY'
    # 初始值
    begintimestamp = 171298248
    # 获取页数数据
    PageNum = 10;
    PageCounter = 1;

    def start_requests(self):
        yield Request(self.token_url, callback=self.parse_token)

    def parse_token(self, response):
        token_json = json.loads(response.text)
        if (token_json["Success"]):
            print('获取Token成功')
            token = token_json["Data"]
            data_url = self.base_url + '?beginTimeStamp=' + str(
                self.begintimestamp) + '&Startindex=0&Endindex=10&token=' + token
            yield Request(data_url, callback=self.parse_item)
        else:
            print('获取Toke失败')

    def parse_item(self, response):
        data_json = json.loads(response.text)
        for item in data_json:
            yield {
                'RoomGUID': str(item['RoomGUID']),
                'RoomInfo': item["RoomInfo"],
                'Status': item["Status"],
                'CgTimeStamp': item["CgTimeStamp"]
            }
            self.begintimestamp = item["CgTimeStamp"]
        if (self.PageCounter <= self.PageNum):
            self.PageCounter = self.PageCounter + 1
            yield Request(self.token_url, callback=self.parse_token, dont_filter=True)
