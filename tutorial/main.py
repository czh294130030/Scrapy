from scrapy.cmdline import execute
import os
import sys

# 用户调试Scrapy使用
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy','crawl','ajax_spider'])