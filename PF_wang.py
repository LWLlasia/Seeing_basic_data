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
def get_data():
    url = 'http://www.cbooo.cn/movies'
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'],executable_path='./phantomjs')

    driver.get(url)

    time.sleep(2)
    year = driver.find_element_by_xpath('//div[@class="borbg mar30 pad01"]/div[@class="select01"]/select[@id="selYear"]')
    year.click()
    time.sleep(0.5)

    target_year = driver.find_element_by_xpath('//div[@class="borbg mar30 pad01"]/div[@class="select01"]/select[@id="selYear"]/option[@value="2018"]')
    target_year.click()

    select = driver.find_element_by_xpath('//div[@class="borbg mar30 pad01"]/div[@class="select01"]/input[@value="查询"]')
    time.sleep(0.3)
    select.click()

    time.sleep(5)

    page = driver.find_elements_by_xpath('//div[@class="row pagebar"]/ul/li')

    # print page[-2].text
    data = []
    for a in range(int(page[-2].text)):
        for i in driver.find_elements_by_xpath('//div[@class="borbg mar30 pad01"]/ul/li'):

            info = {}
            movie_name = i.find_elements_by_xpath('a')[0].text
            movie_url = i.find_element_by_xpath('a').get_attribute('href')
            movie_id = movie_url.split('/')[-1]
            # print movie_name,movie_url
            info['movie_id'] = movie_id
            info['movie_name'] = movie_name.replace('《','').replace('》','')
            info['movie_url'] = movie_url
            info['movie_year'] = 2018
            # print info
            data.append(info)

        next_page = driver.find_elements_by_xpath('//div[@class="row pagebar"]/ul/li')[-1]
        next_page.click()
        time.sleep(3)

    return data

def save_data_csv():

    with open('/home/lasia/桌面/movie_2018.csv', 'a+') as csvfile:
        headers = ["movie_id", "movie_name", "movie_url", "movie_year"]

        writer = csv.writer(csvfile)
        writer.writerow(headers)
        data = get_data()
        for i in data:
            writer = csv.DictWriter(csvfile, headers)
            writer.writerow(i)
            print  i


save_data_csv()



