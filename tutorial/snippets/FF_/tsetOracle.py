import json
import requests
import pymysql, redis

class DBconnection:
    def __init__(self) -> None:
        pass

    def ubitDev(self):
        conn = pymysql.connect(
            host='10.13.22.164',
            user='ubit',
            passwd='!Eaopqno5>amf#w,KB0#',
            )
        return conn
    
    def ubitStg(self):
        conn = pymysql.connect(
            host='54.150.197.171',
            user='rd_user',
            password='rd_user  Sxae4Z93BDfcDUDR',
        )
        return conn

    def ubitRedis(self):
        pool = redis.ConnectionPool(host='10.13.22.154')
        conn = redis.Redis(connection_pool=pool)
        return conn


class UbitAdminApiTest:
    def __init__(self) -> None:
        self.headers = {'Content-type': 'application/json'}
        self.session = requests.Session()
        # 登入後台取得session
        self.session.get('http://admin.ubitdev.com/login/test/admin')
    
    def getIdentity(self, userId: int):
        data ={
            'userId': userId
        }
        r = self.session.post(
            'http://admin.ubitdev.com/user/getIdentity', 
            data=json.dumps(data), 
            headers=self.headers
            )
        return r.json() 

class UbitFrontApiTest:
    def __init__(self) -> None:
        self.headers = {'Content-type': 'application/json'}
        self.session = requests.Session()
        self.user_headers = None
    
        # config
        self.domain = {
            0: 'http://admin.ubitdev.com/',
            1: ''
        }

        self.account = {
            0: '',
            1: ''
        }
    
    def sentVerify(self, areaCode: int, phone: int, verifyType: int) -> None:
        '''
        verifyType: 
        2登录 3登录密码 4支付密码 5.Google验证码 6新增银行卡 7设置新手机 8.修改银行卡验证码 9.校验手机验证码
        '''
        data = {
            "areaCode": areaCode,
            "phone": f"{phone}",
            "verifyType": verifyType
            }
        
        self.session.post(
            'http://api.ubitdev.com/user/verifyCode/send',
            data=json.dumps(data),
            headers=self.headers
            )
    
    def sentCaptcha(self) -> str:
        r = self.session.get(
            'http://api.ubitdev.com/user/captcha'
        )
        return r.json()['data']['captchaToken']

    def getCaptchaValue(self) -> tuple:
        '''
        key -> userLgoin: captchaToken
        key_ -> redis key
        '''
        key = self.sentCaptcha()
        conn = DBconnection().ubitRedis()
        key_ = 'CAPTCHA:'+key
        return key, conn.get(key_)
    
    def userLogin(self, areaCode: int, phone: int, loginType: int) -> dict:
        '''
        loginType: 1:密码登录 2:验证码登录
        '''
        
        if loginType == 2:
            self.sentVerify(areaCode, phone, 2)

            data = {
                "areaCode": areaCode,
                "captchaToken": "",
                "graphicalCode": "",
                "loginType": loginType,
                "password": "",
                "phone": f"{phone}",
                "verifyCode": "123456"
                }
            
        elif loginType == 1:
            capcha = self.getCaptchaValue()
            # 1234qwer: 62c8ad0a15d9d1ca38d5dee762a16e01
            data = {
                "areaCode": areaCode,
                "captchaToken": capcha[0],
                "graphicalCode": str(capcha[1], 'utf-8'), # capcha[1].decode("utf-8") 
                "loginType": loginType,
                "password": "62c8ad0a15d9d1ca38d5dee762a16e01",
                "phone": f"{phone}",
                "verifyCode": ""
                }

        # 預留給更多登入方式
        else:
            data = ''
            
        r = self.session.post(
                'http://api.ubitdev.com/user/login',
                data=json.dumps(data),
                headers=self.headers
                )

        user_token = r.json()['data']['token']
        self.user_headers = {
            'Content-type': 'application/json',
            'token': user_token
            }
        
        return r.json()

    def getUserInfo(self):
        r = self.session.get('http://api.ubitdev.com/user/info', headers=self.user_headers)
        return r.json()

    def addPayment(self, account: str, bindType: int):
        self.sentVerify(886, 222222222, 6)

        data = {
            "bankAccount": account,
            "bankName": "string",
            "bankNumber": "string",
            "bindCardType": bindType,
            "branchName": "string",
            "googleVerifyCode": "string",
            "phoneVerifyCode": "string",
            "qrCodeName": "string"
            }

        self.session.post(
            'http://api.ubitdev.com/user/login',
            data=json.dumps(data),
            headers=self.headers
            )

    def getExchangeRate(self, coinId: int ,paymentTyoe: int):
        '''
        支付方式 0:銀行卡,1:支付寶,2:微信
        '''
        data = {
            "coinId": coinId,
            "paymentType": paymentTyoe
        }

        r = self.session.post(
                'http://api.ubitdev.com/coinTrade/both/getExchangeRate',
                data=json.dumps(data),
                headers=self.user_headers
                )
        return r.json()
    
    def showExchangeRate(self):
        coinId = {
            1: 'USDT',
            2: 'BTC',
            3: 'ETH'
        }

        paymentType = {
            0: '銀行卡',
            1: '支付寶',
            2: '微信'
        }

        exchange = {}
        for cId in coinId:
            exchange[coinId[cId]] = {}
            for pay in paymentType:
                exchange[coinId[cId]][paymentType[pay]] = {}
                r = self.getExchangeRate(cId, pay)
                exchange[coinId[cId]][paymentType[pay]] = {'buy': r['data']['buyPrice'], 'sell': r['data']['sellPrice']}
        return exchange


if __name__ == '__main__':
    from collections import Counter
    test = UbitFrontApiTest()

    # test.userLogin(886, 333333333, 2)
    # info = test.getUserInfo()
    # print(info)
    # rate = test.showExchangeRate()
    # print(rate)

    def merge_sort(arr):
        if len(arr) > 1:
            mid = len(arr) // 2
            left_half = arr[:mid]
            right_half = arr[mid:]
            
            merge_sort(left_half)
            merge_sort(right_half)
            
            i = j = k = 0
            
            while i < len(left_half) and j < len(right_half):
                if left_half[i] < right_half[j]:
                    arr[k] = left_half[i]
                    i += 1
                else:
                    arr[k] = right_half[j]
                    j += 1
                k += 1
                
            while i < len(left_half):
                arr[k] = left_half[i]
                i += 1
                k += 1
                
            while j < len(right_half):
                arr[k] = right_half[j]
                j += 1
                k += 1
    arr = [5, 2, 8, 3, 9, 1, 4, 6, 7]
    merge_sort(arr)
    print(arr)


