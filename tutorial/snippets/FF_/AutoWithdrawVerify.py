import cx_Oracle
import collections
import redis
import json
from typing import Union
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .betNums_config import BetNumsConfig

class checkFrontInput:
    def oracle(self, env: int) -> cx_Oracle:
        '''
        param: env -> envirment for DB, {0: dev02, 1: 188, 2: product}
        return cx_Oracle <class>
        '''
        if env == 2:
            username = 'rdquery'
            service_name = 'gamenxsXDB'
        else:
            username = 'firefog'
            service_name = ''

        oracle_ = {
            'password':['LF64qad32gfecxPOJ603', 'JKoijh785gfrqaX67854', 'eMxX8B#wktFZ8V'],
            'ip':['10.13.22.161', '10.6.1.41', '10.6.1.31'],
            'sid':['firefog', 'game',''],
            }
        
        password = oracle_['password'][env]
        host = oracle_['ip'][env]+':1521/'+oracle_['sid'][env]+service_name
        # host = f"{oracle_['ip'][env]}:1521/{oracle_['sid'][env]}{service_name}"

        conn = cx_Oracle.connect(username, password, host)
        return conn
    
    def verifyOrder(self, orderID, env) -> bool:
        sql = f'''SELECT 
	                fw.ID
                FROM 
	                FUND_WITHDRAW fw
                WHERE 
	                fw.SN = '{orderID}'
       ''' 
        conn = self.oracle(env)
        with conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
        conn.close()

        return True if rows else False

class AutoWithdrawVerify:
    def __init__(self, orderID: str, env=0)  -> None:
        self.env = env
        self.orderID = orderID
        self.account = self.getAccount()
        self.end_time = self.getApplyTime()
        self.defaultTime = self.end_time-relativedelta(months=3)
        self.betToZero = None
        self.prevWithDraw = None
        self.fristCharge = None
        self.prevCharge = None
        self.claen_point = self.getCleanPoint()
        self.rule12ManualPass = self.checkPeriodWithdrawLimitFlag()
        self.config = self.getHistoryConfig()

    def oracle(self, env: int) -> cx_Oracle:
        '''
        param: env -> envirment for DB, {0: dev02, 1: 188, 2: product}
        return cx_Oracle <class>
        '''
        if env == 2:
            username = 'rdquery'
            service_name = 'gamenxsXDB'
        else:
            username = 'firefog'
            service_name = ''

        oracle_ = {
            'password':['LF64qad32gfecxPOJ603', 'JKoijh785gfrqaX67854', 'eMxX8B#wktFZ8V'],
            'ip':['10.13.22.161', '10.6.1.41', '10.6.1.31'],
            'sid':['firefog', 'game',''],
            }
        
        password = oracle_['password'][env]
        host = oracle_['ip'][env]+':1521/'+oracle_['sid'][env]+service_name
        # host = f"{oracle_['ip'][env]}:1521/{oracle_['sid'][env]}{service_name}"

        conn = cx_Oracle.connect(username, password, host)
        return conn
    
    def redisConnection(self) -> redis.Redis:
        # 0:dev,1:188
        connect_data = {'ip': ['10.13.22.152', '10.6.1.82']}
        pool = redis.ConnectionPool(host=connect_data['ip'][self.env], port=6379)
        conn = redis.Redis(connection_pool=pool)
        return conn
    
    def _getRedisValue(self, key: str):
        '''
        清零點key
        WITHDRAW_RISK_ZEROIZE_TIME:{userId}

        舊版清零點key
        withdrawRisk{userId}

        規則  超过累计提款金额 人工通過審核 key
        WITHDRAW_AMOUNT_MANUAL_PASS:{userId}

        return: timestamp
        '''
        conn = self.redisConnection()
        res = (conn.get(key))
        if not key:
            return None
        else:
            return res
    
    def getAccountInfo(self) -> dict:
        sql = f'''SELECT id, account FROM user_customer WHERE id = {self.account}
        '''
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql)
            account = cursor.fetchall()[0][1]
        conn.close()

        return {
            'userId': self.account,
            'account': account
        }

    def getRedisTimePoint(self) -> dict:
        nweBetToZero = self._getRedisValue(f'WITHDRAW_RISK_ZEROIZE_TIME:{self.account}')
        betToZero = self._getRedisValue(f'withdrawRisk{self.account}')
        # Rule: 12 flag
        manualPassRule12 = self._getRedisValue(f'WITHDRAW_AMOUNT_MANUAL_PASS:{self.account}')
        if nweBetToZero:
            timestamps = float(nweBetToZero.decode())/1000
            nweBetToZero = datetime.fromtimestamp(timestamps).strftime('%Y-%m-%d %H:%M:%S')
        if betToZero:
            timestamps = float(betToZero.decode())/1000
            betToZero = datetime.fromtimestamp(timestamps).strftime('%Y-%m-%d %H:%M:%S')
        if manualPassRule12:
            timestamps = float(manualPassRule12.decode())/1000
            manualPassRule12 = datetime.fromtimestamp(timestamps).strftime('%Y-%m-%d %H:%M:%S')

        return {
            'nweBetToZero': nweBetToZero,
            'betToZero': betToZero,
            'manualPassRule12': manualPassRule12
        }

    def getConfig(self) -> dict:
        sql = f'''SELECT VALUE FROM config WHERE KEY = 'auto_withdraw_config'
        '''
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchall()[0][0]
        conn.close()
        return json.loads(row)

    #清零點 -> 提現成功 -> 第一次充值成功 -> 固定三個月
    def getCleanPoint(self) -> datetime:
        end_time = self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        sql_betToZero = f'''SELECT 
                            max(fcl.GMT_CREATED)
                        FROM 
                            FUND_CHANGE_LOG fcl 
                        WHERE 
                            fcl.USER_ID = {self.account}
                            AND (fcl.CT_BAL/10000) < 1
                            AND fcl.REASON = 'GM,DVCB,null,1'
                            AND fcl.GMT_CREATED < TO_TIMESTAMP('{end_time}', 'YYYY-MM-DD HH24:MI:SS')
        '''
        sql_prevWithDraw = f'''SELECT 
                                max(fw.APPLY_TIME)
                            FROM 
                                FUND_WITHDRAW fw 
                            WHERE 
                                fw.USER_ID = {self.account}
                                AND fw.STATUS = 4
                                AND fw.APPLY_TIME < TO_TIMESTAMP('{end_time}', 'YYYY-MM-DD HH24:MI:SS')
        '''
        sql_fristCharge = f'''SELECT 
                                min(fc.APPLY_TIME), max(fc.APPLY_TIME)
                            FROM
                                FUND_CHARGE fc 
                            WHERE 
                                fc.USER_ID = {self.account} 
                                AND fc.STATUS = 2
        '''

        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql_betToZero)
            betToZero = cursor.fetchall()[0][0]
            if betToZero: 
                self.betToZero = betToZero

            cursor.execute(sql_prevWithDraw)
            prevWithDraw = cursor.fetchall()[0][0]
            if prevWithDraw: 
                self.prevWithDraw = prevWithDraw

            cursor.execute(sql_fristCharge)
            rows = cursor.fetchall()[0]
            fristCharge = rows[0]
            if fristCharge: 
                self.fristCharge = fristCharge
            prevCharge = rows[1]
            if prevCharge:
                self.prevCharge = prevCharge
        conn.close()

        # 比較舊redis清零點，若新redis沒有值，用舊redis值取代
        if not betToZero:
            old_point = self._getRedisValue(f'withdrawRisk{self.account}')
            if old_point:
                timestamps = float(old_point.decode())/1000
                old_point = datetime.fromtimestamp(timestamps)
            betToZero = old_point

        if betToZero and prevWithDraw:
            if betToZero > prevWithDraw:
                return betToZero
            else:
                return prevWithDraw
        elif betToZero:
            return betToZero
        elif prevWithDraw:
            return prevWithDraw
        elif fristCharge:
            return fristCharge
        else:
            return self.defaultTime
    
    def getCleanPointValue(self):
        return {
            'claen_point': self.claen_point.strftime('%Y-%m-%d %H:%M:%S'),
            'betToZero': self.betToZero.strftime('%Y-%m-%d %H:%M:%S') if self.betToZero else None,
            'prevWithDraw': self.prevWithDraw.strftime('%Y-%m-%d %H:%M:%S') if self.prevWithDraw else None,
            'fristCharge': self.fristCharge.strftime('%Y-%m-%d %H:%M:%S') if self.fristCharge else None,
            'prevCharge': self.prevCharge.strftime('%Y-%m-%d %H:%M:%S') if self.prevCharge else None,
            'rule12ManualPass': self.rule12ManualPass.strftime('%Y-%m-%d %H:%M:%S') if self.rule12ManualPass else None
        }


    def getApplyTime(self) -> datetime:
        sql = f'''SELECT 
	                fw.APPLY_TIME 
                FROM 
	                FUND_WITHDRAW fw
                WHERE 
	                fw.SN = '{self.orderID}'
       ''' 
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
        conn.close()
        
        return rows[0][0]
    
    def getAccount(self) -> int:
        sql = f'''SELECT 
	                fw.USER_ID 
                FROM 
	                FUND_WITHDRAW fw
                WHERE 
	                fw.SN = '{self.orderID}'
        '''
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
        conn.close()

        return rows[0][0]

    def checkPeriodWithdrawLimitFlag(self) -> Union[datetime, None]:
        endTime = self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        sql = f'''SELECT 
                    fw.APPLY_TIME,
                    (CASE 
                        WHEN fw.APPR2_TIME IS NULL THEN fw.APPR_TIME 
                        ELSE fw.APPR2_TIME END) AS verTime
                FROM 
                    FUND_WITHDRAW fw 
                WHERE 
                    fw.USER_ID = {self.account}
                    AND fw.RISK_TYPE = 23
                    AND	fw.STATUS = 4
                    AND fw.APPLY_TIME < TO_TIMESTAMP('{endTime}', 'YYYY-MM-DD HH24:MI:SS')
                ORDER BY
                    verTime DESC
        '''
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
        conn.close()

        return res[0][0] if res else None
    
    # Rule1: 参与三方游戏
    def isThirdly(self) -> dict:
        start_time = self.prevCharge if self.prevCharge else self.defaultTime
        start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time = self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        sql = f'''SELECT 
	                ctbr.SEQ_ID
                FROM 
	                COLLECT_THIRDLY_BET_RECORD ctbr 
                WHERE
	                ctbr.USER_ID = {self.account} 
                    AND ctbr.THIRDLY_BET_TIME >= TO_TIMESTAMP('{start_time}', 'YYYY-MM-DD HH24:MI:SS')
                    AND ctbr.THIRDLY_BET_TIME < TO_TIMESTAMP('{end_time}', 'YYYY-MM-DD HH24:MI:SS')
        '''
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
        conn.close()

        return {
            'result': True if rows else False,
            'startTime': start_time,
            'endTime': end_time
        }
    
    # Rule2: 已打流水 < 充值金额 X倍
    def isFlow(self) -> dict:
        # x先預設常數:
        muti = float(self.config['BET_REQUIRED']['times'])

        startTtime = self.claen_point.strftime('%Y-%m-%d %H:%M:%S')
        endTime = self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        flow_sql = f'''SELECT  
                    NVL(SUM(TOTAMOUNT-TOTAL_RED_DISCOUNT)/10000, 0)
                FROM 
                    GAME_ORDER
                WHERE
                    USERID = {self.account}
                    and ORDER_TIME >= TO_TIMESTAMP('{startTtime}', 'YYYY-MM-DD HH24:MI:SS')
                    and ORDER_TIME < TO_TIMESTAMP('{endTime}', 'YYYY-MM-DD HH24:MI:SS')
                    and STATUS in (2, 3)
        '''
        charge_sql = f'''SELECT 
                            NVL(SUM(fc.REAL_CHARGE_AMT)/10000, 0)
                        FROM
                            FUND_CHARGE fc 
                        WHERE 
                            fc.USER_ID = {self.account}
                            AND fc.STATUS = 2
                            AND fc.APPLY_TIME >= TO_TIMESTAMP('{startTtime}', 'YYYY-MM-DD HH24:MI:SS')
                            AND fc.APPLY_TIME < TO_TIMESTAMP('{endTime}', 'YYYY-MM-DD HH24:MI:SS')
        '''
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(flow_sql)
            flow = cursor.fetchall()[0][0]
            cursor.execute(charge_sql)
            charge = cursor.fetchall()[0][0]
        conn.close()

        # print(flow, charge)

        return {
            'result': True if flow < charge*muti or charge == 0 else False,
            'flow': flow,
            'charge': charge,
            'muti': muti,
            'startTime': startTtime,
            'endTime': endTime
        }

    
    # Rule3: 黑名单
    def isBlackList(self) -> dict:
        sql_userBlack = f'''SELECT 
                                ub.ACCOUNT
                            FROM 
                                USER_BLACKLIST ub 
                            WHERE 
                                ub.ACCOUNT = (SELECT account FROM USER_CUSTOMER WHERE id = {self.account})
                                AND ub.USER_STATUS = 'ENABLE'
        '''
        sql_withdrawBlack = f'''SELECT 
                                    uwb.ACCOUNT
                                FROM 
                                    USER_WITHDRAW_BLACKLIST uwb 
                                WHERE 
                                    uwb.ACCOUNT IN (SELECT bank_account FROM USER_BANK ub WHERE ub.USER_ID = {self.account})
                                    AND uwb.USER_STATUS = 'ENABLE'
        '''
        sql_susCard = f'''SELECT 
                            fsc.CARD_NUMBER
                        FROM 
                            FUND_SUSPICIOUS_CARD fsc 
                        WHERE 
                            fsc.CARD_NUMBER IN (SELECT BANK_NUMBER FROM USER_BANK ub WHERE ub.USER_ID = {self.account})
                            OR fsc.CARD_NUMBER IN (SELECT DIGITAL_CURRENCY_WALLET FROM USER_BANK ub WHERE ub.USER_ID = {self.account})
        '''
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql_userBlack)
            userBlack = cursor.fetchall()

            cursor.execute(sql_withdrawBlack)
            withdrawBlack = cursor.fetchall()

            cursor.execute(sql_susCard)
            susCard = cursor.fetchall()
        conn.close()
        
        trigger = {}

        if userBlack:
            trigger['用户名黑名单管理'] = [d[0] for d in userBlack]
        if withdrawBlack:
            trigger['绑定姓名黑名单管理'] = [d[0] for d in withdrawBlack]
        if susCard:
            trigger['银行卡黑名单管理'] = [d[0] for d in susCard]

        return {
            'result': True if trigger else False,
            'trigger': trigger
        }
    
    # Rule4: 活动参与
    def isActivityReward(self) -> dict:
        startTime = self.claen_point.strftime('%Y-%m-%d %H:%M:%S')
        endTime = self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        sql = f'''SELECT 
                    fcl.SN
                FROM 
                    FUND_CHANGE_LOG fcl 
                WHERE 
                    fcl.USER_ID = {self.account}
                    AND fcl.REASON IN ('PM,PGXX,null,4', 'PM,PGXX,null,5', 'PM,TAAM,null,3', 'PM,PGXX,null,3')
                    AND fcl.GMT_CREATED >= TO_TIMESTAMP('{startTime}', 'YYYY-MM-DD HH24:MI:SS')
                    AND fcl.GMT_CREATED < TO_TIMESTAMP('{endTime}', 'YYYY-MM-DD HH24:MI:SS')
        '''
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
        conn.close()

        sn = []
        if res:
            sn = [d[0] for d in res] 

        return {
            'result': True if res else False,
            'sn': sn,
            'startTime': startTime,
            'endTime': endTime
        }

    
    # Rule5: 风控标签
    def isRiskTag(self) -> dict:
        sql = f'''SELECT 
                    uc.MAIN_TAG 
                FROM 
                    USER_CUSTOMER uc 
                WHERE 
                    uc.ID = {self.account}
        '''
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
        conn.close()

        return {
            'result': True if res and res[0][0] else False,
            'tag': res[0][0]
        }
    
    # Rule6: 单笔申请提款金额 > X 元
    def withdrawLimit(self) -> dict:
        # 先給常數
        amount_limit = float(self.config['LARGE_AMOUNT']['limit'])

        sql = f'''SELECT 
                    (CASE WHEN fw.IS_SEPERATE = 'N' THEN NVL(fw.WITHDRAW_AMT/10000, 0)
	                ELSE (SELECT SUM(NVL(WITHDRAW_AMT/10000, 0)) FROM FUND_WITHDRAW WHERE ROOT_SN = fw.ROOT_SN) END) AS　"Amount"
                FROM 
                    FUND_WITHDRAW fw 
                WHERE 
                    fw.SN = '{self.orderID}'
        '''  
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql)
            amount = cursor.fetchall()[0][0]
        conn.close()

        return {
            'result': True if amount > amount_limit else False,
            'limit': amount_limit,
            'withdraw': amount
        }    

    # Rule7: 首次使用USDT提款金额 > USDT
    def firstUSDT(self) -> dict:
        limit_amount = float(self.config['FIRST_TIME_USDT']['limit'])

        endTime = self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        sql_fristUse = f'''SELECT 
                            USER_BANK_STRUC
                        FROM 
                            FUND_WITHDRAW fw 
                        WHERE 
                            fw.USER_ID = {self.account}
                            AND fw.APPLY_TIME < TO_TIMESTAMP('{endTime}', 'YYYY-MM-DD HH24:MI:SS')
        '''
        sql_curBindType = f'''SELECT 
                            fw.USER_BANK_STRUC, NVL((fw.WITHDRAW_AMT/10000)/EXCHANGE_RATE, 0)
                        FROM 
                            FUND_WITHDRAW fw 
                        WHERE 
                            fw.SN = '{self.orderID}'
        '''
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql_fristUse)
            fristUse = cursor.fetchall()

            cursor.execute(sql_curBindType)
            cur = cursor.fetchall()
        conn.close()

        curBindType = json.loads(cur[0][0])['bindcardType']
        curWithdrawAmount = cur[0][1]
        bindType =[]
        if fristUse:
            bindType = [json.loads(d[0])['bindcardType'] for d in fristUse]
        
        res = True if curBindType == 2 and curBindType not in bindType and curWithdrawAmount > limit_amount else False

        return {
            'result': res,
            'whithType': curBindType,
            'withInPast': True if 2 in bindType else False,
            'WithdrawAmount': curWithdrawAmount,
            'limit_amount': limit_amount
        }

    def isSamePrevWithCardId(self) -> bool:
        endTime = self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        prev_sql = f'''SELECT 
                    USER_BANK_STRUC
                FROM 
                    FUND_WITHDRAW fw 
                WHERE 
                    fw.USER_ID = {self.account}
                    AND fw.STATUS = 4
                    AND fw.APPLY_TIME < TO_TIMESTAMP('{endTime}', 'YYYY-MM-DD HH24:MI:SS')
                ORDER BY
	                fw.APPLY_TIME DESC
        '''
        cur_sql = f'''SELECT 
                    USER_BANK_STRUC
                FROM 
                    FUND_WITHDRAW fw 
                WHERE 
                    fw.SN = '{self.orderID}'
	    '''
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(prev_sql)
            prev = cursor.fetchall()

            cursor.execute(cur_sql)
            cur = cursor.fetchall()
        conn.close()

        if not prev:
            return True
        return json.loads(prev[0][0])['id'] == json.loads(cur[0][0])['id'] 

    # Rule8: X 天内提款账号信息有过变更用户
    def isChangeInfo(self) -> dict:
        timeDelta = int(self.config['CARD_INFO_CHANGED']['days'])
        startTime = (self.end_time-relativedelta(days=timeDelta)).strftime('%Y-%m-%d %H:%M:%S')
        endTime = self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        sql_bind = f'''SELECT 
                        ID
                    FROM 
                        USER_BANK_BIND_HISTORY ubbh 
                    WHERE 
                        ubbh.USER_ID = {self.account}
                        AND ubbh.ACTION_TIME >= TO_TIMESTAMP('{startTime}', 'YYYY-MM-DD HH24:MI:SS') 
                        AND ubbh.ACTION_TIME < TO_TIMESTAMP('{endTime}', 'YYYY-MM-DD HH24:MI:SS')
        '''
        sql_lock = f'''SELECT 
                        ID
                    FROM 
                        USER_BANK_OPERATE_LOG ubol 
                    WHERE 
                        ubol.BANK_LOCKED_ID IN (SELECT ID FROM USER_BANK_LOCKED WHERE USER_ID = {self.account})
                        AND ubol.OPERATE_DATE >= TO_TIMESTAMP('{startTime}', 'YYYY-MM-DD HH24:MI:SS') 
                        AND ubol.OPERATE_DATE < TO_TIMESTAMP('{endTime}', 'YYYY-MM-DD HH24:MI:SS')
        '''
        
        sql_curBindType = f'''SELECT 
                            USER_BANK_STRUC
                        FROM 
                            FUND_WITHDRAW fw 
                        WHERE 
                            fw.SN = '{self.orderID}'
        '''

        sql_fristUse = f'''SELECT 
                            USER_BANK_STRUC
                        FROM 
                            FUND_WITHDRAW fw 
                        WHERE 
                            fw.USER_ID = {self.account}
                            AND fw.APPLY_TIME < TO_TIMESTAMP('{endTime}', 'YYYY-MM-DD HH24:MI:SS')
        '''

        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql_bind)
            bind = cursor.fetchall()
            
            cursor.execute(sql_lock)
            lock = cursor.fetchall()

            cursor.execute(sql_curBindType)
            cur = cursor.fetchall()

            cursor.execute(sql_fristUse)
            fristUse = cursor.fetchall()
        conn.close()

        curBindType = json.loads(cur[0][0])['bindcardType']
        
        bindType =[]
        if fristUse:
            bindType = [json.loads(d[0])['bindcardType'] for d in fristUse]
            

        trigger = []
        if bind or lock:
            trigger.append('添加/刪除提款資料')
        if not self.isSamePrevWithCardId():
            trigger.append('與上次提款不同卡號')
        if curBindType not in bindType:
            trigger.append('首次使用提款類型')

        return {

            'result': True if trigger else False,
            'trigger': trigger,
            'timeDelta': timeDelta,
            'startTime': startTime,
            'endTime': endTime
        }
    
    # Rule9: 没有充值行为，但是有加币行为 X 元以上
    def isManualCharge(self) -> dict:
        limit = float(self.config['NO_RECHARGE']['limit'])
        startTime = self.claen_point.strftime('%Y-%m-%d %H:%M:%S')
        endTime = self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        sql_charge = f'''SELECT 
                            NVL(SUM(fc.REAL_CHARGE_AMT)/10000, 0)
                        FROM
                            FUND_CHARGE fc 
                        WHERE 
                            fc.USER_ID = {self.account}
                            AND fc.STATUS = 2
                            AND fc.APPLY_TIME >= TO_TIMESTAMP('{startTime}', 'YYYY-MM-DD HH24:MI:SS')
                            AND fc.APPLY_TIME < TO_TIMESTAMP('{endTime}', 'YYYY-MM-DD HH24:MI:SS')
        '''
        sql_increase = f'''SELECT 
                            NVL(SUM(abs(CT_BAL-BEFOR_BAL)/10000), 0)
                        FROM 
                            FUND_CHANGE_LOG fcl 
                        WHERE 
                            fcl.USER_ID = {self.account}
                            AND fcl.REASON IN ('PM,TAAM,null,3','PM,PGXX,null,3','PM,IPXX,null,3','TF,BIRX,null,2','OT,CEXX,null,3','OT,AAXX,null,3','GM,DDAX,null,1','PM,PMXX,null,3','PM,TSVA,null,3','PM,TSVA,null,1','OT,PCXX,null,3',
                            'TF,DLSY,null,1','TF,MLDD,null,1','TF,TADS,null,3','TF,ZDYJ,null,1','PM,AADS,null,3','PM,AAMD,null,3','TF,LMLD,null,1','TF,DABR,null,1','TF,DTWR,null,3','TF,XFYJ,null,1','GM,SFYJ,null,1',
                            'GM,SFFS,null,1','HB,AHBC,null,1','PM,RHYB,null,3','PM,RHYB,null,4','PM,RHYB,null,5','PM,RHYB,null,6','PM,RHYB,null,7','PM,RHYB,null,8','PM,RHYB,null,9','PM,SVUR,null,1','PM,SVUR,null,2',
                            'GM,RHAX,null,2')
                            AND fcl.GMT_CREATED >= TO_TIMESTAMP('{startTime}', 'YYYY-MM-DD HH24:MI:SS')
                            AND fcl.GMT_CREATED < TO_TIMESTAMP('{endTime}', 'YYYY-MM-DD HH24:MI:SS')
        '''
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql_charge)
            charge = cursor.fetchall()[0][0]
            
            cursor.execute(sql_increase)
            increase = cursor.fetchall()[0][0]
        conn.close()
        
        return {
            'result': True if charge==0 and increase > limit else False,
            'charge': charge,
            'increase': increase,
            'limit':limit,
            'startTime': startTime,
            'endTime': endTime
        }
    
    # Rule10: 1、新会员第 X 次充值以上才不算新会员
    #         2、梭哈（下注金额超过>=金额 X% 以上）
    def newUserAndShowHand(self):
        limit_charges_times = int(self.config['SHOW_HAND']['count'])

        endTime = self.end_time.strftime('%Y-%m-%d %H:%M:%S')

        sql_chargeTimes = f'''SELECT 
                            count(id), NVL(SUM(fc.REAL_CHARGE_AMT)/10000, 0)
                        FROM
                            FUND_CHARGE fc 
                        WHERE 
                            fc.USER_ID = {self.account}
                            AND fc.STATUS = 2
                            AND fc.APPLY_TIME < TO_TIMESTAMP('{endTime}', 'YYYY-MM-DD HH24:MI:SS')
        '''
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql_chargeTimes)
            rows = cursor.fetchall()[0]
            charge_times = rows[0]
        conn.close()
        

        return {
            'result': True if charge_times <= limit_charges_times else False,
            'charge_times': charge_times,
            'limit_charges_times': limit_charges_times,
            'endTime': endTime
        }
    
    # Rule11: 当日提款次数超过 X 次，且累计提款超过 X 元
    def dailyWithdrawLimit(self) -> dict:
        limit_amount = float(self.config['WITHDRAW_COUNT_LIMIT']['amount'])
        limit_times = int(self.config['WITHDRAW_COUNT_LIMIT']['count'])
        startTime = self.end_time.strftime('%Y-%m-%d')
        endTime = self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        # 須計入自身這筆提現，結束時間+1秒
        useEndTime = (self.end_time+relativedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')

        sql = f'''SELECT 
                    count(0), NVL(SUM(g."amount"), 0)
                FROM
                    (SELECT 
                        NVL(SUM(fw.REAL_WITHDRAL_AMT)/10000, 0) AS "amount"
                    FROM 
                        FUND_WITHDRAW fw 
                    WHERE 
                        fw.USER_ID = {self.account}
                        AND fw.APPLY_TIME >= TO_TIMESTAMP('{startTime} 00:00:00', 'YYYY-MM-DD HH24:MI:SS') 
                        AND fw.APPLY_TIME < TO_TIMESTAMP('{useEndTime}', 'YYYY-MM-DD HH24:MI:SS')
                    GROUP BY
                        fw.ROOT_SN) g
        '''
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()[0]
            withdraw_times = rows[0]
            amount = rows[1]
        conn.close()

        return {
            'result': True if withdraw_times > limit_times or amount > limit_amount else False,
            'withdraw_times' : withdraw_times,
            'limit_times': limit_times,
            'amount': amount,
            'limit_amount': limit_amount,
            'startTime': f'{startTime} 00:00:00',
            'endTime': endTime
        }
    
    # Rule12: X 天内提款成功总和大于 Y 元
    def periodWithdrawLimit(self) -> dict:
        limit_amount = float(self.config['WITHDRAW_AMOUNT_LIMIT']['amount'])
        days = int(self.config['WITHDRAW_AMOUNT_LIMIT']['days'])

        flagTrigger = False
        flagTime = self.rule12ManualPass
        if flagTime and flagTime > (self.end_time-relativedelta(days=days)):
            startTime = flagTime.strftime('%Y-%m-%d %H:%M:%S')
            flagTrigger = True
        else:
            startTime = (self.end_time-relativedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')

        endTime = self.end_time.strftime('%Y-%m-%d %H:%M:%S')

        sql_withdraw = f'''SELECT 
                    NVL(SUM(fw.REAL_WITHDRAL_AMT)/10000, 0)
                FROM 
                    FUND_WITHDRAW fw 
                WHERE 
                    fw.USER_ID = {self.account}
                    AND fw.STATUS = 4
                    AND fw.APPLY_TIME >= TO_TIMESTAMP('{startTime}', 'YYYY-MM-DD HH24:MI:SS') 
                    AND fw.APPLY_TIME < TO_TIMESTAMP('{endTime}', 'YYYY-MM-DD HH24:MI:SS')
        '''
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql_withdraw)
            amount = cursor.fetchall()[0][0]
        conn.close()

        return {
            'result': True if amount > limit_amount else False,
            'amount': amount,
            'limit_amount': limit_amount,
            'days': days,
            'flagTrigger': flagTrigger,
            'startTime': startTime,
            'endTime': endTime
        }
    
    # Rule13: 提充比：提款金额/充值金额 >= X 倍，且盈利金额 > Y 元
    def ratioOfWD(self) -> dict:
        ratio = float(self.config['WITHDRAW_RECHARGE_RATIO']['times'])
        limit_amount = float(self.config['WITHDRAW_RECHARGE_RATIO']['amount'])

        startTime = self.defaultTime.strftime('%Y-%m-%d %H:%M:%S')
        endTime = self.end_time.strftime('%Y-%m-%d %H:%M:%S')

        sql_charge = f'''SELECT 
                            NVL(SUM(fc.REAL_CHARGE_AMT)/10000, 0)
                        FROM
                            FUND_CHARGE fc 
                        WHERE 
                            fc.USER_ID = {self.account}
                            AND fc.STATUS = 2
                            AND fc.APPLY_TIME >= TO_TIMESTAMP('{startTime}', 'YYYY-MM-DD HH24:MI:SS')
                            AND fc.APPLY_TIME < TO_TIMESTAMP('{endTime}', 'YYYY-MM-DD HH24:MI:SS')
        '''

        sql_withdraw = f'''SELECT 
                            NVL(SUM(fw.REAL_WITHDRAL_AMT)/10000, 0)
                        FROM 
                            FUND_WITHDRAW fw 
                        WHERE 
                            fw.USER_ID = {self.account}
                            AND fw.STATUS = 4
                            AND fw.APPLY_TIME >= TO_TIMESTAMP('{startTime}', 'YYYY-MM-DD HH24:MI:SS') 
                            AND fw.APPLY_TIME < TO_TIMESTAMP('{endTime}', 'YYYY-MM-DD HH24:MI:SS')
        '''
        sql_win = f'''SELECT
                        NVL(SUM(DECODE(
                            fcl.REASON, 'GM,DVCB,null,2', abs(CT_DAMT - BEFORE_DAMT)/10000,
                            'GM,DVCN,null,2', abs(CT_DAMT - BEFORE_DAMT)/10000, 0
                            )), 0)AS BET,
                        NVL(SUM(DECODE(
                            fcl.REASON, 'GM,PDXX,null,3', abs(CT_BAL-BEFOR_BAL)/10000,
                            'GM,BDRX,null,1', -abs(CT_BAL-BEFOR_BAL)/10000,
                            'OT,RBAP,null,3', abs(CT_BAL-BEFOR_BAL)/10000, 0
                            )), 0) AS AWARD
                    FROM 
                        FUND_CHANGE_LOG fcl
                    WHERE
                        fcl.USER_ID = {self.account}
                        AND fcl.GMT_CREATED >= TO_TIMESTAMP('{startTime}', 'YYYY-MM-DD HH24:MI:SS') 
                        AND fcl.GMT_CREATED < TO_TIMESTAMP('{endTime}', 'YYYY-MM-DD HH24:MI:SS')
        '''
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql_withdraw)
            withdraw = cursor.fetchall()[0][0]

            cursor.execute(sql_charge)
            charge = cursor.fetchall()[0][0]

            cursor.execute(sql_win)
            rows = cursor.fetchall()[0]
            win = rows[1] - rows[0]
        conn.close()
        
        return {
            'result': True if withdraw >= charge*ratio and win > limit_amount else False,
            'withdraw': withdraw,
            'charge': charge,
            'ratio': ratio,
            'win': win,
            'limit_amount': limit_amount,
            'startTime': startTime,
            'endTime': endTime
        }
    
    # Rule14: 中投比：中奖金额/投注金额 >= X 倍，且盈利金额 > Y 元
    def ratioOfBA(self) -> dict:
        ratio = float(self.config['WIN_BET_RATIO']['times'])
        limit_amount = float(self.config['WIN_BET_RATIO']['amount'])
        
        startTime = self.defaultTime.strftime('%Y-%m-%d %H:%M:%S')
        endTime = self.end_time.strftime('%Y-%m-%d %H:%M:%S')

        sql_win = f'''SELECT
                        NVL(SUM(DECODE(
                            fcl.REASON, 'GM,DVCB,null,2', abs(CT_DAMT - BEFORE_DAMT)/10000,
                            'GM,DVCN,null,2', abs(CT_DAMT - BEFORE_DAMT)/10000, 0
                            )), 0)AS BET,
                        NVL(SUM(DECODE(
                            fcl.REASON, 'GM,PDXX,null,3', abs(CT_BAL-BEFOR_BAL)/10000,
                            'GM,BDRX,null,1', -abs(CT_BAL-BEFOR_BAL)/10000,
                            'OT,RBAP,null,3', abs(CT_BAL-BEFOR_BAL)/10000, 0
                            )), 0) AS AWARD
                    FROM 
                        FUND_CHANGE_LOG fcl
                    WHERE
                        fcl.USER_ID = {self.account}
                        AND fcl.GMT_CREATED >= TO_TIMESTAMP('{startTime}', 'YYYY-MM-DD HH24:MI:SS') 
                        AND fcl.GMT_CREATED < TO_TIMESTAMP('{endTime}', 'YYYY-MM-DD HH24:MI:SS')
        '''
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql_win)
            rows = cursor.fetchall()[0]
            bet = rows[0]
            award = rows[1]
            win = award - bet
        conn.close()
        
        return {
            'result': True if award >= bet*ratio and win > limit_amount else False,
            'bet': bet,
            'award': award,
            'ratio':ratio,
            'win': win,
            'limit_amount': limit_amount,
            'startTime': startTime,
            'endTime': endTime
        }


    # Rule15: 投注包号 X% 以上
    def ratioOfNum(self):
        ratio = float(self.config['MOST_COMBINATION']['percentage'])/100

        startTime = self.claen_point.strftime('%Y-%m-%d %H:%M:%S')
        endTime = self.end_time.strftime('%Y-%m-%d %H:%M:%S')

        sql = f'''SELECT
                    gs.LOTTERYID, gs.ISSUE_CODE, gs.BET_TYPE_CODE, SUM(TOTBETS),
                    (SELECT LOTTERY_NAME FROM GAME_SERIES WHERE LOTTERYID = gs.LOTTERYID),
                    (SELECT 
                        GROUP_CODE_TITLE||SET_CODE_TITLE||METHOD_CODE_TITLE 
                    FROM 
                        GAME_BETTYPE_STATUS gbs 
                    WHERE 
                        gbs.BET_TYPE_CODE = gs.BET_TYPE_CODE AND ROWNUM = 1)
                FROM 
                    GAME_SLIP gs 
                WHERE 
                    gs.LOTTERYID||gs.ISSUE_CODE||gs.BET_TYPE_CODE IN
                    (SELECT 
                        gs.LOTTERYID||gs.ISSUE_CODE||gs.BET_TYPE_CODE
                    FROM 
                        GAME_SLIP gs 
                    WHERE 
                        gs.USERID  = {self.account}
                        AND gs.STATUS = 2
                        AND gs.CREATE_TIME >= TO_TIMESTAMP('{startTime}', 'YYYY-MM-DD HH24:MI:SS')
                        AND gs.CREATE_TIME < TO_TIMESTAMP('{endTime}', 'YYYY-MM-DD HH24:MI:SS')
                    GROUP BY 
                        gs.LOTTERYID, gs.ISSUE_CODE, gs.BET_TYPE_CODE)
                GROUP BY
                    gs.LOTTERYID, gs.ISSUE_CODE, gs.BET_TYPE_CODE
        '''
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
        conn.close()

        betNumsConfig = BetNumsConfig()
        trigger = []
        if rows:
            for slip in rows:
                lotteryId, issueCode, betTypeCode, totBets, lotteryName, betTypeName = slip
                betConent = self.getExceptBet(lotteryId, issueCode, betTypeCode)
                if betTypeCode in betNumsConfig.exception:
                    pass
                elif betTypeCode in betNumsConfig.nums11:
                    bet_ratio = self.checkNums11(betConent)
                    if bet_ratio > ratio:
                        trigger.append([lotteryName, issueCode, betTypeName, bet_ratio])
                elif betTypeCode in betNumsConfig.nums10:
                    bet_ratio = self.checkNums10(betConent)
                    if bet_ratio > ratio:
                        trigger.append([lotteryName, issueCode, betTypeName, bet_ratio])
                elif betTypeCode in betNumsConfig.nums4:
                    bet_ratio = self.checkNums4(betConent)
                    if bet_ratio > ratio:
                        trigger.append([lotteryName, issueCode, betTypeName, bet_ratio])
                elif betTypeCode in betNumsConfig.nums2:
                    bet_ratio = self.checkNums2(betConent)
                    if bet_ratio > ratio:
                        trigger.append([lotteryName, issueCode, betTypeName, bet_ratio])
                elif betTypeCode in betNumsConfig.shuangmian:
                    bet_ratio = self.checkShuangmian10(betConent)
                    if bet_ratio > ratio:
                        trigger.append([lotteryName, issueCode, betTypeName, bet_ratio])
                else:
                    limitBet = betNumsConfig.betNumsConfig[betTypeCode]
                    if totBets > limitBet*ratio:
                        trigger.append([lotteryName, issueCode, betTypeName, totBets, limitBet])
                        
        
        return {
            'result': True if trigger else False,
            'trigger': trigger,
            'ratio': ratio,
            'startTime': startTime,
            'endTime': endTime
        }

    def getExceptBet(self, lotteryId: int, issueCode: int, betTypeCode: str) -> list:
        sql = f'''SELECT 
                    DISTINCT(gs.BET_DETAIL)
                FROM 
                    GAME_SLIP gs
                WHERE 
                    gs.USERID  = {self.account}
                    AND gs.LOTTERYID = {lotteryId}
                    AND gs.ISSUE_CODE = {issueCode}
                    AND gs.BET_TYPE_CODE = '{betTypeCode}'
        '''
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql)
            betContent = cursor.fetchall()
        conn.close()
        return [d[0] for d in betContent]
    
    def checkNums11(self, betContent: list) -> float:        
        check = [set() for _ in range(5)]

        for content in betContent:
            slip = content.split(',')
            for i in range(len(slip)):
                nums = slip[i]
                for n in nums:
                    if n != '-' and n != ' ':
                        check[i].add(n)

        return round(max([len(d) for d in check])/11, 6)
    
    def checkNums10(self, betContent):
        check = [set() for _ in range(5)]

        for content in betContent:
            slip = content.split(',')
            for i in range(len(slip)):
                nums = slip[i]
                for n in nums:
                    if n != '-' and n != ' ':
                        check[i].add(n)
        
        return round(max([len(d) for d in check])/10, 6)
    
    def checkNums4(self, betContent):
        check = {}

        for content in betContent:
            pre_key = content[:-1]
            val = content[-1]
            sub_key = '大小' if val in '大小' else '单双'

            key = pre_key+sub_key
            if key not in check:
                check[key] = set(val)
            else:
                check[key].add(val)
        
        for v in check.values():
            cur = len(v)
            if cur == 2:
                return 1
        return 0.5

    
    def checkNums2(self, betContent):
        check = {}

        for content in betContent:
            key = content[:-1]
            val = content[-1]
            if key not in check:
                check[key] = set(val)
            else:
                check[key].add(val)
        
        for v in check.values():
            cur = len(v)
            if cur == 2:
                return 1
        return 0.5
    
    def checkShuangmian10(self, betContent: list) -> float:
        check = {}

        for content in betContent:
            key = content[:-1]
            val = content[-1]

            if key not in check:
                check[key] = set(val)
            else:
                check[key].add(val)
        
        return round(max([len(d) for d in check.values()])/10, 6)
            
    # Rule16: 三个月未登录用户
    def silentUser_prev(self): # 登入時間(原版)
        startTime = (self.end_time-relativedelta(days=180)).strftime('%Y-%m-%d %H:%M:%S')
        endTime = self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        sql_userLogin = f'''SELECT 
                            ull.LOGIN_DATE
                        FROM 
                            USER_LOGIN_LOG ull
                        WHERE 
                            ull.USER_ID = {self.account}
                            AND ull.LOGIN_DATE >= TO_TIMESTAMP('{startTime}', 'YYYY-MM-DD HH24:MI:SS')
                            AND ull.LOGIN_DATE < TO_TIMESTAMP('{endTime}', 'YYYY-MM-DD HH24:MI:SS')
                        ORDER BY
                            ull.LOGIN_DATE DESC
        '''

        sql_register = f'''SELECT 
                            REGISTER_DATE 
                        FROM 
                            USER_CUSTOMER
                        WHERE
                            ID = {self.account}
        '''
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql_userLogin)
            rows = cursor.fetchall()

            cursor.execute(sql_register)
            registerDate = cursor.fetchall()[0][0]
        conn.close()
        
        
        baseDate = (self.end_time-relativedelta(days=180)) if registerDate < (self.end_time-relativedelta(months=6)) else registerDate
        res = False
        period = []

        if rows:
            rows.append((baseDate,))
            for i in range(1, len(rows)):
                if rows[i][0]+relativedelta(days=90) < rows[i-1][0]:
                    res = True
                    period.append(rows[i][0].strftime('%Y-%m-%d %H:%M:%S'))
                    period.append(rows[i-1][0].strftime('%Y-%m-%d %H:%M:%S'))
                    break
        
        return {
            'result': res,
            'period': period,
            'startTime': startTime,
            'endTime':endTime
        }

    def silentUser(self):
        startTime = (self.end_time-relativedelta(days=180)).strftime('%Y-%m-%d %H:%M:%S')
        endTime = self.end_time.strftime('%Y-%m-%d %H:%M:%S')

        sql_third = f'''SELECT 
	                ctbr.SEQ_ID
                FROM 
	                COLLECT_THIRDLY_BET_RECORD ctbr 
                WHERE
	                ctbr.USER_ID = {self.account} 
                    AND ctbr.THIRDLY_BET_TIME >= TO_TIMESTAMP('{startTime}', 'YYYY-MM-DD HH24:MI:SS')
                    AND ctbr.THIRDLY_BET_TIME < TO_TIMESTAMP('{endTime}', 'YYYY-MM-DD HH24:MI:SS')
        '''

        sql_bet = f'''SELECT 
                        ID
                    FROM 
                        GAME_ORDER go2 
                    WHERE 
                        go2.USERID  = {self.account}
                        AND go2.ORDER_TIME >= TO_TIMESTAMP('{startTime}', 'YYYY-MM-DD HH24:MI:SS')
                        AND go2.ORDER_TIME < TO_TIMESTAMP('{endTime}', 'YYYY-MM-DD HH24:MI:SS')
        '''

        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql_third)
            third = cursor.fetchall()
            
            cursor.execute(sql_bet)
            bet = cursor.fetchall()
        conn.close()

        return {
            'result': True if not third and not bet else False,
            'third': True if third else False,
            'bet': True if bet else False,
            'startTime': startTime,
            'endTime':endTime
        }

    def _getHistoryConfigValue(self, rule: int, configType: int) -> Union[int, str]:
        '''
        parm: rule 1-16
        parm: type 0 switch/ 1 value
        '''

        applyTime = self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        typeDict = {0: '开关', 1: '内容'}
        sql = f'''SELECT 
                    AFTER_VALUE
                FROM 
                    FUND_WITHDRAW_CHECK_CONFIG_LOG fwccl
                WHERE
                    fwccl.NAME = '规则{rule}{typeDict[configType]}' AND fwccl.AUDIT_TIME < TO_TIMESTAMP('{applyTime}', 'YYYY-MM-DD HH24:MI:SS')
                ORDER BY
                    AUDIT_TIME DESC
        '''
        conn = self.oracle(self.env)
        with conn.cursor() as cursor:
            cursor.execute(sql)
            config = cursor.fetchall()    
        conn.close()

        if not config:
            return None
        return config[0][0]
    
    def getHistoryConfig(self) -> dict:
        config = {
            "PLAYED_THIRD":{
                "enable": int(self._getHistoryConfigValue(1, 0))
                },
            "BET_REQUIRED":{
                "enable": int(self._getHistoryConfigValue(2, 0)),
                "times": float(self._getHistoryConfigValue(2, 1)[12:-1])
                },
            "BLACK_LIST":{
                "enable": int(self._getHistoryConfigValue(3, 0))
                },
            "JOINED_ACTIVITY":{
                "enable": int(self._getHistoryConfigValue(4, 0))
                },
            "RISK_TAGGED":{
                "enable": int(self._getHistoryConfigValue(5, 0))
                },
            "LARGE_AMOUNT":{
                "enable": int(self._getHistoryConfigValue(6, 0)),
                "limit": float(self._getHistoryConfigValue(6, 1)[11:-1])
                },
            "FIRST_TIME_USDT":{
                "enable": int(self._getHistoryConfigValue(7, 0)),
                "limit": float(self._getHistoryConfigValue(7, 1)[15:-4])
                },
            "CARD_INFO_CHANGED":{
                "enable": int(self._getHistoryConfigValue(8, 0)),
                "days": int(self._getHistoryConfigValue(8, 1)[:-14])
                },
            "NO_RECHARGE":{
                "enable": int(self._getHistoryConfigValue(9, 0)),
                "limit": float(self._getHistoryConfigValue(9, 1)[15:-4])
                },
            "SHOW_HAND":{
                "enable": int(self._getHistoryConfigValue(10, 0)),
                "count": int(self._getHistoryConfigValue(10, 1).split(' ')[2]),
                },
            "WITHDRAW_COUNT_LIMIT":{
                "enable": int(self._getHistoryConfigValue(11, 0)),
                "count": int(self._getHistoryConfigValue(11, 1).split(' ')[1]),
                "amount": float(self._getHistoryConfigValue(11, 1).split(' ')[3])
                },
            "WITHDRAW_AMOUNT_LIMIT":{
                "enable": int(self._getHistoryConfigValue(12, 0)),
                "days": int(self._getHistoryConfigValue(12, 1).split(' ')[0]),
                "amount": float(self._getHistoryConfigValue(12, 1).split(' ')[2])
                },
            "WITHDRAW_RECHARGE_RATIO":{
                "enable": int(self._getHistoryConfigValue(13, 0)),
                "times": float(self._getHistoryConfigValue(13, 1).split(' ')[2]),
                "amount": float(self._getHistoryConfigValue(13, 1).split(' ')[5])
                },
            "WIN_BET_RATIO":{
                "enable": int(self._getHistoryConfigValue(14, 0)),
                "times": float(self._getHistoryConfigValue(14, 1).split(' ')[2]),
                "amount": float(self._getHistoryConfigValue(14, 1).split(' ')[5])
                },
            "MOST_COMBINATION":{
                "enable": int(self._getHistoryConfigValue(15, 0)),
                "percentage": float(self._getHistoryConfigValue(15, 1).split(' ')[1][:-1])
                },
            "INACTIVE_USER":{
                "enable": int(self._getHistoryConfigValue(16, 0))
                }
        }

        return config

    def ruleCheck(self) -> dict:
        switch = []
        for k, v in self.config.items():
            if 'enable' in v:
                switch_status = 'On' if v['enable'] == 1 else 'Off'
                switch.append(switch_status)
        res = {}
        res[1] = (self.isThirdly())
        res[2] = (self.isFlow())
        res[3] = (self.isBlackList())
        res[4] = (self.isActivityReward())
        res[5] = (self.isRiskTag())
        res[6] = (self.withdrawLimit())
        res[7] = (self.firstUSDT())
        res[8] = (self.isChangeInfo())
        res[9] = (self.isManualCharge())
        res[10] = (self.newUserAndShowHand())
        res[11] = (self.dailyWithdrawLimit())
        res[12] = (self.periodWithdrawLimit())
        res[13] = (self.ratioOfWD())
        res[14] = (self.ratioOfBA())
        res[15] = (self.ratioOfNum())
        res[16] = (self.silentUser())
        res['switch'] = switch
        return res


if __name__ == '__main__':
    a = AutoWithdrawVerify('FDCWTF5KLW1UEAMX4XNXz0QUU')
    print(a._getRedisValue('WITHDRAW_AMOUNT_MANUAL_PASS:1382045'))

