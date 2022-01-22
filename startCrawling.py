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
    # Crawling Target URL
    URL = 'http://www.대출스타.net/'

    service = Service("./driver/chromedriver")
    driver = webdriver.Chrome(service=service)
    driver.get(url=URL)
