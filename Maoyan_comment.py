# -*- coding: utf-8 -*-
from __future__ import division
import csv
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
from selenium import webdriver
import time
from selenium import webdriver
from lxml import etree
import requests
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
driver.maximize_window()


# 从csv文件中获取电影名字进行搜索
def get_movie_from_data():
    for root, dirs, files in os.walk('/home/lasia/桌面/中国票房网'):
    # # print root #/home/lasia/桌面/中国票房网
    #     # print dirs #当前路径下所有子目录
    #     # print files  # 'movie_2007.csv', 'crawled_year.txt', 'movie_2015.csv',
        for file in files:
            if 'csv' in file:
                path= root+'/'+file
                csv_reader = csv.DictReader(open(path))
                for line in csv_reader:
                    jude = False
                    movie_name = line['movie_name']
                    movie_year = line['movie_year']

                    # 断点重续，开始时需要先建一个空文件
                    with open('./had_checked.txt','r')as f:
                        for line in f.readlines():
                            if line.replace('\n','') == movie_name:
                                jude = True
                                continue
                    if jude:
                        continue
                    if movie_name == 'movie_name':
                        continue
                    print movie_name
                    # 先写列名

                    get_comment_page_url(movie_name,movie_year)


# 从搜索页面中得到电影的ｉｄ
def get_comment_page_url(movie_name,movie_year):



    url = 'http://maoyan.com/query?kw='+ urllib.quote(movie_name)+'&type=0'
    # print url
    driver.get(url)

    movie_url = driver.find_elements_by_xpath('//div[@class="search-result-box"]/dl/dd/div[@class="channel-detail movie-item-title"]/a')
    # print movie_url[0]
    try:
        movie_id = movie_url[0].get_attribute("href").replace('https://maoyan.com/films/','')
    # print movie_id
    except:
        with open('.gice_up.txt','a+') as f:
            f.write(movie_name+','+movie_year+'\n')
        return
    movie_comment_url = 'http://m.maoyan.com/movie/'+movie_id+'/comments'

    print movie_comment_url

    driver.get(movie_comment_url)
    save_data_to_csv(movie_name, movie_year, [], True)
    get_comment(movie_name,movie_id,movie_year)
    # print movie_id
    # return movie_id


# 用电影ｉｄ进入到电影评论的手机版
def get_comment(movie_name,movie_id,movie_year):

    print movie_name,movie_id

   # '''下滑５０次，得到更多的评论页面'''
    for i in range(50):
        time.sleep(2)
        try:
            driver.find_element('//div[@id="app"]/div[@class="layout"]/footer//span/')

        except:
            driver.execute_script("window.scrollTo(100000,document.body.scrollHeight);")
    print "50页信息已得到"



    '''获取评论信息'''
    users_info = driver.find_elements_by_xpath('//div[@class="comment-right"]')
    # print users_info
    jude = True
    for user_info in users_info:
        information = {}

        try:
            information['movie_id'] = movie_id
            information['user_name'] = user_info.find_element_by_xpath('header/div/em').text
            print information['user_name']


            user_url = user_info.find_element_by_xpath('section/a').get_attribute("href")
            user_id = user_url.split('replies/')[-1].replace('?_v_=yes','')
            information['user_id'] = user_id



            information['comment'] = user_info.find_element_by_xpath('section/a/p').text
            information['time'] = user_info.find_element_by_xpath('footer/time').text
            information['good'] = user_info.find_element_by_xpath('footer/div/a[@class="link comment-like"]/span').text
            information['source'] = get_source(user_info)

            print information

            save_data_to_csv(movie_name,movie_year, information,False)
            # return information
        except:

            print 2222222222
            if jude:
                with open('./had_wrone.txt', 'a+')as f:
                    f.write(movie_name + '\n')
                jude = False


    with open('./had_checked.txt','a+')as f:
        f.write(movie_name+'\n')

# 得到用户评分
def get_source(response):
    source = 0
    pictures = response.find_elements_by_xpath('header/div[@class="comment-score"]')[0].text
    source = pictures.split('了')[-1].replace('分','')
    source = float(source)
    return source


# 存储数据到csv文件，若type为True,则写入列名，否则按列名顺序存入数据
def save_data_to_csv(movie_name,movie_year,information,type):
    path = '/home/lasia/桌面/Maoyan_comment/'+movie_year
    if not os.path.exists(path):
        os.makedirs(path)

    with open(path + '/'+movie_name+'.csv','a+') as csvfile:
        headers = ["movie_id", "user_name", "user_id", "comment", "time", "good", "source"]
        if type:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
        else:
            writer = csv.DictWriter(csvfile, headers)
            writer.writerow(information)



get_movie_from_data()