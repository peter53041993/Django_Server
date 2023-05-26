import os 
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import unittest
from HTMLTestRunner import HTMLTestRunner
import time
from .api_test import UbitAdminApiTest, UbitFrontApiTest
import pandas as pd
from random import randint, random
from time import sleep

report_path = 'C:/Users/Peter/Documents/Django_Server/tutorial/ubit_test/report/'

class UbitTest(unittest.TestCase):
    def __init__(self, env: int, methodName: str = "runTest") -> None:
        super().__init__(methodName)

        # 0: dev, 1: stg
        self.env = env
        env_name_map = {
            0: "Ubit DEV",
            1: "Ublt STG"
        }
        self.env_name = env_name_map[env]

        admin_users = {
            0: ['admin', 'eddiec'],
            1: ['admin', 'peter_test']
            }
        self.amdin1, self.admin2 = admin_users[env]

        users = {
            0: 65,
            1: 1452485458
            }
        self.user = users[env]

        global admin_zero, admin_one, old_user, external_user
        admin_zero = UbitAdminApiTest(self.env, self.amdin1)
        admin_one = UbitAdminApiTest(self.env, self.admin2)
        old_user = UbitFrontApiTest(self.env, self.user)

        external_env = 0 if self.env == 1 else 0
        external_user = UbitFrontApiTest(external_env, users[external_env])

        self.coins = {1: 'USDT', 2: 'BTC', 3: 'ETH'}
        self.coin_chains = {0: 'Inner', 1: 'ERC20', 2: 'TRC20', 3: 'ETH', 4: 'BTC'}
        self.payment_type = {0: 'banks_c2c', 1: 'alipay', 2: 'weixin', 3: 'user_release_order'}
        

    def testAdminLogin(self):
        print('管理員登入測試')

        r1 = admin_zero.adminLogin()
        if r1:
            print(f'後台管理員: {self.amdin1} 登入成功')
        else:
            print(f'後台管理員: {self.amdin1} 登入失敗')
        
        r2 = admin_one.adminLogin()
        if r2:
            print(f'後台管理員: {self.admin2} 登入成功')
        else:
            print(f'後台管理員: {self.admin2} 登入失敗')

        self.assertEqual(r1, True)
        self.assertEqual(r2, True)
    
    def testUserLogin(self):
        print('舊用戶登入測試')

        r = old_user.userLogin()
        if r['success']:
            print(f'用戶 id: {self.user} 登入成功')
        else:
            print(f'用戶 id: {self.user} 登入失敗')
            print(f"code {r['code']}: {r['msg']}")
        self.assertEqual(r['success'], True)
    
    def testUserInfo(self):
        print('取得舊用戶資訊測試')

        # old_user.userLogin()
        r = old_user.getUserInfo()
        if r['success']:
            print(pd.Series(r['data']))
        self.assertEqual(r['success'], True)
    
    def testCreatUser(self):
        print('創建新用戶測試')

        global new_user

        mobile = randint(100_000_000, 999_999_999)
        # mobile = 222222222
        new_user = UbitFrontApiTest(self.env)
        r = new_user.createUser(886, mobile)
        if r:
            self.assertEqual(r['success'], True)
            print(f'新用戶: {new_user.getUserId()}' )
            print(f"{pd.Series(r['data'])} \n創建成功")
        else:
            print(f"新用戶創建失敗")
    
    def testNewUserInfo(self):
        print('取得新用戶資訊測試')

        r = new_user.getUserInfo()
        print(pd.Series(r['data']))
        self.assertEqual(r['success'], True)
    
    def testSetNewUser(self):
        print('設置新用戶密碼測試')

        r_set_password = new_user.newUserSetPassword()
        r_set_trade_password = new_user.newUserSetTradePassword()

        if r_set_password and r_set_trade_password:
            self.assertEqual(r_set_password['success'], True)
            self.assertEqual(r_set_trade_password['success'], True)
            print('新用戶\n登入密碼: 1234qwer\n交易密碼: 123456\n設置完成')
        elif not r_set_password:
            print('登入密碼設置失敗')
        elif not r_set_trade_password:
            print('交易密碼設置失敗')
        else:
            pass
    
    def testSetNewPhone(self):
        print('修改新用戶手機號碼測試')

        r = new_user.setPhoneNumber()
        if r:
            self.assertEqual(r['success'], True)
            print('新手機號碼設置完成')
    
    def testNewUserAuthenty(self):
        print('新用戶提交實名認證測試')

        auth_step_1 = new_user.applyAuthenty(0, 0, 0)
        auth_step_2 = new_user.applyAuthentyDocuments()

        if auth_step_1 and auth_step_2:
            if auth_step_1['success']:
                print('提交用戶資訊成功')
            if auth_step_2['success']:
                print('用戶上傳圖片成功')
            self.assertEqual(auth_step_1['success'], True)
            self.assertEqual(auth_step_2['success'], True)
    
    def testNewUserAuthentyPass(self):
        print('新用戶實名認證審核測試')

        identity_id = admin_zero.getIdentity(new_user.getUserId())['data']['id']
        r = admin_zero.passIdentity(identity_id)
        if r:
            if r['success']:
                print('新用戶實名認證審核通過')
            self.assertEqual(r['success'], True)
    
    def testNewUserSetGoogleAuthenticator(self):
        print('新用戶綁定google驗證碼測試')
        
        r = new_user.setGoogleAuthenticator()
        if r:
            if r['success']:
                print('google驗證碼綁定成功')
            self.assertEqual(r['success'], True)

    def testNewUserBindBank(self):
        r = new_user.addPayment()
        if r:
            if r['success']:
                print('銀行卡綁定成功')
                payment_info = new_user.getPaymentInfo()['data'][0]
                print(f'Payment:\n {pd.Series(payment_info)}')
            self.assertEqual(r['success'], True)
        
        
    def testManualAdd(self):
        amount = 100
        print('測試新用戶人工加幣: ', amount)

        print(f'用戶 {new_user.getUserId()}')
        print('\n加幣前 用戶資產: ')
        property = new_user.getUserProperty()
        print(f"總資產: {property['data']['totalBalance']}")
        print(f"暫不可用: {property['data']['totalFrozen']}")

        assetsList = property['data']['assetsList']
        
        check_amount_change = [[0, 0] for _ in range(len(self.coins))]
        for asset in assetsList:
            check_amount_change[asset['coinId']-1][0] = asset['frozen']
            print(f"幣種: {self.coins[asset['coinId']]}")
            print(pd.Series(asset))

        print('\n')
        admin_zero.manualApply(amount, new_user.getUserId())
        admin_one.manualAudit()
        print('\n')

        print('\n加幣後 用戶資產: ')
        property = new_user.getUserProperty()
        print(f"總資產: {property['data']['totalBalance']}")
        print(f"暫不可用: {property['data']['totalFrozen']}")

        assetsList = property['data']['assetsList']
        for asset in assetsList:
            check_amount_change[asset['coinId']-1][1] = asset['frozen']
            print(f"幣種: {self.coins[asset['coinId']]}")
            print(pd.Series(asset))
        

        for before, after in check_amount_change:
            self.assertEqual(after-before, amount)

        # waiting for forzen blance to be aviliable
        sleep(90)
    
    def testUserWithdraw(self):
        print('用戶充提幣測試:')
        print(f'用戶: {new_user.getUserId()} 提幣至 用戶: {old_user.getUserId()}')


        print(f'提幣用戶 {new_user.getUserId()}')
        print('\n提幣前 用戶資產: ')
        new_property = new_user.getUserProperty()
        print(f"總資產: {new_property['data']['totalBalance']}")
        print(f"暫不可用: {new_property['data']['totalFrozen']}")

        new_assetsList = new_property['data']['assetsList']
        
        new_check_amount_change = [[0, 0] for _ in range(len(self.coins))]
        for asset in new_assetsList:
            new_check_amount_change[asset['coinId']-1][0] = asset['frozen']
            print(f"幣種: {self.coins[asset['coinId']]}")
            print(pd.Series(asset))

        print(f'充幣用戶 {old_user.getUserId()}')
        print('\n充幣前 用戶資產: ')
        old_property = old_user.getUserProperty()
        print(f"總資產: {old_property['data']['totalBalance']}")
        print(f"暫不可用: {old_property['data']['totalFrozen']}")

        old_assetsList = old_property['data']['assetsList']
        
        old_check_amount_change = [[0, 0] for _ in range(len(self.coins))]
        for asset in old_assetsList:
            old_check_amount_change[asset['coinId']-1][0] = asset['frozen']
            print(f"幣種: {self.coins[asset['coinId']]}")
            print(pd.Series(asset))

        # Unlock New User Withdraw
        admin_zero.clean24HrWithdrawLock(new_user.getUserId())
        # set amount
        amount = 5

        target_user_id = old_user.getUserId()
        target_user_info = old_user.conn.getUserInfo(target_user_id)
        target_user_area_code, target_user_area_phone = target_user_info['area_code'], target_user_info['mobile']


        # Inner: USDT-Inner, BTC-Inner, ETH-Inner
        orders = []
        for i in range(1, 4):
            r = new_user.withdraw(amount, i, 0, target_user_area_code, target_user_area_phone)
            if r:
                if r['success']:
                    orders.append(r['data'])
                    print(f'站內手機轉帳發起成功，幣種: {self.coins[i]}')
                    print(f"訂單號: {r['data']}")
                else:
                    print(f'站內手機轉帳發起失敗，幣種: {self.coins[i]}')
                    print('失敗訊息: ', r['msg'])
        
        # Adress: USDT-ERC20, USDT-TRC20, BTC-BTC, ETH-ETH
        for coin_id, chainid in [(1, 1), (1, 2), (3, 3), (2, 4)]:
            r = new_user.withdraw(
                amount, coin_id, chainid,
                adress=old_user.conn.getUserVirtualAdress(target_user_id, coin_id, chainid)
                )
            if r:
                if r['success']:
                    orders.append(r['data'])
                    print(f'提幣發起成功，鏈: {self.coins[coin_id]}-{self.coin_chains[chainid]}')
                    print(f"訂單號: {r['data']}")
                else:
                    print(f'提幣發起失敗，鏈: {self.coins[coin_id]}-{self.coin_chains[chainid]}')
                    print('失敗訊息: ', r['msg'])
        
        # External Adress: USDT-ERC20, USDT-TRC20, BTC-BTC, ETH-ETH
        print(f"外部提幣用戶: {external_user.getUserId()}")
        external_amount = 0.5
        external_user_id = external_user.getUserId()
        for coin_id, chainid in [(1, 1), (1, 2), (3, 3), (2, 4)]:
            r = new_user.withdraw(
                external_amount, coin_id, chainid,
                adress=external_user.conn.getUserVirtualAdress(external_user_id, coin_id, chainid)
                )
            if r:
                if r['success']:
                    orders.append(r['data'])
                    print(f'外部提幣發起成功，鏈: {self.coins[coin_id]}-{self.coin_chains[chainid]}')
                    print(f"訂單號: {r['data']}")
                else:
                    print(f'外部提幣發起失敗，鏈: {self.coins[coin_id]}-{self.coin_chains[chainid]}')
                    print('失敗訊息: ', r['msg'])

        
        # 7 cases for now
        self.assertEqual(len(orders), 11)

        # waiting for orders done
        sleep(5)

        print('\n提幣後 用戶資產: ')
        new_property = new_user.getUserProperty()
        print(f"總資產: {new_property['data']['totalBalance']}")
        print(f"暫不可用: {new_property['data']['totalFrozen']}")

        new_assetsList = new_property['data']['assetsList']
        for asset in new_assetsList:
            new_check_amount_change[asset['coinId']-1][1] = asset['frozen']
            print(f"幣種: {self.coins[asset['coinId']]}")
            print(pd.Series(asset))
        

        print('\n充幣後 用戶資產: ')
        old_property = old_user.getUserProperty()
        print(f"總資產: {old_property['data']['totalBalance']}")
        print(f"暫不可用: {old_property['data']['totalFrozen']}")

        new_assetsList = old_property['data']['assetsList']
        for asset in new_assetsList:
            new_check_amount_change[asset['coinId']-1][1] = asset['frozen']
            print(f"幣種: {self.coins[asset['coinId']]}")
            print(pd.Series(asset))

    def testGetExchangeRate(self):
        print('獲取買賣幣匯率測試')

        rates = new_user.showExchangeRate()
        if rates:
            for k, v in rates.items():
                print(f'{self.coins[k]}:')
                for k_, v_ in v.items():
                    print(f"{self.payment_type[k_]}: {v_}")
        else:
            print('獲取買賣幣匯率失敗')
            self.assertEqual(True, False)
    
    def testApplyBuy(self):
        print('發起買幣訂單測試')

        trade_limit = new_user.getTradeLimit()

        orders = []
        for coin_id in self.coins:
            amount = round(trade_limit[coin_id][0]['buyMin']*1.1, 8)
            # amount = 1
            r = new_user.applyBuy(coin_id ,amount)
            if r:
                if r['success']:
                    print(f'{self.coins[coin_id]} 買幣訂單發起成功 {amount} {self.coins[coin_id]}')
                    print(f"訂單號: {r['data']['orderId']}")
                    orders.append(r['data']['orderId'])
                else:
                    print(f"買幣訂單發起失敗: {r['msg']}")
            sleep(2)

        self.assertEqual(len(orders), len(self.coins))

    def testApplySell(self):
        print('發起賣幣訂單測試')


        trade_limit = new_user.getTradeLimit()
        
        orders = []
        for coin_id in self.coins:
            amount = round(trade_limit[coin_id][0]['sellMin']*1.1, 8)
            # amount = 1
            r = new_user.applySell(coin_id ,amount)
            if r:
                if r['success']:
                    print(f'{self.coins[coin_id]} 賣幣訂單發起成功 {amount} {self.coins[coin_id]}')
                    print(f"訂單號: {r['data']['orderId']}")
                    orders.append(r['data']['orderId'])
                    admin_zero.sellOrderAudit(r['data']['orderId'])
                else:
                    print(f"賣幣訂單發起失敗: {r['msg']}")
            sleep(2)

        self.assertEqual(len(orders), len(self.coins))
    
    def openReleaseOrder(self):
        print('開啟自選和掛單開關')

        print(f'用戶: {new_user.getUserId()}')
        r = admin_zero.openOptionTrade(new_user.getUserId())
        if r['success']:
            print('自選交易開啟')
        else:
            print('自選交易開啟失敗')

        r = admin_zero.openReleaseOrder(new_user.getUserId())
        if r['success']:
            print('掛單交易開啟')
        else:
            print('掛單交易開啟失敗')
    
    def testApplyReleaseOrder(self):
        print('資質申請測試')

        r = new_user.applyReleaseOrder()
        if r:
            if r['success']:
                print(f"用戶: {new_user.getUserId()} 資質申請成功")
            else:
                print(f"用戶: {new_user.getUserId()} 資質申請失敗")
                print({r['msg']})
                self.assertEqual(True, False)
    
    def testAuditReleaseOrder(self):
        print('資質審核測試')

        user_id = new_user.getUserId()
        apply_id = new_user.conn.getApplyReleaseOrderId(user_id)
        r = admin_zero.releaseOrderAudit(apply_id)
        if r:
            if r['success']:
                print(f"用戶: {new_user.getUserId()} 申請ID: {apply_id} 資質審核成功")
            else:
                print(f"用戶: {new_user.getUserId()} 資質審核失敗")
                print({r['msg']})
                self.assertEqual(True, False)
    
    def testC2CtradeBuy(self):
        print('自選交易-買幣訂單交易測試')
        print(f'買家: {old_user.getUserId()} 賣家: {new_user.getUserId()}')
        amount = 1
        check_orders = []
        for coin_id in range(1, 4):
            order = new_user.creatReleaseOrder(amount, coin_id, 2)
            order_id = order['data']['orderId']
            if order['success']:
                print(f"{self.coins[coin_id]} 賣幣掛單成功: {order_id}")
            else:
                print(f"{self.coins[coin_id]} 賣幣掛單失敗")

            payment_id = new_user.conn.getUserPaymentId(0, new_user.getUserId())
            order = old_user.placeOrder(amount, order_id, payment_id)
            order_id = order['data']['orderId']
            if order['success']:
                print(f"{self.coins[coin_id]} 接單成功: {order_id}")
            else:
                print(f"{self.coins[coin_id]} 接單失敗")


            payment_id = old_user.conn.getUserPaymentId(0, old_user.getUserId())
            r = old_user.comfirmPaid(order_id, payment_id)
            if r['success']:
                print('買家確認付款完成')
            else:
                print('買家確認付款失敗')

            
            r = new_user.confirmRecived(order_id)
            if r['success']:
                print('賣家確認收款完成')
                check_orders.append(order_id)
            else:
                print('賣家確認收款失敗')

        print(f'完成自選賣幣訂單: {check_orders}')
    
    def testC2CtradeSell(self):
        print('自選交易-賣幣訂單交易測試')
        print(f'買家: {new_user.getUserId()} 賣家: {old_user.getUserId()}')
        amount = 1
        check_orders = []
        for coin_id in range(1, 4):
            order = new_user.creatReleaseOrder(amount, coin_id, 1)
            order_id = order['data']['orderId']
            if order['success']:
                print(f"{self.coins[coin_id]} 買幣掛單成功: {order_id}")
            else:
                print(f"{self.coins[coin_id]} 買幣掛單失敗")

            payment_id = old_user.conn.getUserPaymentId(0, old_user.getUserId())
            order = old_user.placeOrder(amount, order_id, payment_id)
            order_id = order['data']['orderId']
            if order['success']:
                print(f"{self.coins[coin_id]} 接單成功: {order_id}")
            else:
                print(f"{self.coins[coin_id]} 接單失敗")


            payment_id = new_user.conn.getUserPaymentId(0, new_user.getUserId())
            r = new_user.comfirmPaid(order_id, payment_id)
            if r['success']:
                print('買家確認付款完成')
            else:
                print('買家確認付款失敗')

            r = old_user.confirmRecived(order_id)
            if r['success']:
                print('賣家確認收款完成')
                check_orders.append(order_id)
            else:
                print('賣家確認收款失敗')

        print(f'完成自選買幣訂單: {check_orders}')

def runUbitTrunk(env: int):
    suite = unittest.TestSuite()
    tests = [
        UbitTest(env, 'testAdminLogin'), UbitTest(env, 'testUserLogin'),
        UbitTest(env, 'testUserInfo'), UbitTest(env, 'testCreatUser'),
        UbitTest(env, 'testSetNewUser') ,UbitTest(env, 'testNewUserInfo'),
        UbitTest(env, 'testSetNewPhone'), UbitTest(env, 'testNewUserAuthenty'),
        UbitTest(env, 'testNewUserAuthentyPass'), UbitTest(env, 'testNewUserSetGoogleAuthenticator'),
        UbitTest(env, 'testNewUserBindBank'),  UbitTest(env, 'testManualAdd'),
        UbitTest(env, 'testUserWithdraw'), 
        UbitTest(env, 'testGetExchangeRate'),
        UbitTest(env, 'testApplyBuy'), UbitTest(env, 'testApplySell'),
        UbitTest(env, 'openReleaseOrder'),
        UbitTest(env, 'testApplyReleaseOrder'), UbitTest(env, 'testAuditReleaseOrder'), 
        UbitTest(env, 'testC2CtradeSell'), UbitTest(env, 'testC2CtradeBuy')
    ]
    suite.addTests(tests)

    try:
        setter = UbitAdminApiTest(env, 'admin')
        setter.setUp()
        now = time.strftime('%Y_%m_%d^%H-%M-%S')
        filename = now + u'ubit_turnk' + '.html'
        fp = open(report_path+filename, 'w', encoding='UTF-8')
        runner = HTMLTestRunner.HTMLTestRunner(
                stream = fp,
                title = u'Ubit Trunk 測試報告',
                description = u'環境: %s' % ("Ubit DEV" if env == 0 else "Ubit STG"),
                )
        runner.run(suite)
        fp.close()
    finally:
        setter.rollBack()
    
    file = open(report_path+filename, 'rb')
    return file
    

if __name__ == '__main__':
    pass    