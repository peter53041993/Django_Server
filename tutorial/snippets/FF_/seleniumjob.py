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
from selenium.webdriver.chrome.options import Options
from faker import Factory, Faker

# ChromeDriver 設定參數
chrome_options = Options()
chrome_options.add_argument("--headless")  # 背景執行
chrome_options.add_argument("--start-maximized")  # 全螢幕

class AutoFrontTools:
    def __init__(self) -> None:
        self.dr = webdriver.Chrome(
            executable_path=r'C:\\Users\\Peter\\Documents\\drf_test\\tutorial\\snippets\\FF_\\chromedriver',
            #executable_path='./chromedriver',
            chrome_options=chrome_options
            )
        self.id_ = self.dr.find_element_by_id
        self.xpath = self.dr.find_element_by_xpath
        self.class_ = self.dr.find_element_by_class_name
        self.css = self.dr.find_element_by_css_selector
        self.link = self.dr.find_element_by_link_text

        self.safe_dict = ['amberrd', '123qwe']
        
    def login(self, env: str, user: str) -> None:
        global em_url,www_url,envs
        try:
            if env in ['joy188', 'joy188.teny2020']:
                envs = 1
                www_url = f'https://www2.{env}.com/'
                em_url = f'https://em.{env}.com/'
                password = 'amberrd'
                

            elif env in ['dev02', 'dev03', 'fh82dev02']:
                envs = 0
                www_url = f'http://www.{env}.com/'
                em_url = f'http://em.{env}.com/'
                password = '123qwe'
            else:
                www_url = ''
                password = ''
        
            self.dr.get(www_url)
            self.dr.find_element_by_id('J-user-name').send_keys(user)
            self.dr.find_element_by_id('J-user-password').send_keys(password)
            self.dr.find_element_by_id('J-form-submit').click()
            sleep(3)

        except NoSuchElementException as e:
            print(e)
        except ElementClickInterceptedException as e:
            print(e)
    
    def registerUser(self, user: str, nums: int, subtitle: str, status: str) -> tuple:
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
            else:
                register_url = ''

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
    
    def safeCenterSetting(self):
        safePassword = self.safe_dict[envs]
        self.dr.get(www_url+'/safepersonal/safecodeset')
        # print(self.dr.title)

        self.id_('J-safePassword').send_keys(safePassword)
        self.id_('J-safePassword2').send_keys(safePassword)
        # print(u'設置安全密碼/確認安全密碼: %s'%safePassword)
        self.id_('J-button-submit').click()

        self.dr.get(www_url+'/safepersonal/safequestset')
        # print(self.dr.title)
        for i in range(1,4,1):#J-answrer 1,2,3  
            self.id_('J-answer%s'%i).send_keys(safePassword)#問題答案
        for i in range(1,6,2):# i產生  1,3,5 li[i], 問題選擇
            self.xpath('//*[@id="J-safe-question-select"]/li[%s]/select/option[2]'%i).click()
        self.id_('J-button-submit').click()#設置按鈕
        self.id_('J-safequestion-submit').click()#確認
    
    def bindBankCard(self):
        safePassword = self.safe_dict[envs]

        self.dr.get(www_url+'/bindcard/bindcardsecurityinfo/')
        # print(self.dr.title)
        fake = Factory.create()
        card = fake.credit_card_number(card_type='visa16')

        self.xpath('//*[@id="bankid"]/option[2]').click()#開戶銀行選擇
        self.xpath('//*[@id="province"]/option[2]').click()#所在城市  :北京
        self.id_('branchAddr').send_keys(u'內湖分行')#之行名稱
        self.id_('bankAccount').send_keys('kerr')#開戶人
        self.id_('bankNumber').send_keys(str(card))#銀行卡浩
        # print(u'綁定銀行卡號: %s'%card)
        self.id_('bankNumber2').send_keys(str(card))#確認銀行卡浩
        self.id_('securityPassword').send_keys(safePassword)#安全密碼
        self.id_('J-Submit').click()#提交
        sleep(3)
    
    def bindVirtualAdress(self):
        safePassword = self.safe_dict[envs]

        usdt_dict  = {
            'TRC-20':['T1166616165a1S1DCD2FD7afefff651651','2'],
            'ERC-20':['0xaaaaaaaaaaaaaaaaaaa11aa11111111111111111','3']
        }

        for key in usdt_dict.keys():
            self.dr.get(www_url+'/bindcard/bindcarddigitalwallet?bindcardType=2')
            self.id_('protocol').click()#幣種選擇
            self.xpath('//*[@id="protocol"]/option[{value}]'.format(value=usdt_dict[key][1])).click()# 選擇 trc-20
            card = usdt_dict[key][0]
            self.id_('walletAddr').send_keys(card)#
            # print(u'usdt 幣種協議: %s , 提現錢包地址: %s'%(key,card))
            self.id_('securityPassword').send_keys(safePassword)
            # print(u'安全密碼:%s'%safePassword)
            self.id_('J-Submit').click()#提交
            sleep(2)

    def bindAlipay(self):
        safePassword = self.safe_dict[envs]

        bnak_account = 'peterq'
        user_random = bnak_account+'%s'%random.randint(1,1000000)
        bnak_number = user_random+'@123.com'

        self.dr.get(www_url+'/bindcard/bindcardalipay?bindcardType=1')
        self.id_('bankAccount').send_keys(bnak_account)
        self.id_('bankNumber').send_keys(bnak_number)
        self.id_('bankNumber2').send_keys(bnak_number)
        self.id_('securityPassword').send_keys(safePassword)
        self.id_('J-Submit').click()#提交
        # print(u'支付寶用戶名: %s, 綁訂帳號: %s' %(bnak_account, bnak_number))
        sleep(2)


if __name__ == '__main__':
    pass





            
        


    

