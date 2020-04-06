from time import sleep

import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_driver = r"F:\install\chrome\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver)


# scrapy crawl selenium_spider
# scrapy crawl selenium_spider -o selenium_spider.json


class selenium_spider(scrapy.Spider):
    name = "selenium_spider"
    # 登录页面
    login_url = 'http://mdmtest.zoina.cn:7865/PlatForm/AdminMain/Login'
    # 个人待办页面
    profile_url = 'http://mdmtest.zoina.cn:7866/PlanSystemPortal/PlanSystem/HomePage/PersonalDefault.aspx'

    # 模拟登录
    def start_requests(self):
        # 加载个人待办，由于没有登录跳转到登录页面
        yield scrapy.Request(self.profile_url, callback=self.parse_login)

    def parse_login(self, response):
        if response.url.find(self.login_url) > -1:
            print('到登录页面成功')
            driver.get(response.url)
            driver.find_element_by_id('txbUserID').send_keys('zhangjunwei2')
            driver.find_element_by_id('txbPwd').send_keys('12345678')
            driver.find_element_by_id('btnlogin').click()
            # 等到id为jbsx的元素加载完毕(页面跳转完成),最多等10秒
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'jbsx')))
            # 判断风险预警节点Ajax请求加载完成
            WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.ID, 'progressBar1')))
            # 获取界面元素内容
            trs = driver.find_element_by_id('table1').find_elements_by_tag_name('tr')
            for tr in trs:
                yield {
                    'project_report_name': tr.find_elements_by_tag_name('td')[0].text,
                    'task_name': tr.find_elements_by_tag_name('td')[3].text
                }
            print('获取风险预警节点完成')
        else:
            print('到登录页面失败')

    def parse_None(self, response):
        pass
