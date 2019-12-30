# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import os
import json
import csv
import random
import time
from selenium import webdriver
from lxml import etree
import requests
from selenium.webdriver.common.action_chains import ActionChains
driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'],executable_path='./phantomjs')



# 将得到的演员列表写入json文件中
# li = {}
# b=0
# a = ['2016', '2010', '2015', '2014', '2009', '2013', '2018', '2012', '2017', '2011']
#
# for i in a:
#
#     for root, dirs, files in os.walk('/home/lasia/桌面/newMovie_info/' + i):
#         # print root #/home/lasia/桌面/中国票房网
#         # print dirs #当前路径下所有子目录
#         # print files  # 'movie_2007.csv', 'crawled_year.txt', 'movie_2015.csv',
#         for file in files:
#             path = root + '/' + file
#             # print path
#             with open(path, 'r')as f:
#                 for line in f.readlines():
#                     line = json.loads(line)
#                     # print line['movie_name'], line['actor_list']
#                     if line['actor_list'] == []:
#                         print line['movie_name']
#                         print 222222222222222222222
#                         break
#
#                     for x in line['actor_list']:
#
#                         b = b+1
#                         url = x.split('_')[-1]
#                         name = x.split('_')[0]
#                         print name,url
#                         li[name] = url
#             print '========================='
#
# print b
# print len(li)
# with open('/home/lasia/桌面/PF_actor_url.json','a+') as f:
#     json.dump(li,f)

def get_data():
    with open('/home/lasia/桌面/PF_actor_url.json', 'r') as f:
        for line in f.readlines():
            line = json.loads(line)
            for x in line:
                id = line[x].split('/')[-1]
                name = x.split(' ')[0].replace('·','')
                url = line[x]

        # with open('./wrong.txt','r') as f:
        #     for line in f.readlines():
        #         line = line.replace('\n','')
        #         name = line.split(',')[-1]
        #         url = line.split(',')[0]

                print name,url

                driver.get(url)
                path ='/home/lasia/桌面/actor_office/'+name+'.json'
                jude = os.path.exists(path)
                print jude
                if jude:
                    continue
                try:
                    time.sleep(2)
                    content = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/ul/li[2]')

                    content.click()

                    time.sleep(2)
                    # print "=========="
                    # data=[]
                    c = driver.find_elements_by_xpath('//div[@id="tabcont"]/ul/li/div/h5/a')
                    # print c
                    # for i in c:
                    #     print i.text
                    next_page = driver.find_elements_by_xpath('//div[@id="tabcont"]/div[@class="row pagebar"]/ul/li')
                    # print next_page[-1]
                    # for i in next_page:
                    #     print i.text
                    click_num =  int(next_page[-2].text)

                    for r in range(click_num):
                        # print '=========================='
                        # data = []
                        for i in driver.find_elements_by_xpath('//div[@id="tabcont"]/ul[@id="ulperm"]/li'):

                            info={}
                            info['year'] = int(i.find_elements_by_xpath('div[1]')[0].text.replace('年',''))

                            a = i.find_elements_by_xpath('div[2]/h5/a')
                            info['movie_name'] = a[0].text.split('》')[0].replace('《','')
                            info['movie_url'] = a[0].get_attribute('href')
                            info['office'] = a[0].text.split('）')[-1]
                            if '￥' in info['office']:
                                info['office'] = info['office'].split('￥')[-1]
                            else:
                                info['office'] = 'null'
                                if '-万' in info['office']:
                                    info['office'] = 'null'
                            print info
                            # data.append(info)
                            with open('/home/lasia/桌面/actor_office/' + name + '.json', 'a+') as yy:
                                json.dump(info, yy)
                                yy.write('\n')
                        next_page = driver.find_elements_by_xpath('//div[@id="tabcont"]/div[@class="row pagebar"]/ul/li')
                        next_page[-1].click()
                        time.sleep(2)
                        # print '====================='
                        # with open('/home/lasia/桌面/actor_office/'+name+'.json','w+') as yy:
                        #     json.dump(data,yy)
                            # jude = os.path.exists(path)
                            # print jude
                    print '====================='

                except :
                    with open('./wrong.txt','a+') as ff:
                        ff.write(url+','+name+'\n')

                    print 2222222222222222

get_data()