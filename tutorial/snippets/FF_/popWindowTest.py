import unittest
from rest_framework import response
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException 
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import  ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementNotInteractableException
from time import time, sleep
from datetime import datetime
import HTMLTestRunner
import re
import random
import cx_Oracle
# from superdatagenerator import Super2000Data
from selenium.webdriver.chrome.options import Options


# ChromeDriver 設定參數
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 背景執行
# chrome_options.add_argument("--start-maximized")  # 全螢幕

class AutoFrontTools:
    def __init__(self) -> None:
        self.dr = webdriver.Chrome(
            executable_path=r'C:\\Users\\Peter\\drf_test\\tutorial\\snippets\\FF_\\chromedriver',
            #executable_path='./chromedriver',
            chrome_options=chrome_options
            )
        self.id_ = self.dr.find_element_by_id
        self.xpath = self.dr.find_element_by_xpath
        self.class_ = self.dr.find_element_by_class_name
        self.css = self.dr.find_element_by_css_selector
        self.link = self.dr.find_element_by_link_text

        self.env = 'fh82dev02'
        self.user = 'shycontract00'
        
    def login(self, env: str, user: str) -> None:
        global em_url,www_url,envs
        try:
            if env in ['joy188', 'joy188.195353']:
                envs = 1
                www_url = f'http://www2.{env}.com/'
                em_url = f'http://em.{env}.com/'
                password = 'amberrd'
                

            elif env in ['dev02', 'dev03', 'fh82dev02']:
                envs = 0
                www_url = f'http://www.{env}.com/'
                em_url = f'http://em.{env}.com/'
                password = '123qwe'
        
            self.dr.get(www_url)
            self.dr.find_element_by_id('J-user-name').send_keys(user)
            self.dr.find_element_by_id('J-user-password').send_keys(password)
            self.dr.find_element_by_id('J-form-submit').click()
            sleep(3)

        except NoSuchElementException as e:
            print(e)
        except ElementClickInterceptedException as e:
            print(e)
    
    def checkPopWindow(self):
        now_time = datetime.now().strftime("%Y%m%d%H%M")

        # 登入
        self.login(self.env, self.user)

        # 首頁免轉彈窗
        hover = self.dr.find_element_by_xpath('//*[@id="jointVentureHrader"]/div[2]/div/div[2]/div[5]/div[3]/a')
        ActionChains(self.dr).move_to_element(hover).perform()
        self.dr.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div[5]/div[3]/div/a').click()
        # self.dr.get_screenshot_as_file(f'{now_time}_首頁免轉.png')
        sleep(3)
        self.dr.find_element_by_xpath('/html/body/div[22]/div[1]/i').click()

        self.dr.find_element_by_xpath('//*[@id="shortcut"]/div/div/div/div[2]').click()
        # self.dr.get_screenshot_as_file(f'{now_time}_首頁客服.png')
        sleep(3)
        

if __name__ == '__main__':
    AutoFrontTools().checkPopWindow()
    