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
import json

driver = webdriver.Chrome()
# driver.maximize_window()
name = 'douban_comment'
heasers = {
        'Host': 'accounts.douban.com',
        'Referer': 'https://accounts.douban.com/passport/login',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
}


def get_movie_from_data():
    cookie = login()

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
                            if line.replace('\n','').split('/')[0] == movie_name:
                                jude = True
                                continue
                    if jude:
                        continue
                    if movie_name == 'movie_name':
                        continue
                    print movie_name
                    # 先写列名


                    get_comment_page_url(movie_name,movie_year,cookie)

def login():
    url = "https://accounts.douban.com/login?source=movie"

    driver.get(url)
    account = driver.find_elements_by_xpath('//li[@class="account-tab-account"]')
    account[0].click()
    print 2222222222
    time.sleep(2)

    phone = driver.find_element_by_xpath('//input[@class="account-form-input"]')
    password = driver.find_element_by_xpath('//*[@class="account-form-input password"]')
    submit = driver.find_element_by_xpath('//div[@class="account-form-field-submit "]')
    phone.send_keys('18924891329')
    password.send_keys('853594529')
    # print cookie
    time.sleep(1)
    submit.click()
    cookies_list = driver.get_cookies()
    cookie_dict = {i["name"]:i["value"] for i in cookies_list}
    return cookie_dict


def get_comment_page_url(movie_name,movie_year,cookie):
    url = 'https://movie.douban.com/j/subject_suggest?q='+ urllib.quote(movie_name)
    # print url

    driver.implicitly_wait(100)
    driver.get(url)
    body = driver.find_element_by_xpath('//body').text
    # print body
    sites = json.loads(body)
    # print type(sites)
    # print sites
    for i in sites:
        i = dict(i)
        if not i.has_key('year'):
            continue
        if movie_year in i['year']:
            url = i['url'].split("?")[0]
            # print url
            url = url+"comments?start=0&limit=20&sort=new_score&status=P&percent_type="
            get_comment(movie_name,url+'h',movie_year,cookie)
            get_comment(movie_name, url + 'm', movie_year,cookie)
            get_comment(movie_name, url + 'l', movie_year,cookie)
            # print movie_id
            # return movie_id
    return

# argparse



def get_comment(movie_name,url,movie_year,cookie):
    driver.implicitly_wait(10)
    # driver.delete_all_cookies()
    # driver.add_cookie(cookie)

    # driver.refresh()
    driver.get(url)
    # print movie_name

    try:
        '''获取评论信息'''
        for i in driver.find_elements_by_xpath('//div[@id="comments"]//div[@class="comment"]'):
            movie_data = {}
            comment_type = url.split('=')[-1]
            movie_data['movie_id'] = url.split('subject/')[-1].split('/')[0]
            movie_data['type'] = comment_type

            movie_data['user_name'] = i.find_element_by_xpath('h3//span[@class="comment-info"]/a').text
            movie_data['user_id'] = i.find_element_by_xpath('h3//span[@class="comment-info"]/a').get_attribute('href').split('people/')[-1].replace('/', '')
            try:
                judge = judge_data(movie_data,movie_name,movie_year )
                if judge:
                    continue
            except:
                pass

            movie_data['comment'] = i.find_element_by_xpath('p/span[@class="short"]').text
            movie_data['time'] = i.find_element_by_xpath('h3//span[@class="comment-time "]').text.replace('\n                    ', '')
            movie_data['good'] = i.find_element_by_xpath('h3/span[@class="comment-vote"]/span').text

            rating = i.find_element_by_xpath('h3/span[@class="comment-info"]/span[2]').get_attribute('class').replace("allstar","").replace(" rating", "")
            # print rating

            movie_data['source'] = rating
            print movie_data
            save_data(movie_data, movie_name, movie_year)
    except:
        pass

    print '=========='
    try:
        next_page = driver.find_element_by_xpath("//*[@class='next']")

        if next_page.get_attribute('href') == None:
            print '到底了'

            with open('./had_checked.txt','a+')as f:
                f.write(movie_name+'/'+url+'\n')
            return
        else:
            print next_page.get_attribute('href')
            url = next_page.get_attribute('href')
            next_page.click()
            driver.implicitly_wait(20)
            print 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
            get_comment(movie_name,url,movie_year,cookie)

    except:
        return

# 存储数据到csv文件，若type为True,则写入列名，否则按列名顺序存入数据
def save_data(data, movie_name, movie_year):
    headers = ["movie_id", "user_name", "user_id", "comment", "type", "time", "good", "source"]
    type = data['type'].split('_')[0]

    path = "/home/lasia/桌面/douban_comment/" + movie_year
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)

        with open("/home/lasia/桌面/douban_comment/" + movie_year + '/' + movie_name  + '.csv', 'a')as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)

    else:
        with open("/home/lasia/桌面/douban_comment/" + movie_year + '/' + movie_name + '.csv','a')as csvfile:
            writer = csv.DictWriter(csvfile, headers)
            writer.writerow(data)


# 帮电影建文件夹和ｃｓｖ文件
def judge_data(data,movie_name,movie_year):
    judge = False
    type = data['type'].split('_')[0]
    root = "/home/lasia/桌面/douban_comment/" + movie_year

    path = root + '/' + movie_name  + ".csv"
    # print path
    csv_reader = csv.DictReader(open(path))
    for row in csv_reader:
        # print row['user_id']
        if data['user_id'] == row['user_id']:
            judge = True
            break

    return judge

get_movie_from_data()