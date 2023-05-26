import pymysql, redis

class DBconnection:
    def __init__(self, env: int) -> None:
        self.env = env

    def ubitConn(self):
        config = {
            0: ('10.13.22.164', 'ubit', 'rPsSSNqeUTpYYxY5', 'ubit'),
            1: ('54.150.197.171', 'rd_user', 'Sxae4Z93BDfcDUDR', 'ubit')
        }
        host, user, passwd, db = config[self.env]

        conn = pymysql.connect(
            host=host,
            user=user,
            passwd=passwd,
            db=db)
        return conn

    def ubitRedisConn(self):
        # 目前僅dev能連線至redis
        pool = redis.ConnectionPool(host='10.13.22.154')
        conn = redis.Redis(connection_pool=pool)
        return conn

class DBSearch(DBconnection):
    def __init__(self, env: int) -> None:
        super().__init__(env)
    
    def getUserInfo(self, userId: int):
        conn = self.ubitConn()
        try:
            with conn.cursor() as cursor:
                sql = f"""select area_code, mobile from user_info where id = {userId}
                """
                cursor.execute(sql)
                rows = cursor.fetchone()

            return {'area_code': rows[0], 'mobile': rows[1]} if rows else None
        finally:
            conn.close()
    
    def isUserExisted(self, area_code: int, mobile: int) -> bool:
        conn = self.ubitConn()
        try:
            with conn.cursor() as cursor:
                sql = f"""select id from user_info where area_code = {area_code} and mobile = '{mobile}'
                """
                cursor.execute(sql)
                rows = cursor.fetchall()
            return True if rows else False
        finally:
            conn.close()
    
    def getUserId(self, area_code: int, mobile: int):
        conn = self.ubitConn()
        try:
            with conn.cursor() as cursor:
                sql = f"""select id from user_info where area_code = {area_code} and mobile = '{mobile}'
                """
                cursor.execute(sql)
                rows = cursor.fetchone()
            return rows[0] if rows else None
        finally:
            conn.close()
    
    def getMunualAddOrders(self, note: str='Ubit trunk manual apply: Add.') -> list:
        conn = self.ubitConn()
        try:
            with conn.cursor() as cursor:
                sql = f"""select id from manual_deposit_audit where operate_note = '{note}' and status = 0
                """
                cursor.execute(sql)
                rows = cursor.fetchall()
                
                res = []
                if rows:
                    for row in rows:
                        res.append(row[0])

            return res if rows else None
        finally:
            conn.close()
    
    def getGoogleAuthSecretKey(self, user_id: int) -> str:
        conn = self.ubitConn()
        try:
            with conn.cursor() as cursor:
                sql = f"""select google_code from user_info where id = {user_id} 
                """
                cursor.execute(sql)
                rows = cursor.fetchone()

            return rows[0] if rows else None
        finally:
            conn.close()
    
    def getUserVirtualAdress(self, user_id: int, coin_id: int, chain_id: int) -> str:
        conn = self.ubitConn()
        try:
            with conn.cursor() as cursor:
                sql = f"""select 
                            address 
                        from 
                            user_virtual_address 
                        where 
                            user_id = {user_id} and coin_id = {coin_id} and chain_id = {chain_id}
                """
                cursor.execute(sql)
                rows = cursor.fetchone()

            return rows[0] if rows else None
        finally:
            conn.close()
    
    def getUserPaymentId(self, bind_card_type: int, user_id: int) -> int:
        conn = self.ubitConn()
        try:
            with conn.cursor() as cursor:
                sql = f"""select id from payment_method_info where bindcard_type = {bind_card_type} and user_id = {user_id}
                """
                cursor.execute(sql)
                rows = cursor.fetchone()

            return rows[0] if rows else None
        finally:
            conn.close()

    def getApplyReleaseOrderId(self, user_id: int):
        conn = self.ubitConn()
        try:
            with conn.cursor() as cursor:
                sql = f"""select id from c2c_qualification_apply where user_id = {user_id} and status = 1
                """
                cursor.execute(sql)
                rows = cursor.fetchone()

            return rows[0] if rows else None
        finally:
            conn.close()
    
    def getConfig(self, config_name: str) -> tuple:
        '''
        return: tuple(config_id, config_value, config_desc)
        '''
        conn = self.ubitConn()
        try:
            with conn.cursor() as cursor:
                sql = f"""select id, config_value, config_desc from config where config_key = '{config_name}'
                """
                cursor.execute(sql)
                rows = cursor.fetchone()
            return rows if rows else None
        finally:
            conn.close()

if __name__ == '__main__':
    # import base64

    # with open("1.jpg", "rb") as image_file:
    #     encoded_string = base64.b64encode(image_file.read())

    # print(encoded_string)
    print(DBSearch(0).getMunualAddOrders())







