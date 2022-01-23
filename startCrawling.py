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


if __name__ == '__main__':
    startCwal('123', '123')
