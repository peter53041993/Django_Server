import unittest, time
import HTMLTestRunner
from HTMLTestRunner import HTMLTestRunner
from time import sleep
import os 
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

# local module:
from . import FF_
from .joy188_test_trunk import Joy188Test, Joy188Test2, Joy188Test3

'''
自動化測試報告   , test_LotterySubmit 執行trunk腳本時, 需注意  req_post_submit 的cookie和 lottery是否更換
'''


envs = FF_.Env().env
env_dict = {0: 'dev02', 1: 'joy188'}
env_name = env_dict[envs]

suite = unittest.TestSuite()

tests = [Joy188Test('test_Login'),Joy188Test('test_redEnvelope'),Joy188Test('test_LotterySubmit'),
        Joy188Test('test_CancelOrder'),Joy188Test('test_LotteryPlanSubmit'),
        Joy188Test('test_ThirdHome'),Joy188Test('test_188'),Joy188Test('test_chart'),
        Joy188Test('test_thirdBalance'),Joy188Test('test_transferin'),Joy188Test('test_transferout'),
        Joy188Test('test_tranUser'),Joy188Test('test_ChargeLimit'), Joy188Test('test_Spuer2000Submit'), ]

tests2 = [Joy188Test2('test_safepersonal'),Joy188Test2('test_applycenter')
,Joy188Test2('test_safecenter'),Joy188Test2('test_bindcard'),Joy188Test2('test_bindcardUs')]

app = [Joy188Test3('test_iapiLogin'),Joy188Test3('test_iapiSubmit'),
        Joy188Test3('test_IapiCancelSubmit'),Joy188Test3('test_IapiPlanSubmit'),
        Joy188Test3('test_OpenLink'),
        Joy188Test3('test_AppRegister'),
        Joy188Test3('test_IapiSecurityPass'),Joy188Test3('test_IapiSecurityQues'),
        Joy188Test3('test_IapiCardBind'),Joy188Test3('test_IapiLockCard'),
        Joy188Test3('test_IapiRecharge'),
        Joy188Test3('test_IapiWithDraw'),Joy188Test3('test_iapiCheckIn'),
        Joy188Test3('test_AppBalance'),
        Joy188Test3('test_ApptransferIn'),Joy188Test3('test_ApptransferOut'),
        Joy188Test3('test_AppcheckPassword'),Joy188Test3('test_IapiTransfer'),
        Joy188Test3('test_IapiOgAgent'),Joy188Test3('test_IapiNewAgent')
        ]

test = [Joy188Test('test_Login'),Joy188Test('test_Spuer2000Submit') ]


def run_trunk(unit: str) -> str:
        '''
        param: unit, 1.web_api, 2.web_front, 3.iapi, 4.all
        return: filename (str)
        '''
        #suite.addTests(test)

        # all units
        if unit == 'all': 
                suite.addTests(tests)
                suite.addTests(tests2)
                suite.addTests(app)
        elif unit == 'web_api':
                suite.addTests(tests)
        elif unit == 'web_front':
                suite.addTests(tests2)
        elif unit == 'iapi':
                suite.addTest(Joy188Test('test_Login'))
                suite.addTest(Joy188Test('test_LotterySubmit'))
                suite.addTests(app)
        else:
                raise('unit type error: 1.web_api, 2.web_front, 3.iapi, 4.all')


        now = time.strftime('%Y_%m_%d^%H-%M-%S')
        filename = now + u'自動化測試' + '.html'
        fp = open(f'C:\\Users\\Peter\\drf_test\\tutorial\\snippets\\trunk_reports\\{filename}', 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(
                stream = fp,
                title = u'測試報告',
                description = u'環境: %s' % env_name
                )
        runner.run(suite)
        fp.close()

        return filename
