# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import os
import json
import csv
import time
from selenium import webdriver
from lxml import etree
import requests
from selenium.webdriver.common.action_chains import ActionChains
# driver = webdriver.PhantomJS(executable_path='./phantomjs')
driver = webdriver.Chrome()

'''找到演员对应的url'''
# with open ('/home/lasia/桌面/PF_actor_url.json') as f:
#     for line in f.readlines():
#         line = json.loads(line)
#         for info in line:
#             jude = 0
#             actor_name = info.split(' ')[0]
#             with open('./had_checked.txt','a+') as h:
#                 for l in h.readlines():
#                     if actor_name in l:
#                         jude =1
#                         break
#             if jude ==1:
#                 continue
#             url = 'http://search.mtime.com/search/?q='+ urllib.quote(actor_name.encode('utf-8'))
#             print actor_name,url
#             print '================='
#             driver.get(url)
#             time.sleep(1)
#             a = {}
#             for i in  driver.find_elements_by_xpath('//div[@id="downRegion"]/div[@class="main"]/ul/li'):
#                 url = i.find_element_by_xpath('h3/a').get_attribute("href")
#                 name = i.find_element_by_xpath('h3/a').text
#                 print name,url
#
#                 if actor_name in name:
#                     a[actor_name] = url
#                     with open('/home/lasia/桌面/寒假爬的数据/actor_url_time.json','a+')as ff:
#                         json.dump(a,ff)
#                         ff.write('\n')
#                     with open('./had_checked.txt','a+') as fi:
#                         fi.write(name+'\n')
#                     break


with open('/home/lasia/桌面/寒假爬的数据/actor_url_time.json','r+') as f:
    for line in f.readlines():
        line = json.loads(line.replace('\n',''))
        print line
        # print type(line)
        for i in line:
            name = i
            url = line[i]+'awards.html'
        driver.get(url)
        time.sleep(1)
        data = {}
        data['actor_id'] = url.split('/')[-2]
        data['actor_name'] = name
        call_present = {}
        get_present = {}
        for i in driver.find_elements_by_xpath('//dl[@id="awardSlidesItems"]/dd'):
            i.click()
            info = str(driver.find_element_by_xpath('//div[@id="awardInfo"]/dl').text)
            if '获奖' in info:
                






