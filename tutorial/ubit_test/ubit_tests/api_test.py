import json
import requests
from .ubit_connection import DBconnection, DBSearch
import base64
from random import randint
from .googleAuthenticator import get_totp_token

img_path = 'C:/Users/Peter/Documents/Django_Server/tutorial/ubit_test/ubit_tests/'

class UbitAdminApiTest:
    def __init__(self, env: int, admin_account: str) -> None:
        # Admin SetUp
        self.env = env
        self.admin_account = admin_account
        
        self.headers = {'Content-type': 'application/json'}
        self.session = requests.Session()

        domains = {
            0: 'http://admin.ubitdev.com/',
            1: 'https://admin.ubitstg.com/api/'

        }

        self.domain = domains[self.env]
        self.conn = DBSearch(self.env)

        self.init_config = {}
        self.set_up_configs = {
            'manual_order_frozen_time': 1
        }
    
    def changeConfig(self, config_name: str, value: float):
        config_id, config_value, config_desc = self.conn.getConfig(config_name)

        if config_name not in self.init_config:
            self.init_config[config_name] = config_value
            config_value = value
        else:
            config_value = self.init_config[config_name]
        
        data = {
            "configDesc": config_desc,
            "configKey": config_name,
            "configValue": str(config_value),
            "id": config_id
        }

        r = self.session.post(
            self.domain+'config/systemConfig/update', 
            data=json.dumps(data),
            headers=self.headers
            )
        
        return r.json()
    
    def setUp(self):
        self.adminLogin()
        for k, v in self.set_up_configs.items():
            self.changeConfig(k, v)
    
    def rollBack(self):
        self.adminLogin()
        for k, v in self.set_up_configs.items():
            self.changeConfig(k, v)
    
    def adminLogin(self):
        # 登入後台取得session
        r = self.session.get(self.domain+f'login/test/{self.admin_account}')
        return True if r.json()['success'] else False

    def getIdentity(self, userId: int):
        data ={
            'userId': userId
        }

        r = self.session.post(
            self.domain+'user/getIdentity', 
            data=json.dumps(data),
            headers=self.headers
            )
        return r.json()

    def _uploadImg(self):
        with open(img_path+"1.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            encoded_string = encoded_string.decode('utf-8')
        data = {
            "img": "data:image/jpeg;base64,"+encoded_string
        }

        r = self.session.post(
            self.domain+'user/set/uploadFile', 
            data=json.dumps(data),
            headers=self.headers
            )
        return r.json()

    def modifyIdentity(self, identity_id: int):
        photo_path = self._uploadImg()['data']['path']

        data = {
            "id": identity_id,
            "identityPictureHandheld": photo_path
        }

        r = self.session.post(
            self.domain+'user/set/modifyIdentity', 
            data=json.dumps(data),
            headers=self.headers
            )
        return r.json()

    def passIdentity(self, identity_id: int):
        self.modifyIdentity(identity_id)
        
        data = {
            "id": identity_id,
            "identityNote": "ubit auto test: pass",
            "identityStatus": 2
        }

        r = self.session.post(
            self.domain+'user/set/updateIdentity', 
            data=json.dumps(data),
            headers=self.headers
            )
        return r.json()

    def _manualApply(self, amount: float, coin_id: int, user_id: int,
                     note: str='Ubit trunk manual apply: Add.'):
        '''
        coin_id: 1: USDT 2: BTC 3: ETH
        manual_type: 101 加幣-理賠
        '''
        coins = {1: 'USDT', 2: 'BTC', 3: 'ETH'}

        data = {
            "userId": user_id,
            "operator": "加币",
            "manualType": "理赔",
            "coinType": coins[coin_id],
            "amount": amount,
            "operateNote": note,
            "coinId": coin_id
            }
        r = self.session.post(
            self.domain+'assets/manual/apply', 
            data=json.dumps(data),
            headers=self.headers
            )
        return r.json()
    
    def _manualAudit(self, order_id, status: int, note: str='Ubit trunk manual audit.'):
        '''
        order_id: 訂單id
        status: 1:審核成功 2:審核失敗
        '''
        data = {
            "auditNote": note,
            "id": order_id,
            "status": status
        }

        r = self.session.post(
            self.domain+'assets/manual/audit', 
            data=json.dumps(data),
            headers=self.headers
            )
        return r.json()
    
    def manualApply(self, amount: float, user_id: int):
        '''
        coin_id: 1: USDT 2: BTC 3: ETH
        '''
        coins = {1: 'USDT', 2: 'BTC', 3: 'ETH'}
        for coin_id in range(1, 4):
            r = self._manualApply(amount, coin_id, user_id)
            if r['success']:
                print(f'{coins[coin_id]} 發起加幣 {amount}')
            else:
                print(f'{coins[coin_id]} 發起加幣 {amount} 失敗')

    def manualAudit(self):   
        orders = self.conn.getMunualAddOrders()
        
        if orders is None:
            print('No order need to audit.')
            return 
        for order in orders:
            r = self._manualAudit(order, 1)
            if r['success']:
                print(f'訂單: {order} 審核通過')
            else:
                print(f'訂單: {order} 審核失敗')
    
    def sellOrderAudit(self, order_id: str):
        data = {
            "note": "Ubit Trunk Audit: Fail.",
            "orderId": order_id,
            "reviewPass": False
        }

        r = self.session.post(
            self.domain+'sell/audit', 
            data=json.dumps(data),
            headers=self.headers
            )
        return r.json()
    
    def sellOrderFail(self, order_id: str):
        params = {'order_id': order_id}
        self.session.get(self.domain+'sell/manualFail', params=params)

    def clean24HrWithdrawLock(self, user_id: int):
        data = {
            "userId": user_id
        }

        r = self.session.post(
            self.domain+'user/set/withdrawLock', 
            data=json.dumps(data),
            headers=self.headers
            )
        return r.json()
    
    def openOptionTrade(self, user_id: int):
        data = {
            "status": 1,
            "userId": user_id
        }
        r = self.session.post(
            self.domain+'user/userInfo/set/updateOptionTradeSwitch', 
            data=json.dumps(data),
            headers=self.headers
            )
        return r.json()
    
    def openReleaseOrder(self, user_id: int):
        data = {
            "status": 1,
            "userId": user_id
        }
        r = self.session.post(
            self.domain+'user/userInfo/set/updateReleaseOrderSwitch', 
            data=json.dumps(data),
            headers=self.headers
            )
        return r.json()
    
    def releaseOrderAudit(self, apply_id: int, 
                          note: str='Ubit Trunk Audit.') -> dict:
        data = {
            "id": apply_id,
            "note": note,
            "reviewPass": True
        }
        r = self.session.post(
            self.domain+'c2c/release/audit', 
            data=json.dumps(data),
            headers=self.headers
            )
        return r.json()





        




class UbitFrontApiTest:
    def __init__(self, env: int, userId: int = -1) -> None:
        self.env = env
        self.userId = userId
        self.user_headers = {
            'Content-type': 'application/json',
            'api-version': '20221229'}
        self.session = requests.Session()
        self.conn = DBSearch(self.env)

        # config
        self.domain_dict = {
            0: 'http://api.ubitdev.com/',
            1: 'https://www.ubitstg.com/api/'
        }
        self.domain = self.domain_dict[self.env]

    
    def _sentVerify(self, areaCode: int, phone: int, verifyType: int) -> None:
        '''
        verifyType: 
        2登录 3登录密码 4支付密码 5.Google验证码 6新增银行卡 
        7设置新手机 8.修改银行卡验证码 9.校验手机验证码 10.確認已收款
        '''
        data = {
            "areaCode": areaCode,
            "phone": str(phone),
            "verifyType": verifyType
            }
        r = self.session.post(
            self.domain+'user/verifyCode/send',
            data=json.dumps(data),
            headers=self.user_headers
            )
    
    def _checkVerify(self, areaCode: int, phone: int, verifyType: int) -> None:

        data = {
            "areaCode": areaCode,
            "phone": str(phone),
            "verifyCode": "123456",
            "verifyType": verifyType
            }
        r = self.session.post(
            self.domain+'user/verifyCode/check',
            data=json.dumps(data),
            headers=self.user_headers
            )

    def _sentCaptcha(self) -> str:
        r = self.session.get(
            self.domain+'user/captcha'
        )
        return r.json()['data']['captchaToken']

    def _getCaptchaValue(self) -> tuple:
        '''
        key -> userLgoin: captchaToken
        key_ -> redis key
        '''
        key = self._sentCaptcha()
        conn = self.conn.ubitRedisConn()
        key_ = 'CAPTCHA:'+key
        return key, conn.get(key_)
    
    def _userLogin(self, areaCode: int, phone: int, loginType: int) -> dict:
        '''
        loginType: 1:密码登录 2:验证码登录
        '''
        if loginType == 2:
            self._sentVerify(areaCode, phone, 2)

            data = {
                "areaCode": areaCode,
                "captchaToken": "",
                "graphicalCode": "",
                "loginType": loginType,
                "password": "",
                "phone": str(phone),
                "verifyCode": "123456"
                }
            
        elif loginType == 1:
            capcha = self._getCaptchaValue()
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
                self.domain+'user/login',
                data=json.dumps(data),
                headers=self.user_headers
                )

        if r.json()['success']:
            # 更新user token
            user_token = r.json()['data']['token']
            self.user_headers['token'] = user_token
        
        return r.json()
    
    def getUserId(self):
        return self.userId
    
    def userLogin(self):
        try:
            user_info = self.conn.getUserInfo(self.userId)
            areaCode, phone = user_info['area_code'], user_info['mobile']
            r = self._userLogin(areaCode, phone, 2)
            return r
        except TypeError:
            print('This User is not existed.')
    
    def createUser(self, areaCode: int, phone: int):
        if not self.conn.isUserExisted(areaCode, phone):
            try:
                r = self._userLogin(areaCode, phone, 2)
                self.userId = self.conn.getUserId(areaCode, phone)
                return r
            except:
                print('Create User failed.')
        else:
            print('User is already existed.')
    
    def _setPassword(self, password_type: int, verifyCode: bool=True):
        '''
        password_type:
        重置密碼類型 3:登入密碼 4:資金密碼
        '''
        passwords = {
            3: '62c8ad0a15d9d1ca38d5dee762a16e01',
            4: 'e10adc3949ba59abbe56e057f20f883e'
        }
        data = {
            "googleAuthCode": "",
            "originalPassword": passwords[password_type],
            "password": passwords[password_type],
            "type": password_type,
            "verifyCode": "123456" if verifyCode else ""
        }

        r = self.session.post(self.domain+'user/set/password',
                          data=json.dumps(data),
                          headers=self.user_headers)
        return r.json()
    
    def newUserSetPassword(self):
        return self._setPassword(3, False)
    
    def newUserSetTradePassword(self):
        return self._setPassword(4, False)
    
    def changePassword(self):
        user_info = self.conn.getUserInfo(self.userId)
        area_code, mobile =  user_info['area_code'], user_info['mobile']
        self._sentVerify(area_code, mobile, 3)
        return self._setPassword(3)

    def changeTradePassword(self):
        user_info = self.conn.getUserInfo(self.userId)
        area_code, mobile =  user_info['area_code'], user_info['mobile']
        self._sentVerify(area_code, mobile, 4)
        return self._setPassword(4)
    
    def setPhoneNumber(self):
        user_info = self.conn.getUserInfo(self.userId)
        area_code, mobile =  user_info['area_code'], user_info['mobile']

        self._sentVerify(area_code, mobile, 9)
        self._checkVerify(area_code, mobile, 9)

        new_mobile = randint(100_000_000, 999_999_999)
        while self.conn.isUserExisted(area_code, new_mobile):
            new_mobile = randint(100_000_000, 999_999_999)
        
        self._sentVerify(area_code, new_mobile, 7)
        data = {
            "newAreaCode": 886,
            "newPhone": str(new_mobile),
            "verifyCode": "123456"
        }

        r = self.session.post(self.domain+'user/set/phone',
                          data=json.dumps(data),
                          headers=self.user_headers)
        print(f'New Phone: +886 {new_mobile}')
        return r.json()
    

    def getUserInfo(self):
        r = self.session.get(self.domain+'user/info', headers=self.user_headers)
        return r.json()
    
    def getUserProperty(self):
        data = {}
        r = self.session.post(self.domain+'assets/assetsList',
                          data=json.dumps(data),
                          headers=self.user_headers)
        if not r.json()['success']:
            print('Get User Property fail.')

        return r.json()

    def applyAuthenty(self, area: int, area_code: int, id_type: int) -> dict:
        '''
        area: 地區 0:中國大陸 1:其他區域
        area_code: 區域碼
        id_type: 證件類型 0:身分證 1:護照
        '''
        data = {
            "area": str(area),
            "areaCode": area_code,
            "identityNo": "123456789",
            "identityType": str(id_type),
            "trueName": "預發布"
        }

        r = self.session.post(
            self.domain+'user/realAuthenty',
            data=json.dumps(data),
            headers=self.user_headers
        )

        return r.json()
    
    def applyAuthentyDocuments(self) -> dict:
        with open(img_path+"1.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            encoded_string = encoded_string.decode('utf-8')

        data = {
            "identityPictureBack": encoded_string,
            "identityPictureFront": encoded_string,
            "identityPictureSign": encoded_string
        }
        r = self.session.post(
            self.domain+'user/realAuthentyDocuments',
            data=json.dumps(data),
            headers=self.user_headers
        )

        return r.json()
    
    def _createGoogleVerifyCode(self):
        data = {}

        r = self.session.post(
            self.domain+'user/set/createGoogleVerifyCode',
            data=json.dumps(data),
            headers=self.user_headers
        )

        return r.json()
    
    def setGoogleAuthenticator(self):
        secert_key = self._createGoogleVerifyCode()['data']['secretKey']
        google_verify_code = get_totp_token(secert_key)
        
        user_info = self.conn.getUserInfo(self.userId)
        area_code, mobile =  user_info['area_code'], user_info['mobile']
        
        self._sentVerify(area_code, mobile, 5)
        data = {
            "googleVerifyCode": str(google_verify_code),
            "phoneVerifyCode": "123456"
        }

        r = self.session.post(
            self.domain+'user/set/googleVerifyCode',
            data=json.dumps(data),
            headers=self.user_headers
        )

        return r.json()


    def addPayment(self, account: str='PeterUbit', bindCardType: int=0):
        user_info = self.conn.getUserInfo(self.userId)
        area_code = user_info['area_code']
        mobile = user_info['mobile']
        self._sentVerify(area_code, mobile, 6)
        bankNumber = randint(100_000_000_000_000_0, 999_999_999_999_999_999)
        data = {
            "bankAccount": account,
            "bankId": 1,
            "bankName": "中國工商銀行",
            "bankNumber": str(bankNumber),
            "bindCardType": bindCardType,
            "branchName": "",
            "googleVerifyCode": "",
            "phoneVerifyCode": "123456",
            "qrCodeName": ""
        }

        r = self.session.post(
            self.domain+'payment/addPaymentMode',
            data=json.dumps(data),
            headers=self.user_headers
            )
        return r.json()
    
    def getPaymentInfo(self):
        data = {}

        r = self.session.post(
            self.domain+'payment/paymentMsg',
            data=json.dumps(data),
            headers=self.user_headers
            )
        return r.json()
    
    def getExchangeRate(self, coinId: int ,paymentTyoe: int):
        '''
        支付方式 0:銀行卡,1:支付寶,2:微信
        '''
        data = {
            "coinId": coinId,
            "paymentType": paymentTyoe
        }

        r = self.session.post(
                self.domain+'coinTrade/both/getExchangeRate',
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
            2: '微信',
            3: '掛單'
        }

        exchange = {}
        for cId in coinId:
            exchange[cId] = {}
            for pay in paymentType:
                exchange[cId][pay] = {}
                r = self.getExchangeRate(cId, pay)
                exchange[cId][pay] = {'buy': r['data']['buyPrice'], 'sell': r['data']['sellPrice']}
        return exchange

    def withdraw(self, amount: float, coin_id: int, chain_id: int,
                 area_code: int=None, phone_number: int=None, adress: str=None):
        
        secrect_key = self.conn.getGoogleAuthSecretKey(self.userId)
        google_verify_code = get_totp_token(secrect_key)

        data = {
            "address": adress,
            "amount": amount,
            "areaCode": area_code,
            "chainId": chain_id,
            "coinId": coin_id,
            "googleVerifyCode": str(google_verify_code),
            "phone": str(phone_number),
            "token": "",
            "tradePassword": "e10adc3949ba59abbe56e057f20f883e"
        }

        r = self.session.post(
            self.domain+'assets/withdraw',
            data=json.dumps(data),
            headers=self.user_headers
            )
        
        return r.json()
    
    def applyReleaseOrder(self):
        data = {}
        r = self.session.post(
            self.domain+'releaseOrder/qualificationApply',
            data=json.dumps(data),
            headers=self.user_headers
            )
        
        return r.json()
    
    def _getTradeInit(self):
        data = {}
        r = self.session.post(
            self.domain+'coinTrade/both/init',
            data=json.dumps(data),
            headers=self.user_headers
            )
        
        return r.json()

    def getTradeLimit(self):
        '''
        coin_id: {1: 'USDT', 2: 'BTC', 3: 'ETH'}
        payment_type = {0: 'banks_c2c', 1: 'alipay', 2: 'weixin', 3: 'user_release_order'}
        '''
        exchange = self.showExchangeRate()
        trade_info = self._getTradeInit()
        sell_limit = trade_info['data']['coinTradeInfoList']
        plg_limit = trade_info['data']['plgGatewayInfoList']

        ubit_sell = {}
        plg_info = {}
        for coin_info in sell_limit:
            coin_ = coin_info['frontCoinInfoResponse']
            ubit_sell[coin_['coinId']] = {
                'sellMin': coin_['sellMin'],
                'sellMax': coin_['sellMax']
                }
        
        for plg in plg_limit:
            buy_min = plg['gatewayLimits']['min']
            buy_max = plg['gatewayLimits']['max']
            plg_info[plg['payType']] = {'buyMin': buy_min, 'buyMax': buy_max}

        res = {}
        for coin_id in range(1,4):
            res[coin_id] = {}
            for pay_way in range(3):
                res[coin_id][pay_way] = {}
                buy_min = plg_info[pay_way]['buyMin']/exchange[coin_id][pay_way]['buy']
                buy_max = plg_info[pay_way]['buyMax']/exchange[coin_id][pay_way]['buy']
                sell_min = ubit_sell[coin_id]['sellMin']
                sell_max = ubit_sell[coin_id]['sellMax']

                res[coin_id][pay_way] = {
                    'buyMin': buy_min,
                    'buyMax': buy_max,
                    'sellMin': sell_min,
                    'sellMax': sell_max
                }

        return res
    
    def applyBuy(self, coin_id: int, coin_amount: float, payType: int=0) -> dict:
        exchangeRate = self.getExchangeRate(coin_id, 0)['data']['buyPrice']

        data = {
            "coinAmount": coin_amount,
            "coinId": coin_id,
            "exchangeRate": exchangeRate,
            "legalAmount": coin_amount*exchangeRate,
            "mode": 0,
            "payType": payType,
            "tradePassword": "e10adc3949ba59abbe56e057f20f883e"
        }
        r = self.session.post(
            self.domain+'coinTrade/buy/apply',
            data=json.dumps(data),
            headers=self.user_headers
            )
        
        return r.json()
    
    def applySell(self, coin_id: int, coin_amount: float, payType: int=0) -> dict:
        exchangeRate = self.getExchangeRate(coin_id, 0)['data']['sellPrice']
        bank_id = self.conn.getUserPaymentId(payType, self.userId)

        data = {
            "coinAmount": coin_amount,
            "coinId": coin_id,
            "exchangeRate": exchangeRate,
            "legalAmount": coin_amount*exchangeRate,
            "mode": 0,
            "sellBankId": bank_id,
            "tradePassword": "e10adc3949ba59abbe56e057f20f883e"
        }
        r = self.session.post(
            self.domain+'coinTrade/sell/apply',
            data=json.dumps(data),
            headers=self.user_headers
            )
        
        return r.json()
    
    def createReleaseOrderStepOne(self, coin_id: int, order_type: int):
        '''
        order_type: 1:買幣 2:賣幣
        '''

        data = {}
        r = self.session.post(
            self.domain+'releaseOrder/step1',
            data=json.dumps(data),
            headers=self.user_headers
            )
        coins = r.json()['data']['c2cPriceList']

        for coin in coins:
            if coin['coinId'] == coin_id:
                if order_type == 1:
                    return coin['buyPrice']
                else:
                    return coin['sellPrice']
        return None
    
    def creatReleaseOrder(self, amount: int, coin_id: int, order_type: int,
                          price_type: int=1, trade_time_limit: int=30):
        '''
        order_type: 1:買幣 2:賣幣
        '''
        payment_id = self.conn.getUserPaymentId(0, self.userId)
        price = self.createReleaseOrderStepOne(coin_id, order_type)
        data = {
            "amount": amount,
            "coinId": coin_id,
            "currency": "CNY",
            "isInstantPublish": True,
            "isKycNeed": False,
            "lowerLimits": 0,
            "orderType": order_type,
            "paymentLit": [
                payment_id
            ],
            "price": price,
            "priceType": price_type,
            "registerDays": None,
            "successMessage": "Ubit trunk test",
            "tradeAgreement": "Ubit trunk test",
            "tradeTimeLimit": trade_time_limit,
            "upperLimits": amount*price,
            "usdtHoldAmount": None
        }
        r = self.session.post(
            self.domain+'releaseOrder/create',
            data=json.dumps(data),
            headers=self.user_headers
            )
        
        return r.json()
    
    def _getReleaseOrderDetail(self, order_id: str):
        r = self.session.get(
            self.domain+f'c2c/trade/release/detail/{order_id}',
            headers=self.user_headers)
        return r.json()
        
    
    def placeOrder(self, amount: float, order_id: str, payment_id: int):
        self._getReleaseOrderDetail(order_id)

        data = {
            "amount": amount,
            "releaseOrderId": order_id,
            "sellerBindId": payment_id
        }
        r = self.session.post(
            self.domain+'c2c/trade/order/create',
            data=json.dumps(data),
            headers=self.user_headers
            )
        
        return r.json()
    
    def comfirmPaid(self, order_id: str, payment_id: int):
        data = {
            "orderId": order_id,
            "sellerBindId": payment_id
        }

        r = self.session.post(
            self.domain+'c2c/trade/order/confirmPaid',
            data=json.dumps(data),
            headers=self.user_headers
            )
        
        return r.json()
    
    def confirmRecived(self, order_id: str):
        user_info = self.conn.getUserInfo(self.userId)
        area_code = user_info['area_code']
        mobile = user_info['mobile']
        
        self._sentVerify(area_code, mobile, 10)
        data = {
            "verifyCode": "123456"
        }
        r = self.session.post(
            self.domain+'/c2c/trade/order/confirmReceived/'+order_id,
            data=json.dumps(data),
            headers=self.user_headers
            )
        
        return r.json()


if __name__ == '__main__':
    pass

        
    

            
    
