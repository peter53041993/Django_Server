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
from time import sleep
import HTMLTestRunner
import re
import random
import cx_Oracle
from .superdatagenerator import Super2000Data

class AutoFrontTools:
    def __init__(self) -> None:
        self.dr = webdriver.Chrome(executable_path=r'C:\\Users\\Peter\\drf_test\\tutorial\\snippets\\FF_\\chromedriver')
        self.id_ = self.dr.find_element_by_id
        self.xpath = self.dr.find_element_by_xpath
        self.class_ = self.dr.find_element_by_class_name
        self.css = self.dr.find_element_by_css_selector
        self.link = self.dr.find_element_by_link_text
        
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
    
    def registerUser(self, user: str, nums: int, subtitle: str, status: str) -> list:
        register_list = []
        register_list.append(user)

        for i in range(nums):
            new_user = f'{subtitle}{random.randint(10,10000)}'
            register_list.append(new_user)

        response_message = []
        for index, value in enumerate(register_list):
            if index == len(register_list) - 1:
                break
            
            sleep(5)
            
            if status == 'chain':
                register_url = Super2000Data().selectUserUrl(envs, value)
            elif status == 'one':
                register_url = Super2000Data().selectUserUrl(envs, user)

            self.dr.get(www_url+'register?'+register_url[0])

            password = '123qwe' if envs == 0 else 'amberrd'
            
            new_user = register_list[index +1]

            self.id_('J-input-username').send_keys(new_user)
            self.id_('J-input-password').send_keys(password)
            self.id_('J-input-password2').send_keys(password)
            self.id_('J-button-submit').click()
            
            response_message.append(f'{new_user} 成功註冊')
            sleep(1)
        
        return (register_list ,response_message)






            
        


    

