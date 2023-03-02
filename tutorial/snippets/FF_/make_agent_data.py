import cx_Oracle
from time import time, sleep
from datetime import datetime



class AgentCenter:
    def __init__(self) -> None:
        
        # 彩票	团队彩票销量	
        # 投注扣款（GM,DVCB,null,2）+追号投注扣款（GM,DVCN,null,2）
        self.bet = ['GM,DVCB,null,2', 'GM,DVCN,null,2']

        # 三方	团队三方有效销量	所有三方总有效投注
        third_bet = '另開func'

        # 彩票	团队彩票中奖金额	
        # 奖金派送（GM,PDXX,null,3）
        # -撤销派奖（GM,BDRX,null,1）
        # +【加币-补发奖金（OT,RBAP,null,3）】
        self.award = ['GM,PDXX,null,3', 'GM,BDRX,null,1', 'OT,RBAP,null,3']

        # 三方	团队三方中奖金额	所有三方总派送奖金
        self.third_award = '另開func'

        # 彩票	团队彩票总活动礼金（含VIP奖励和红包）	
        # 活动：
        # 活动礼金-自动（PM,PGXX,null,4）
        # +活动礼金-代活动系统派发（PM,PGXX,null,5）
        # +加币-活动礼金（PM,PGXX,null,3）
        # +平台奖励（PM,IPXX,null,3）
        # +首投返利（GM,FBRX,null,1）
        # - 扣币-活动减项（OT,ADBA,null,3）
        # +新VIP体系-晋级礼金(PM,SVUR,null,1）
        # +积分商城加币（PM,PMXX,null,3）
        # +红包收入（HB,AHBC,null,1 ）
        self.activity = [
            'PM,PGXX,null,4', 'PM,PGXX,null,5', 'PM,PGXX,null,3', 'PM,IPXX,null,3', 'GM,FBRX,null,1',
            'OT,ADBA,null,3', 'PM,SVUR,null,1', 'PM,PMXX,null,3', 'HB,AHBC,null,1'
        ]

        # 三方	团队三方总活动礼金（不含VIP奖励）	三方活动礼金（PM,TAAM,null,3）
        self.third_activity = ['PM,TAAM,null,3']

        # 充值	全部	团队总充值成功金额	
        # 自动充值（FD,ADAL,null,3）
        # +加币-人工充值（FD,MDAX,null,5）
        # +加币-人工充值（OT,AAXX,null,3）
        # -充值手续费-成功（FD,ADAC,null,1）
        # +充值手续费-返还（PM,RBRC,null,1）
        self.charge = ['FD,ADAL,null,3', 'FD,MDAX,null,5', 'OT,AAXX,null,3', 'FD,ADAC,null,1', 'PM,RBRC,null,1']

        # 提现	全部	团队总提现成功金额	
        # 提现（FD,CWTS,null,5）
        # +部份提现成功(FD,CWTS,null,6)
        # +人工提现（FD,CWCS,null,4）
        self.withdraw = ['FD,CWTS,null,5', 'FD,CWTS,null,6', 'FD,CWCS,null,4']

        # 彩票返点	全部/彩票	团队的彩票返点(投注+上级所得)	
        # 本人投注返点（GM,RSXX,null,1）
        # +上级投注返点（GM,RHAX,null,2）
        self.rebet = ['GM,RSXX,null,1', 'GM,RHAX,null,2']

        # 彩票日工资	全部/彩票	团队所有彩票日工资总额	
        # 彩票日工资+彩票VIP返水

        # 彩票日工资=转入日工资（TF,DLSY,null,1）+日工资派发（PM,AADS,null,3）-扣币日工资减项（OT,WDBA,null,3）-下级日工资（TF,DABR,null,1）
        # 彩票VIP返水=彩票返水（PM,RHYB,null,6）+星級返水 (人工加幣) (PM,RHYB,null,7）-彩票返水扣币(OT,SVWD,null,3)
        self.daily_salary = ['TF,DLSY,null,1', 'PM,AADS,null,3', 'OT,WDBA,null,3', 'TF,DABR,null,1']
        self.vip_rebet = ['PM,RHYB,null,6', 'PM,RHYB,null,7', 'OT,SVWD,null,3']

        # 三方返水	全部/三方	团队总三方日返水（含三方vip返水）	
        # 三方返水+三方VIP返水

        # 1）三方返水=三方返水（GM,SFFS,null,1）+转入返水（TF,TADS,null,1）-扣币-返水减项（OT,TDBA,null,3）-下级返水（TF,DTWR,null,1）
        # 2）VIP返水=体育返水（PM,RHYB,null,3）+电竞返水（PM,RHYB,null,4）+真人返水（PM,RHYB,null,5）+棋牌返水（PM,RHYB,null,8）+电子返水（PM,RHYB,null,9）-三方返水扣币(OT,SVWF,null,3)+人工三方返水（PM,TSVA,null,1）
        self.third_rebet = ['GM,SFFS,null,1', 'TF,TADS,null,1', 'OT,TDBA,null,3', 'TF,DTWR,null,1']
        self.third_vip_rebet = ['PM,RHYB,null,3', 'PM,RHYB,null,4', 'PM,RHYB,null,5', 'PM,RHYB,null,8', 'PM,RHYB,null,9', 'OT,SVWF,null,3', 'PM,TSVA,null,1']

        # 三方平台费	全部/三方	团队总三方扣除费用	（各三方月累计GP1*平台费比例）相加
        self.third = '另開func'

        # 彩票	团队彩票GP1.5	
        # 中奖+活动+日工资（含VIP彩票返水）+返点-投注

        # 三方	团队三方GP1.5	中奖+三方活动+三方返水+三方平台费-销量
        # 注：三方平台费在计算GP1.5时，如果为负数则最低为0

        self.deduct = [
            'GM,BDRX,null,1',
            'OT,ADBA,null,3', 'HB,CRHB,null,3', 'HB,CRHB,null,4', 'HB,DHBS,null,2',
            'FD,ADAC,null,1',
            'FD,CWTS,null,5', 'FD,CWTS,null,6', 'FD,CWCS,null,4',
            'OT,WDBA,null,3', 'TF,DABR,null,1',
            'OT,SVWD,null,3',
            'OT,TDBA,null,3', 'TF,DTWR,null,1',
            'OT,SVWF,null,3'
        ]


        self.reason_comparision_table = {
            'GM,DVCB,null,2': '投注扣款', 'GM,DVCN,null,2': '追号投注扣款',
            'GM,PDXX,null,3': '奖金派送', 'GM,BDRX,null,1': '撤销派奖', 'OT,RBAP,null,3': '加币-补发奖金',
            'PM,PGXX,null,4': '活动礼金-自动', 'PM,PGXX,null,5': '活动礼金-代活动系统派发', 'PM,PGXX,null,3': '加币-活动礼金', 'PM,IPXX,null,3': '平台奖励',
            'GM,FBRX,null,1': '首投返利', 'OT,ADBA,null,3': '扣币-活动减项', 'PM,SVUR,null,1': '新VIP体系-晋级礼金', 'PM,PMXX,null,3': '积分商城加币', 
            'HB,CRHB,null,3': '撤单红包返还', 'HB,CRHB,null,4': '撤单红包返还', 'HB,DHBS,null,2': '红包抵扣', 'HB,AHBC,null,1': '红包收入',
            'PM,TAAM,null,3': '三方活动礼金', 'FD,ADAL,null,3': '自动充值', 'OT,AAXX,null,3': '加币-人工充值', 'FD,MDAX,null,5': '加币-人工充值', 
            'FD,ADAC,null,1': '充值手续费-成功', 'PM,RBRC,null,1': '充值手续费-返还',
            'FD,CWTS,null,5': '提现', 'FD, CWTS,null,6': '部份提现成功', 'FD,CWCS,null,4': '人工提现',
            'GM,RSXX,null,1': '本人投注返点', 'GM,RHAX,null,2': '上级投注返点',
            'TF,DLSY,null,1': '转入日工资', 'PM,AADS,null,3': '日工资派发', 'OT,WDBA,null,3': '扣币日工资减项', 'TF,DABR,null,1': '下级日工资',
            'PM,RHYB,null,6': '彩票返水', 'PM,RHYB,null,7': '星級返水 (人工加幣)', 'OT,SVWD,null,3': '彩票返水扣币',
            'GM,SFFS,null,1': '三方返水', 'TF,TADS,null,1': '转入返水', 'OT,TDBA,null,3': '扣币-返水减项', 'TF,DTWR,null,1': '下级返水', 
            'PM,RHYB,null,3': '体育返水', 'PM,RHYB,null,4': '电竞返水', 'PM,RHYB,null,5': '真人返水', 'PM,RHYB,null,8': '棋牌返水', 'PM,RHYB,null,9': '电子返水', 
            'OT,SVWF,null,3': '三方返水扣币', 'PM,TSVA,null,1': '人工三方返水'
        }

    def oracle(self, env: int) -> object:
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

    def user_bal(self, env: int, user_id: int) -> list: 
        conn = self.oracle(env)
        with conn.cursor() as cursor:
            sql = f'''SELECT 
                        CT_BAL, CT_DAMT, CT_AVAIL_BAL, BEFORE_AVAIL_BAL 
                    FROM 
                        FUND_CHANGE_LOG 
                    WHERE 
                        USER_ID = {user_id} AND ROWNUM = 1 ORDER BY GMT_CREATED DESC
            '''
            cursor.execute(sql)
            rows = cursor.fetchall()
            if rows:
                row = rows[0]
            elif not rows:
                row = [0,0,0,0]
            bal_list = [int(data) for data in row] 
        conn.close()
        return bal_list

    def insertData(self, env: int, user_id: int, reason: str, value: float) -> None:
        conn = self.oracle(env)
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bal_data = self.user_bal(env, user_id)

        ct_bal = (bal_data[0] - value) if reason in self.deduct else (bal_data[0] + value)
        ct_damt = (bal_data[1] - value) if reason in self.deduct else (bal_data[1] + value)
        with conn.cursor() as cursor:
            sql = f'''INSERT INTO FUND_CHANGE_LOG fcl
                        (ID, USER_ID, BEFOR_BAL, BEFORE_DAMT, CT_BAL, CT_DAMT, REASON, FUND_ID, SN, GMT_CREATED, ISACLUSER, ISVISIBLEBYFRONTUSER, CT_AVAIL_BAL, BEFORE_AVAIL_BAL)
                    VALUES (
                    SEQ_FUND_CHANGE_LOG_ID.Nextval,
                    {user_id},
                    {bal_data[0]},
                    {bal_data[1]},
                    {ct_bal},
                    {ct_damt},
                    '{reason}',
                    777,
                    '{'HM_peter_'+datetime.now().strftime("%m%d%H%M%S")}',
                    TO_DATE('{cur_time}','yyyy-MM-dd HH24:mi:ss'),
                    1,
                    1,
                    {bal_data[2]},
                    {bal_data[3]}
                    )
            '''
            # print(sql)
            cursor.execute(sql)
        conn.commit()
        conn.close()
        print(f'{user_id} Reason: {reason} Value: {value} GMT: {cur_time}')

    def verifyAgentData(self, env: int, user: str, start: str, end: str, mode: int) -> dict:
        '''
        param: mode 0 is team data, 1 is personal data
        start/end formate: '2022-06-02 00:00:00'
        '''
        if mode == 0:
            key = f'''(SELECT o_id FROM USER_CUSTOMER_FOR_REPORT_TEMP t where u_id=(SELECT ID FROM USER_CUSTOMER WHERE ACCOUNT='{user}'))'''
        elif mode == 1:
            key = f'''(SELECT ID FROM USER_CUSTOMER WHERE ACCOUNT='{user}')'''
        else:
            return 'wrong mode'

        def fundChangeCal():
            conn = self.oracle(env)
            with conn.cursor() as cursor:
                sql = f'''SELECT
                    NVL(SUM(DECODE(
                        fcl.REASON, 'GM,DVCB,null,2', abs(CT_DAMT - BEFORE_DAMT)/10000,
                        'GM,DVCN,null,2', abs(CT_DAMT - BEFORE_DAMT)/10000, 0
                        )), 0)AS BET,
                    NVL(SUM(DECODE(
                        fcl.REASON, 'GM,PDXX,null,3', abs(CT_BAL-BEFOR_BAL)/10000,
                        'GM,BDRX,null,1', -abs(CT_BAL-BEFOR_BAL)/10000,
                        'OT,RBAP,null,3', abs(CT_BAL-BEFOR_BAL)/10000, 0
                        )), 0) AS AWARD,
                    NVL(SUM(DECODE(
                        fcl.REASON, 'PM,PGXX,null,4', abs(CT_BAL-BEFOR_BAL)/10000,
                        'PM,PGXX,null,5', abs(CT_BAL-BEFOR_BAL)/10000,
                        'PM,PGXX,null,3', abs(CT_BAL-BEFOR_BAL)/10000,
                        'PM,IPXX,null,3', abs(CT_BAL-BEFOR_BAL)/10000,
                        'GM,FBRX,null,1', abs(CT_BAL-BEFOR_BAL)/10000,
                        'OT,ADBA,null,3', -abs(CT_BAL-BEFOR_BAL)/10000,
                        'PM,SVUR,null,1', abs(CT_BAL-BEFOR_BAL)/10000,
                        'PM,PMXX,null,3', abs(CT_BAL-BEFOR_BAL)/10000,
                        'HB,AHBC,null,1', abs(CT_BAL-BEFOR_BAL)/10000, 0
                        )), 0) AS ACTIVITY,
                    NVL(SUM(DECODE(
                        fcl.REASON, 'PM,TAAM,null,3', abs(CT_BAL-BEFOR_BAL)/10000, 0
                        )), 0) AS THIRD_ACTIVITY,
                    NVL(SUM(DECODE(
                        fcl.REASON, 'FD,ADAL,null,3', abs(CT_BAL-BEFOR_BAL)/10000,
                        'FD,MDAX,null,5', abs(CT_BAL-BEFOR_BAL)/10000,
                        'OT,AAXX,null,3', abs(CT_BAL-BEFOR_BAL)/10000,
                        'FD,ADAC,null,1', -abs(CT_BAL-BEFOR_BAL)/10000,
                        'PM,RBRC,null,1', abs(CT_BAL-BEFOR_BAL)/10000, 0
                        )), 0) AS CHARGE,
                    NVL(SUM(DECODE(
                        fcl.REASON, 'FD,CWTS,null,5', abs(CT_DAMT - BEFORE_DAMT)/10000,
                        'FD,CWTS,null,6', abs(CT_DAMT - BEFORE_DAMT)/10000,
                        'FD,CWCS,null,4', abs(CT_DAMT - BEFORE_DAMT)/10000, 0
                        )), 0) AS WITHDRAW,
                    NVL(SUM(DECODE(
                        fcl.REASON, 'GM,RSXX,null,1', abs(CT_BAL-BEFOR_BAL)/10000,
                        'GM,RHAX,null,2', abs(CT_BAL-BEFOR_BAL)/10000, 0
                        )), 0) AS REBET,
                    NVL(SUM(DECODE(
                        fcl.REASON, 'TF,DLSY,null,1', abs(CT_BAL-BEFOR_BAL)/10000,
                        'PM,AADS,null,3', abs(CT_BAL-BEFOR_BAL)/10000,
                        'OT,WDBA,null,3', -abs(CT_BAL-BEFOR_BAL)/10000,
                        'TF,DABR,null,1', -abs(CT_BAL-BEFOR_BAL)/10000,
                        'PM,RHYB,null,6', abs(CT_BAL-BEFOR_BAL)/10000,
                        'PM,RHYB,null,7', abs(CT_BAL-BEFOR_BAL)/10000,
                        'OT,SVWD,null,3', -abs(CT_BAL-BEFOR_BAL)/10000, 0
                        )), 0) AS daily_salary,
                    NVL(SUM(DECODE(
                        fcl.REASON, 'GM,SFFS,null,1', abs(CT_BAL-BEFOR_BAL)/10000,
                        'TF,TADS,null,1', abs(CT_BAL-BEFOR_BAL)/10000,
                        'OT,TDBA,null,3', -abs(CT_BAL-BEFOR_BAL)/10000,
                        'TF,DTWR,null,1', -abs(CT_BAL-BEFOR_BAL)/10000,
                        'PM,RHYB,null,3', abs(CT_BAL-BEFOR_BAL)/10000,
                        'PM,RHYB,null,4', abs(CT_BAL-BEFOR_BAL)/10000,
                        'PM,RHYB,null,5', abs(CT_BAL-BEFOR_BAL)/10000,
                        'PM,RHYB,null,8', abs(CT_BAL-BEFOR_BAL)/10000,
                        'PM,RHYB,null,9', abs(CT_BAL-BEFOR_BAL)/10000,
                        'OT,SVWF,null,3', -abs(CT_BAL-BEFOR_BAL)/10000,
                        'PM,TSVA,null,1', abs(CT_BAL-BEFOR_BAL)/10000, 0
                        )), 0) AS third_rebet
                FROM 
                    FUND_CHANGE_LOG fcl 
                WHERE
                    fcl.USER_ID  IN {key}
                    AND fcl.GMT_CREATED BETWEEN TO_TIMESTAMP('{start}','yyyy-MM-dd HH24:mi:ss') AND TO_TIMESTAMP('{end}','yyyy-MM-dd HH24:mi:ss')
                '''

                cursor.execute(sql)
                rows = cursor.fetchall()[0]
                r_dict = {
                    'BET': rows[0],
                    'AWARD': rows[1],
                    'ACTIVITY': rows[2],
                    'THIRD_ACTIVITY': rows[3],
                    'CHARGE': rows[4],
                    'WITHDRAW': rows[5],
                    'REBET': rows[6],
                    'DAILY_SALARY': rows[7],
                    'THIRD_REBET': rows[8]
                    }
            conn.close()
            return r_dict
        
        def thirdCal():
            conn = self.oracle(env)
            with conn.cursor() as cursor:
                sql = f'''SELECT 
                        NVL(SUM(COST), 0),
                        NVL(SUM(PRIZE), 0)
                    FROM
                        THIRDLY_AGENT_CENTER tac
                    WHERE 
                        USER_ID  IN {key}
                        AND tac.CREATE_DATE BETWEEN TO_DATE('{start}','yyyy-MM-dd HH24:mi:ss') AND TO_DATE('{end}','yyyy-MM-dd HH24:mi:ss')
                '''
                cursor.execute(sql)
                rows = cursor.fetchall()[0]
                r_dict = {
                    'THIRD_BET': rows[0],
                    'THIRD_AWARD': rows[1]
                }
            conn.close()
            return r_dict

        def thirdPlat():
            start_year = int(start[0:3])
            end_year = int(end[0:3])
            start_month = int(start[6:7])+1 
            end_month = int(end[6:7])+1

            if start_month == 12:
                start_month = 1
                start_year += 1
            
            if end_month == 12:
                end_month = 1
                end_year += 1
            
            start_month = '0'+str(start_month) if start_month < 10 else str(start_month)
            end_month = '0'+str(end_month) if end_month < 10 else str(end_month)
            start_year = str(start_year)
            end_year = str(end_year)
            
            conn = self.oracle(env)
            with conn.cursor() as cursor:
                sql = f'''SELECT 
                        NVL(SUM((BET-WIN)*RATE), 0) 
                    FROM 
                        THIRDLY_COST tc 
                    WHERE 
                        tc.USER_ID  IN {key}
                        AND tc.CREATE_DATE BETWEEN TO_TIMESTAMP('{start_year}-{start_month}-01 00:00:00','yyyy-MM-dd HH24:mi:ss') AND TO_TIMESTAMP('{start_year}-{end_month}-01 00:00:00','yyyy-MM-dd HH24:mi:ss')
                '''
                cursor.execute(sql)
                r = cursor.fetchall()[0][0]
                return r

        fcl_result = fundChangeCal()
        third_reuslt = thirdCal()
        third_plat = thirdPlat()

        total = {
            'BET': third_reuslt['THIRD_BET']+fcl_result['BET'],
            'AWARD': fcl_result['AWARD']+third_reuslt['THIRD_AWARD'],
            'ACTIVITY': fcl_result['ACTIVITY']+fcl_result['THIRD_ACTIVITY'],
            'CHARGE': fcl_result['CHARGE'],
            'WITHDRAW': fcl_result['WITHDRAW'],
            'REBET': fcl_result['REBET'],
            'DAILY_SALARY': fcl_result['DAILY_SALARY'],
            'THIRD_REBET': fcl_result['THIRD_REBET'],
            'THIRD_PLAT': third_plat,
            'T_GP15': fcl_result['AWARD'] + fcl_result['ACTIVITY'] + fcl_result['DAILY_SALARY'] + fcl_result['REBET'] - fcl_result['BET'] + third_reuslt['THIRD_AWARD'] + fcl_result['THIRD_ACTIVITY'] + fcl_result['THIRD_REBET'] - third_reuslt['THIRD_BET'] + third_plat
            }

        fh = {
            'FH_BET': fcl_result['BET'],
            'FH_AWARD': fcl_result['AWARD'],
            'FH_ACTIVITY': fcl_result['ACTIVITY'],
            'CHARGE': fcl_result['CHARGE'],
            'WITHDRAW': fcl_result['WITHDRAW'],
            'REBET': fcl_result['REBET'],
            'DAILY_SALARY': fcl_result['DAILY_SALARY'],
            'FH_GP15': fcl_result['AWARD'] + fcl_result['ACTIVITY'] + fcl_result['DAILY_SALARY'] + fcl_result['REBET'] - fcl_result['BET'] + third_plat
        }

        third = {
            'THIRD_BET': third_reuslt['THIRD_BET'],
            'THIRD_AWARD': third_reuslt['THIRD_AWARD'],
            'THIRD_ACTIVITY': fcl_result['THIRD_ACTIVITY'],
            'CHARGE': fcl_result['CHARGE'],
            'WITHDRAW': fcl_result['WITHDRAW'],
            'THIRD_REBET': fcl_result['THIRD_REBET'],
            'THIRD_PLAT': third_plat,
            'THIRD_GP15': third_reuslt['THIRD_AWARD'] + fcl_result['THIRD_ACTIVITY'] + fcl_result['THIRD_REBET'] - third_reuslt['THIRD_BET']
        }
            
        return {'TOTAL': total, 'FH': fh, 'THIRD': third}

    def agentDetail(self, env: int, user: str, col: int, start: str, end: str, mode: int) -> list:
        '''
        param: mode 0 is team data, 1 is personal data
        start/end formate: '2022-06-02 00:00:00'
        '''
        if mode == 0:
            key = f'''(SELECT o_id FROM USER_CUSTOMER_FOR_REPORT_TEMP t where u_id=(SELECT ID FROM USER_CUSTOMER WHERE ACCOUNT='{user}'))'''
        elif mode == 1:
            key = f'''(SELECT ID FROM USER_CUSTOMER WHERE ACCOUNT='{user}')'''
        else:
            return []

        col_comparision = {
            0: self.bet,
            1: self.award,
            2: self.activity,
            3: self.third_activity,
            4: self.charge,
            5: self.withdraw,
            6: self.rebet,
            7: self.daily_salary + self.vip_rebet,
            8: self.third_rebet + self.third_vip_rebet
        }
        # 9: third_bet/third_award, 10: third_plat

        def fundChangeCal():
            reasons = '('+str(col_comparision[col])[1:-1]+')'

            conn = self.oracle(env)
            with conn.cursor() as cursor:
                sql = f'''SELECT
                        fcl.ID ,
                        uc.ACCOUNT ,
                        fcl.REASON ,
                        fcl.SN ,
                        abs(CT_BAL-BEFOR_BAL)/10000 AS amount,
                        abs(CT_DAMT - BEFORE_DAMT)/10000 AS sale,
                        fcl.GMT_CREATED 
                    FROM 
                        FUND_CHANGE_LOG fcl INNER JOIN USER_CUSTOMER uc ON fcl.USER_ID = uc.ID 
                    WHERE
                        fcl.USER_ID  IN {key}
                        AND fcl.REASON IN {reasons}
                        AND fcl.GMT_CREATED BETWEEN TO_DATE('{start}','yyyy-MM-dd HH24:mi:ss') AND TO_DATE('{end}','yyyy-MM-dd HH24:mi:ss')
                    ORDER BY 
                        REASON DESC
                '''
                cursor.execute(sql)
                rows = cursor.fetchall()

                result = []
                for data in rows:
                    if data[2] in ['GM,DVCB,null,2','GM,DVCN,null,2','HB,DHBS,null,2','FD,CWTS,null,5','FD,CWTS,null,6','FD,CWCS,null,4']:
                        value = data[5]
                    else:
                        value = data[4]
                    row = [data[0], data[1], data[2], self.reason_comparision_table[data[2]], data[3], value, data[6].strftime("%Y-%m-%d %H:%M:%S")]
                    result.append(row)

            conn.close()
            return result

        def thirdCal():
            conn = self.oracle(env)
            with conn.cursor() as cursor:
                sql = f'''SELECT 
                    FROM
                        THIRDLY_AGENT_CENTER tac
                    WHERE 
                        USER_ID  IN {key}
                        AND tac.CREATE_DATE BETWEEN TO_DATE('{start}','yyyy-MM-dd HH24:mi:ss') AND TO_DATE('{end}','yyyy-MM-dd HH24:mi:ss')

                '''
                cursor.execute(sql)
                rows = cursor.fetchall()
            conn.clsoe()
            return

        def thirdPlat():
            conn = self.oracle(env)
            with conn.cursor() as cursor:
                sql = f'''
                '''
                cursor.execute(sql)
                rows = cursor.fetchall()
            conn.clsoe()
            return
        
        if col in col_comparision:
            return fundChangeCal()
        elif col == 9:
            pass
        elif col == 10:
            pass
        else:
            return ['Wrong col']

if __name__ == '__main__':
    r = AgentCenter().verifyAgentData(1, 'peterfhn', '2022-10-14 00:00:00', '2022-10-15 00:00:00', 1)
    print(r)
    
    print(AgentCenter().oracle(1))