from scrapy.cmdline import execute
import os
import sys

# 用户调试Scrapy使用
# Edit Configurations->Python interpreter->python 3.8
# 设置断点后回到 main.py 进行 debug，会自动跳到设置断点处
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy','crawl','selenium_spider'])