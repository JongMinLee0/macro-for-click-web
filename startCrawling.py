# -*- coding: utf-8 -*-
import platform
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.chrome.service import Service

'''
ot16908
임태균94
'''


def login(driver, id, pwd):
    # move login page
    login_ele = driver.find_element_by_xpath(
        "//*[@id='header']/div[1]/div/div[1]/div[2]/ul/li[2]/a")
    print(login_ele)
    login_ele.click()

    # input id, password
    id_ele = driver.find_element_by_xpath(
        "//*[@id='sub']/div/div[2]/div/div[2]/form/ul/li[1]/input")
    id_ele.send_keys(id)
    pwd_ele = driver.find_element_by_xpath(
        "//*[@id='sub']/div/div[2]/div/div[2]/form/ul/li[2]/input")
    pwd_ele.send_keys(pwd)

    # click login
    login_btn = driver.find_element_by_xpath(
        "//*[@id='sub']/div/div[2]/div/div[2]/form/input")
    login_btn.click()

    result = driver.switch_to.alert
    print(result.text())
    try:
        result = driver.switch_to.alert
        print(result.text())
    except:
        print("로그인 성공")


def startCwal(id, pwd):
    check_os = platform.system()
    # Crawling Target URL
    URL = 'http://www.대출스타.net/'

    if check_os == "Darwin":
        # for macbook pro
        service = Service(r"/usr/local/bin/chromedriver")
    else:
        # for window
        service = Service("./driver/chromedriver")

    driver = webdriver.Chrome(service=service)
    driver.get(url=URL)
    driver.implicitly_wait(10)
    # login
    login(driver, id, pwd)

    # block auto close for test
    while(True):
        pass


if __name__ == '__main__':
    startCwal('ot16908', 'dlaxorbs94')
