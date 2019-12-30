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
driver = webdriver.PhantomJS(executable_path='./phantomjs')
def get_data():
    for root, dirs, files in os.walk('/home/lasia/桌面/actor_office'):
            # print root #/home/lasia/桌面/中国票房网
            # print dirs #当前路径下所有子目录
            # print files  # 'movie_2007.csv', 'crawled_year.txt', 'movie_2015.csv',
            for file in files:
                # print file
                path = root+'/'+file
                print path
                road = '/home/lasia/桌面/other_movie_info/' + file
                try:
                    with open(path,'r+') as f:
                        for line in f.readlines():
                            line = json.loads(line.replace('\n',''))
                            # print line
                            jude = 0
                            url = line['movie_url']
                            if os.path.exists(road):
                                with open(road,'r+') as x:
                                    for i in x.readlines():
                                        i = json.loads(i.replace('\n', ''))
                                        if i['id'] in url:
                                            jude = 1
                                            print '111111111'
                                            break
                                        else :
                                            jude = 0
                            if jude ==1:
                                continue

                            try:

                                info = get_movie_info(url,line['movie_name'])
                                with open(road,'a+') as ff:
                                    json.dump(info,ff)
                                    ff.write('\n')
                            except:
                                with open('./problem.txt','a+')as ff:
                                    ff.write(file+','+line['movie_name']+url+'\n')
                                print url
                                print '22222222222222'




                except:
                    print '==========================='


def get_movie_info(url,movie_name):

    driver.get(url)
    time.sleep(2)
    info = {}

    r = requests.get(url)
    page_source = r.content.decode("utf-8")
    html = etree.HTML(page_source)

    for i in html.xpath('//div[@class="ziliaoku"]//div[@class="cont"]'):

            info['id'] = url.split('/')[-1]
            info['movie_name'] = movie_name

            # 票房
            total = i.xpath('p/span[@class="m-span"]/text()')
            if total !=[]:
                info['total'] = total[1]
            else:
                info['total'] = 'null'
            # print info['total']
            # 电影类型
            a = i.xpath('p/text()')
            for e in a:
                if '类型' in e:
                   info['type'] = e
            # 片长
            longtime = i.xpath('p[4]/text()')[0].replace('\r\n','')
            longtime = longtime.replace(' ','')
            # print longtime
            longtime = longtime.split('：')[-1]

            if ":" in longtime:
                longtime  = longtime.split(':')[-1]
            if "(" in longtime:
                longtime = longtime.split('(')[0]
            if longtime == '':
                longtime = 'null'
            info['longtime'] = longtime
            # 上映日期，国家及地区
            date = i.xpath('p[5]/text()')[0].replace('\r\n','').replace(' ','').split('：')[-1]
            info['date'] = date
            area = i.xpath('p[7]/text()')[0].split('：')[-1]
            info['area'] = area


            company = i.xpath('p/a/text()')
            if company == []:
                company = 'null'
            else:
                company = company[0]
            # print company

            # 演员
            actor_list = []
            for i in html.xpath("//div[@id='tabcont1']/dl[@class='dltext']/dd[2]/p/a"):

                actor_url = i.xpath("@href")[0]
                name = i.xpath('@title')[0]
                actor_list.append(name+"_"+actor_url)
                # print actor_url,name
                # with open('/home/lasia/桌面/票房网演员id/url.txt','a+') as f:
                #     f.write(actor_url+'`'+name+'\n')

            info['actor_list'] = actor_list
            print info


    # print '===================='
    return info
get_data()




def get_typenum():
    for root, dirs, files in os.walk('/home/lasia/桌面/actor_movietype'):
            # print root #/home/lasia/桌面/中国票房网
            # print dirs #当前路径下所有子目录
            # print files  # 'movie_2007.csv', 'crawled_year.txt', 'movie_2015.csv',
            info =[]
            for file in files:
                # print file
                path = root+'/'+file
                print path
                with open(path,'r') as f:
                    a = []
                    for line in f.readlines():
                        line = line.replace('\n','')
                        types = line.split('*')[-1]
                        # print types
                        types = types.replace('类型：','')
                        print types
                        if '/' in types:
                            types = types.split('/')
                            for i in types:
                                if i not in a:
                                    a.append(i)
                        else:
                            if types not in a:
                                a.append(types)

                    info = {}
                    for i in a:
                        num = 0
                        with open(path, 'r') as f:
                            for line in f.readlines():
                                line = line.replace('\n','')

                                if i in line:
                                    num = num+1
                        info[i]= num
                    print info
                    print '================================'


# get_typenum()

