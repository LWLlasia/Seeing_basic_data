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


# for root, dirs, files in os.walk('/home/lasia/桌面/中国票房网'):
#     # print root #/home/lasia/桌面/中国票房网
#     # print dirs #当前路径下所有子目录
#     # print files  # 'movie_2007.csv', 'crawled_year.txt', 'movie_2015.csv',
#     for file in files:
#         if 'csv' in file:
#             path= root+'/'+file
#             with open(path,'r') as f:
#                 csv_reader = csv.DictReader(open(path))
#                 for row in csv_reader:
#                     movie_url = row['movie_url']
#                     print movie_url,row['movie_name']


url = ''


def get_actor(url,movie_name):
    """
    获取演員
    :param url:电影所在頁面地址
    :return:
    """






    info = {}
    actor = []
    time.sleep(1)

    r = requests.get(url)
    page_source = r.content.decode("utf-8")
    html = etree.HTML(page_source)
    try:
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

        # 导演
        director_list = []
        for i in html.xpath("//div[@id='tabcont1']/dl[@class='dltext']/dd[1]/p/a"):
            director = i.xpath('@title')[0]
            director_url = i.xpath("@href")[0]
            # print director,director_url
            director_list.append(director+"_"+director_url)

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
        # 制作公司
        makecompany_list = []
        for i in html.xpath("//div[@id='tabcont1']/dl[@class='dltext']/dd[3]/p/a"):
            makecompany_url = i.xpath("@href")[0]
            makecompany = i.xpath('@title')[0]
            makecompany_list.append(makecompany+"_"+makecompany_url)
        info['make_companylist'] = makecompany_list

        print info

        with open('./had_check.text','a+')as f:
            f.write(url + '\n')
    except:
        print '222222222222222222222222'
        with open('./had_wrong.text','a+')as f:
            f.write(url + '\n')
    # print '===================='
    return info



def get_starturl():
    for root, dirs, files in os.walk('/home/lasia/桌面/中国票房网'):
        # print root #/home/lasia/桌面/中国票房网
        # print dirs #当前路径下所有子目录
        # print files  # 'movie_2007.csv', 'crawled_year.txt', 'movie_2015.csv',
        for file in files:
            if '.csv' in file:
                path= root+'/'+file
                print path

                csv_reader = csv.DictReader(open(path))
                for datas in csv_reader:
                    print datas['movie_url'],datas['movie_name']
                    # info = get_actor(datas['movie_url'],datas['movie_name'])
                    road = '/home/lasia/桌面/newMovie_info/'+datas['movie_year']
                    if not os.path.exists(road):
                        os.makedirs(road)
                    road = road + '/' + datas['movie_url'].split('/')[-1] + '.json'
                    if os.path.exists(road):
                        print 'true'
                        continue
                    info = get_actor(datas['movie_url'], datas['movie_name'])
                    with open(road,'a+') as f:
                        json.dump(info,f)

# get_starturl()