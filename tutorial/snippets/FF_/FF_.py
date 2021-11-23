class Env:
    def __init__(self):
        self.env = 1 # 0: dev02, 1: 188
        self.env_dict = {'測試總代': ['hsieh000','kerr000'] ,'一般帳號': ['hsieh001','kerr001'],'合營1940': ['hsiehwin1940test','kerrwin1940test'],'轉入/轉出':['kerrthird001','kerrthird001'],'APP帳號': ['hsiehapp001','kerrapp001'],'玩家':['hsieh0620','kerr010'],'APP合營': ['hsiehwin','kerrwin1940' ]}
        self.url_dict =  {0:['http://www.dev02.com','http://em.dev02.com'],
        1:['http://www2.joy188.com','http://em.joy188.com']}
        self.iapi_url = {0: 'http://10.13.22.152:8199/', 1: 'http://iphong.joy188.com/'}
        self.password = {0: ['123qwe','fa0c0fd599eaa397bd0daba5f47e7151'],1: ['amberrd','3bf6add0828ee17c4603563954473c1e']}
        self.trunk_login = {0: {
        'dev02': [{'hsieh000':u'總代','hsieh001':u'一代','hsiehthird001':'一代','hsieh001001':'','hsieh001002':'',
        'hsieh0420001':''},'一般4.0'],
        'fh82dev02': [{'hsiehwin000':u'總代','hsiehwin001':u'一代','hsiehwin1940test':'合營1940' },'一般合營']} 
        ,1:{'joy188.teny2020':[{'kerrwin000':u'總代','kerrwin001':u'一代'},'合營teny'],
        'joy188.195353':[{'kerrwin1940test':u'合營1940'},'一般合營'],
        'joy188.88hlqp':[{'hlqp001':u'總代','kerrlc001':u'玩家'},'歡樂棋牌'],
        'joy188':[{'kerr000':u'總代','kerr001':u'一代','kerr43453':u'玩家',
        'kerrthird001':'二代'},'一般4.0']}
        }
class Lottery:
    def __init__(self):
        self.lottery_dict = {
        'cqssc':[u'重慶','99101'],'xjssc':[u'新彊時彩','99103'],'tjssc':[u'天津時彩','99104'],'hljssc':[u'黑龍江','99105'],'llssc':[u'樂利時彩','99106'],'shssl':[u'上海時彩','99107'],'jlffc':[u'吉利分彩','99111'],'slmmc':[u'順利秒彩','99112'],'txffc':[u'騰訊分彩','99114'],'btcffc':[u'比特幣分彩','99115'],'fhjlssc':[u'吉利時彩','99116'],'sd115':[u'山東11選5','99301'],'jx115':[u"江西11選5",'99302'],'gd115':[u'廣東11選5','99303'],'sl115':[u'順利11選5','99306'],'jsk3':[u'江蘇快3','99501'],'ahk3':[u'安徽快3','99502'],'jsdice':[u'江蘇骰寶','99601'],'jldice1':[u'吉利骰寶(娛樂)','99602'],'jldice2':[u'吉利骰寶(至尊)','99603'],'fc3d':[u'3D','99108'],'p5':[u'排列5','99109'],'lhc':[u'六合彩','99701'],'btcctp':[u'快開','99901'],'pk10':[u"pk10",'99202'],'v3d':[u'吉利3D','99801'], 'xyft':[u'幸運飛艇','99203'],'fhxjc':[u'鳳凰新疆','99118'],'fhcqc':[u'鳳凰重慶','99117'],'n3d':[u'越南3d','99124'],'np3':[u'越南福利彩','99123'],'pcdd':[u'PC蛋蛋','99204'],'xyft168':[u'幸運飛艇168','99205'], 'fckl8':[u'福彩快樂8','99206'],'ptxffc':[u'奇趣腾讯分分彩','99125'],'hn60':[u'多彩河内分分彩','99126'],'hnffc':[u'河内分分彩','99119'],'hn5fc':[u'河内五分彩','99120'],'tmffc':['天貓分分彩','99127'],
        'tm3fc': ['天貓三分彩','99128'], 'tm5fc': ['天貓五分彩','99129'],
        'super2000': ['超級2000App','99113']}

        self.lottery_sh = ['cqssc','xjssc','tjssc','hljssc','llssc','jlffc','slmmc','txffc','fhjlssc','btcffc','fhcqc','fhxjc','hnffc','hn5fc','hn60','ptxffc','tmffc','tm3fc','tm5fc']
        self.lottery_sh2000 = ['cqssc','xjssc','tjssc','hljssc','fhjlssc','fhcqc','fhxjc','hn5fc','super2000','tm5fc']
        self.lottery_3d = ['v3d']
        self.lottery_115 = ['sd115','jx115','gd115','sl115']
        self.lottery_k3 = ['ahk3','jsk3']
        self.lottery_sb = ['jsdice',"jldice1",'jldice2']
        self.lottery_fun = ['pk10','xyft','xyft168']
        self.lottery_noRed = ['fc3d','n3d','np3','p5']#沒有紅包
        
        self.LotterySsh_group = {'wuxing':{'zhixuan':['fushi'],
            'zuxuan':['zuxuan120','zuxuan60','zuxuan30','zuxuan20','zuxuan10''zuxuan5'],
            'budingwei':['ermabudingwei','sanmabudingwei'],
            'quwei':['yifanfengshun','haoshichengshuang','sanxingbaoxi','sijifacai']},
        'sixing': {'zhixuan':['fushi'],
            'zuxuan':['zuxuan24','zuxuan12','zuxuan6','zuxuan4'],
            'budingwei':['ermabudingwei','yimabudingwei']},
        'qiansan': {'zhixuan':['fushi','hezhi','kuadu'],
            'zuxuan':['hezhi','baodan','zusan','zuliu'],
            'budingwei': ['ermabudingwei','yimabudingwei']},
        'housan': {'zhixuan':['fushi','hezhi','kuadu'],
            'zuxuan':['hezhi','baodan','zusan','zuliu'],
            'budingwei':['ermabudingwei','yimabudingwei']},
        'zhongsan': {'zhixuan':['fushi','hezhi','kuadu'],
            'zuxuan':['hezhi','baodan','zusan','zuliu'],
            'budingwei':['ermabudingwei','yimabudingwei']},
        'qianer': {'zhixuan':['fushi','hezhi','kuadu'],
            'zuxuan':['hezhi','baodan','fushi']},
        'houer':{'zhixuan':['fushi','hezhi','kuadu'],
            'zuxuan':['hezhi','baodan','fushi']},
        'yixing': {'dingweidan':['fushi']},
        'housan_2000' : {'zhixuan':['fushi','hezhi','kuadu'],
            'zuxuan': ['hezhi','baodan','zusan','zuliu'],
            'budingwei': ['ermabudingwei','yimabudingwei']},
        'houer_2000':{'zhixuan':['fushi','hezhi','kuadu'],
            'zuxuan':['hezhi','baodan','fushi'] },
        'yixing_2000':{'dingweidan':['fushi']},
            'daxiaodanshuang': {'dxds':['zonghe','qianyi','qianer','houyi','houer']},
            'longhu': {'longhudou':['fushi'] }
        }
        self.Lottery115_group = {'xuanyi': {'qiansanyimabudingwei':['fushi'],
            'dingweidan':['fushi'], 'renxuanyizhongyi': ['fushi']},
        'xuaner': {'qianerzhixuan':['zhixuanfushi'],'qianerzuxuan':['zuxuanfushi','zuxuandantuo'],'renxuanerzhonger':['renxuanfushi','renxuandantuo']},
        'xuansan': {'qiansanzhixuan':['zhixuanfushi'],'qiansanzuxuan':['zuxuanfushi','zuxuandantuo'],'renxuansanzhongsan':['renxuanfushi','renxuandantuo']},
        'xuansi': {'renxuansizhongsi':['fushi','dantuo']},
        'xuanwu': {'renxuanwuzhongwu':['fushi','dantuo']},
        'xuanliu':{'renxuanliuzhongwu':['fushi','dantuo']},
        'xuanqi':{'renxuanqizhongwu':['fushi','dantuo']},
        'xuanba':{'renxuanbazhongwu': ['fushi','dantuo'] },
        'quwei':{'normal':['dingdanshuang','caizhongwei']}
        }
class Third:
    def __init__(self):
        self.third_list = ['gns','shaba','im','ky','lc','city','bg','yb','pg']

class Others:
    def __init__(self):
        self.usdt_dict  = {
            'TRC-20':['T1166616165a1S1DCD2FD7afefff651651','2'],
            'ERC-20':['0xaaaaaaaaaaaaaaaaaaa11aa11111111111111111','3']
        }