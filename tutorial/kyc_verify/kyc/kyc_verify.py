from ubit_test.ubit_tests.ubit_connection import DBconnection

class KYCverify:
    def __init__(self, env: int, order_id: str) -> None:
        self.db = DBconnection(env)
        self.order_id = order_id
        self.user_id = self.getUserId()


    def _search(self, sql: str):
        conn = self.db.ubitConn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                return rows if rows else None
        finally:
            conn.close()

    def getUserId(self) -> int:
        sql = f'''select user_id from trade_buy_order_info where order_id = '{self.order_id}'
        '''
        data = self._search(sql)
        if data:
            return data[0][0]
        else:
            return None
    
    def getUserVerifySetting(self) -> dict:
        '''
        後台用戶標籤設定
        '''
        ...
    
    def getVerifySetting(self) -> dict:
        '''
        後台參數設定
        '''
        ...

    # 1. 单笔买币交易金额
    def tradeLimit(self) -> dict:
        sql = f'''select order_legal_amount from trade_buy_order_info where order_id = '{self.order_id}'
        '''
        data = self._search(sql)
        amount = None
        if data:
            amount = data[0][0]
        return {
            'result': True,
            'amount': float(amount)
        }
    
    # 2. 当日成功买币累积交易笔数
    def tradeDailyCount(self) -> dict:
        sql = f'''select count(id) from trade_buy_order_info where user_id = {self.user_id} and create_date >= CURDATE()
        '''
        data = self._search(sql)
        count = None
        if data:
            count = data[0][0]

        return {
            'result': True,
            'count': count
        }
    
    # 3. 当日成功买币累积交易金额
    def tradeDailyAmount(self) -> dict:
        sql = f'''select sum(order_legal_amount) from trade_buy_order_info where user_id = {self.user_id} and create_date >= CURDATE()
        '''
        data = self._search(sql)
        amount = None
        if data:
            amount = data[0][0]
        return {
            'result': True,
            'amount': float(amount)
        }
    
    # 4. 累积成功买币交易15万人民币(但历史未与商户API转)
    def tradeAmount(self) -> dict:
        sql = f'''select sum(order_legal_amount) from trade_buy_order_info where user_id = {self.user_id}
        '''
        data = self._search(sql)
        amount = None
        if data:
            amount = data[0][0]
        return {
            'result': True,
            'amount': float(amount)
        }
    
    # 5.  累积成功买币交易笔数150笔(但历史未与商户API转)
    def tradeCount(self) -> dict:
        sql = f'''select count(id) from trade_buy_order_info where user_id = {self.user_id}
        '''
        data = self._search(sql)
        count = None
        if data:
            count = data[0][0]

        return {
            'result': True,
            'count': count
        }

    def runVerify(self) -> dict:
        '''
        1. tradeLimit           单笔买币交易金额
        2. tradeDailyCount      当日成功买币累积交易笔数
        3. tradeDailyAmount     当日成功买币累积交易金额
        4. tradeAmount          累积成功买币交易15万人民币(但历史未与商户API转)
        5. tradeCount           累积成功买币交易笔数150笔(但历史未与商户API转)
        '''
        res = []
    

if __name__ == '__main__':
    ver = KYCverify(1, 'kjdd202305224sL5cAbv1AitRG')
    print(ver.user_id)
    r = ver.tradeLimit()
    print(r)
    r = ver.tradeDailyCount()
    print(r)
    r = ver.tradeDailyAmount()
    print(r)
    r = ver.tradeAmount()
    print(r)
    r = ver.tradeCount()
    print(r)
    
