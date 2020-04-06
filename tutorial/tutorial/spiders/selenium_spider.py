from time import sleep

import scrapy

# scrapy crawl login_spider
# scrapy crawl login_spider -o login_spider.json


class login_spider(scrapy.Spider):
    name = "login_spider"
    # 个人待办页面
    profile_url = 'http://mdmtest.zoina.cn:7866/PlanSystemPortal/PlanSystem/HomePage/PersonalDefault.aspx'
    # 货值列表页面
    project_url = 'http://mdmtest.zoina.cn:7865/HY_MDS/ProjectManage/ProjectList'
    # 登录页面
    login_url = 'http://mdmtest.zoina.cn:7865/PlatForm/AdminMain/LoginM'

    # 模拟登录
    def start_requests(self):
        # 如果直接跳转到个人待办，由于系统有登录判断，会跳转到登录页面
        # yield scrapy.Request(self.profile_url, callback=self.parse_profile)
        return [scrapy.FormRequest(self.login_url,
                                   formdata={'Account': 'zhangjunwei2', 'Password': '12345678', 'Remember': 'false'},
                                   callback=self.logged_in)]

    # 如果登录成功跳转到个人待办
    def logged_in(self, response):
        print('登录返回数据：' + response.text)
        if '1' in response.text:
            print('登录成功')
            # 跳转个人待办
            yield scrapy.Request(self.profile_url, callback=self.parse_profile)
            # 跳转项目列表
            # yield scrapy.Request(self.project_url, callback=self.parse_project)
        else:
            print('登录失败')

    def parse_project(self, response):
        print(response.url)
        if response.url.find(self.project_url) > -1:
            print('进入项目表成功！')
        else:
            print('进入项目列表失败！')

    def parse_profile(self, response):
        print(response.url)
        if response.url.find(self.profile_url) > -1:
            print('进入个人待办成功！')
            # 等待区域加载完成
            # 解决FileNotFoundError: [WinError 2]系统找不到指定的文件
            # 根据提示找到lib中的subprocess.py文件 查找class Popen模块，再将这个模块中的__init__函数中的shell = False改成shell = True
            progress_style = response.css("#progressBar1::attr(style)").extract_first()
            print(progress_style)
            sleep(60)
            trs = response.css("#table1>tr");
            for tr in trs:
                yield {
                    'text': tr.css("td.eq(0)::text").extract_first(),
                }
        else:
            print('进入个人待办失败！')

    def parse_None(self, response):
        pass
