class BetNumsConfig:
    def __init__(self) -> None:
        self.betNumsConfig = {
            '18_13_65':	6,      #趣味	趣味	定单双
            '18_13_66':	7,      #趣味	趣味	猜中位
            '22_12_10': 11,     #选一	前三一码不定位	复式
            # 22_14_10	选一	定位胆	复式	11(每位數)
            '22_20_10':	11,     #选一	任选一中一	复式
            '22_20_11': 11,     #选一	任选一中一	单式
            '23_10_10': 110,    #选二	前二直选	复式
            '23_10_11': 110,    #选二	前二直选	单式
            '23_11_10': 55,     #选二	前二组选	复式
            '23_11_11': 55,     #选二	前二组选	单式
            '23_11_12':	10,     #选二	前二组选	胆拖
            '23_21_10': 55,     #选二	任选二中二	复式
            '23_21_11':	55,     #选二	任选二中二	单式
            '23_21_12': 10,     #选二	任选二中二	胆拖
            '24_10_10': 990,    #选三	前三直选	复式
            '24_10_11': 990,    #选三	前三直选	单式
            '24_11_10': 165,    #选三	前三组选	复式
            '24_11_11':	165,    #选三	前三组选	单式
            '24_11_12':	45,     #选三	前三组选	胆拖
            '24_22_10':	165,    #选三	任选三中三	复式
            '24_22_11':	165,    #选三	任选三中三	单式
            '24_22_12':	45,     #选三	任选三中三	胆拖
            '25_23_10':	330,    #选四	任选四中四	复式
            '25_23_11':	330,    #选四	任选四中四	单式
            '25_23_12':	120,    #选四	任选四中四	胆拖
            '26_24_10':	462,    #选五	任选五中五	复式
            '26_24_11':	462,    #选五	任选五中五	单式
            '26_24_12':	210,    #选五	任选五中五	胆拖
            '27_25_10':	462,    #选六	任选六中五	复式
            '27_25_11':	462,    #选六	任选六中五	单式
            '27_25_12':	252,    #选六	任选六中五	胆拖
            '28_26_10':	330,    #选七	任选七中五	复式
            '28_26_11':	330,    #选七	任选七中五	单式
            '28_26_12':	210,    #选七	任选七中五	胆拖
            '29_27_10':	165,    #选八	任选八中五	复式
            '29_27_11':	165,    #选八	任选八中五	单式
            '29_27_12':	120,    #选八	任选八中五	胆拖
            '12_10_10':	1000,   #P3三星	直选	复式
            '12_10_10':	1000,   #三星	直选	复式
            '12_10_11':	1000,   #P3三星	直选	单式
            '12_10_11':	1000,   #三星	直选	单式
            '12_10_33':	1000,   #P3三星	直选	直选和值
            '12_10_33':	1000,   #三星	直选	直选和值
            '12_10_34':	1000,   #P3三星	直选	跨度
            '12_10_34':	1000,   #三星	直选	跨度
            '12_11_33':	210,    #P3三星	组选	组选和值
            '12_11_33':	210,    #三星	组选	组选和值
            '12_11_35':	90,     #P3三星	组选	组三
            '12_11_35':	90,     #三星	组选	组三
            '12_11_36':	120,    #P3三星	组选	组六
            '12_11_36':	120,    #三星	组选	组六
            '12_11_37':	1000,   #P3三星	组选	混合组选
            '12_11_37':	1000,   #三星	组选	混合组选
            '12_11_39':	540,    #P3三星	组选	组选包胆
            '12_11_39':	540,    #三星	组选	组选包胆
            '12_11_62':	90,     #P3三星	组选	组三单式
            '12_11_62':	90,     #三星	组选	组三单式
            '12_11_63':	120,    #P3三星	组选	组六单式
            '12_11_63':	120,    #三星	组选	组六单式
            '12_12_40':	10,     #P3三星	不定位	一码不定位
            '12_12_40':	10,     #三星	不定位	一码不定位
            '12_12_41':	45,     #P3三星	不定位	二码不定位
            '12_12_41':	45,     #三星	不定位	二码不定位
            '14_10_10':	100,    #P3后二	直选	直选复式
            '14_10_10':	100,    #后二	直选	直选复式
            '14_10_11':	100,    #P3后二	直选	直选单式
            '14_10_11':	100,    #后二	直选	直选单式
            '14_10_33':	100,    #P3后二	直选	直选和值
            '14_10_33':	100,    #后二	直选	直选和值
            '14_10_34':	100,    #P3后二	直选	跨度
            '14_10_34':	100,    #后二	直选	跨度
            '14_11_10':	45,     #P3后二	组选	组选复式
            '14_11_10':	45,     #后二	组选	组选复式
            '14_11_11':	45,     #P3后二	组选	组选单式
            '14_11_11':	45,     #后二	组选	组选单式
            '14_11_33':	45,     #P3后二	组选	组选和值
            '14_11_33':	45,     #后二	组选	组选和值
            '14_11_39':	90,     #P3后二	组选	组选包胆
            '14_11_39':	90,     #后二	组选	组选包胆
            '15_10_10':	100,    #P3前二	直选	直选复式
            '15_10_10':	100,    #前二	直选	直选复式
            '15_10_11':	100,    #P3前二	直选	直选单式
            '15_10_11':	100,    #前二	直选	直选单式
            '15_10_33':	100,    #P3前二	直选	直选和值
            '15_10_33':	100,    #前二	直选	直选和值
            '15_10_34':	100,    #P3前二	直选	跨度
            '15_10_34':	100,    #前二	直选	跨度
            '15_11_10':	45,     #P3前二	组选	组选复式
            '15_11_10':	45,     #前二	组选	组选复式
            '15_11_11':	45,     #P3前二	组选	组选单式
            '15_11_11':	45,     #前二	组选	组��单式
            '15_11_11':	45,     #前二	组选	组选单式
            '15_11_33':	45,     #P3前二	组选	组选和值
            '15_11_33':	45,     #前二	组选	组选和值
            '15_11_39':	90,     #P3前二	组选	组选包胆
            '15_11_39':	90,     #前二	组选	组选包胆
            # '16_14_10':	一星	定位胆	复式	10(每位數),
            '30_10_10':	100,    #P5后二	直选	直选复式
            '30_10_11':	100,	#P5后二	直选	直选单式
            '30_10_33':	100,    #P5后二	直选	直选和值
            '30_10_34':	100,    #P5后二	直选	跨度	
            '30_11_10':	45,     #P5后二	组选	组选复式
            '30_11_11':	45,     #P5后二	组选	组选单式
            '30_11_33':	45,     #P5后二	组选	组选和值
            '30_11_39':	90,     #P5后二	组选	组选包胆
            # '31_14_10':	P5一星	定位胆	复式	10(每位數),
            '53_17_64':	49,     #正码	平码	直选六码
            '54_10_81':	49,     #特码	直选	直选一码
            '54_18_82':	61,     #特码	特肖	特肖
            '54_19_84':	3,      #特码	色波	色波
            '54_19_85':	12,     #特码	色波	半波
            '54_37_83':	12,     #特码	两面	两面
            '55_38_86':	12,     #正特码	一肖	一肖
            '55_39_87':	211876, #正特码	不中	四不中
            # '55_39_88':	1906884,#正特码	不中	五不中
            # '55_39_89':	13983816,#正特码	不中	六不中
            # '55_39_90':	85900584,#正特码	不中	七不中
            # '55_39_91':	450978066,#正特码	不中	八不中
            '55_40_92':	66,     #正特码	连肖(中)	二连肖
            '55_40_93':	220,    #正特码	连肖(中)	三连肖	
            '55_40_94':	495,    #正特码	连肖(中)	四连肖
            '55_40_95':	792,    #正特码	连肖(中)	五连肖
            '55_41_92':	78,     #正特码	连肖(不中)	二连肖
            '55_41_93':	220,    #正特码	连肖(不中)	三连肖	
            '55_41_94':	495,    #正特码	连肖(不中)	四连肖
            '55_41_95':	792,    #正特码	连肖(不中)	五连肖
            '56_42_13':	18424,  #连码	连码	三全中
            '56_42_14':	19600,  #连码	连码	三中二
            '56_42_15':	1176,   #连码	连码	二全中
            '56_42_16':	1176,   #连码	连码	二中特
            '56_42_17':	2352,   #连码	连码	特串
            # '32_71_67':	14254400160,#标准玩法	标准	复式
            # '32_71_68':	14254400160,#标准玩法	标准	单式	
            # '32_71_69':	3054514320,#标准玩法	标准	胆拖
            '17_15_23':	10,     #任选	普通玩法	任选1
            '17_15_24':	45,     #任选	普通玩法	任选2
            '17_15_25':	120,    #任选	普通玩法	任选3
            '17_15_26':	210,    #任选	普通玩法	任选4
            '17_15_27':	252,    #任选	普通玩法	任选5
            '17_15_28':	210,    #任选	普通玩法	任选6
            '17_15_29':	120,    #任选	普通玩法	任选7
            # '18_16_70':	趣味	盘面	趣味型	
            '57_10_10':	90,     #冠亚	直选	复式
            '57_10_11':	90,     #冠亚	直选	单式
            '57_11_10':	45,     #冠亚	组选	复式
            '57_11_11':	45,     #冠亚	组选	单式
            '57_28_10':	90,     #冠亚	和值	复式
            '57_43_10':	90,     #冠亚	猜冠亚	复式
            '57_43_11':	90,     #冠亚	猜冠亚	单式
            '58_10_10':	720,    #冠亚季	直选	复式
            '58_10_11':	720,    #冠亚季	直选	单式
            '58_11_10':	120,    #冠亚季	组选	复式
            '58_11_11':	120,    #冠亚季	组选	单式
            '58_44_10':	720,    #冠亚季	猜冠亚季	复式
            '58_44_11':	720,    #冠亚季	猜冠亚季	单式
            '59_10_10':	5040,   #前四	直选	复式
            '59_10_11':	5040,   #前四	直选	单式
            '59_11_10':	210,    #前四	组选	复式
            '59_11_11':	210,    #前四	组选	单式
            '60_10_10':	30240,  #前五	直选	复式
            '60_10_11':	30240,  #前五	直选	单式
            '60_11_10':	252,    #前五	组选	复式
            '60_11_11':	252,    #前五	组选	单式
            # '61_14_96':	猜排位	定位胆	1-5位复式	10(每位數),
            # '61_14_97':	猜排位	定位胆	6-10位复式	10(每位數),
            # '62_45_10':	大小单双	大小单双	复式	4(每名),
            # '63_46_10':	龙虎	龙虎	复式	2(每名),
            # '66_13_109':	整合	趣味	豹子	X,
            '66_13_110': 17550, #整合	趣味	特码包三
            '66_13_84':	3,      #整合	趣味	色波
            '66_28_71':	27,     #整合	和值	和值
            '66_74_106': 4,     #整合	双面	大小单双
            '66_74_107': 4,     #整合	双面	组合大小单双
            '66_74_108': 2,     #整合	双面	极值
            '19_47_18':	6,      #猜不出	猜不出	猜不出
            '34_28_71':	16,     #和值	和值	和值
            # '35_29_72':三同号通选	三同号通选	三同号通选	X,
            '36_30_73':	6,      #三同号单选	三同号单选	三同号单选
            '37_31_12':	10,     #三不同号	三不同号	胆拖
            '37_31_74':	20,     #三不同号	三不同号	标准
            # '38_32_75':三连号通选	三连号通选	三连号通选	X,
            '39_33_76':	6,      #二同号复选	二同号复选	二同号复选
            '40_34_77':	6,      #二同号单选	二同号单选	二同号单选
            '41_35_12':	5,      #二不同号	二不同号	胆拖
            '41_35_74':	15,     #二不同号	二不同号	标准
            '42_36_78':	6,      #猜1个号就中奖	猜1个号就中奖	猜1个号就中奖
            '42_36_78':	6,      #猜一个号	猜一个号	猜1个号（特殊）
            '43_37_79':	2,      #特殊	两面	大小
            '43_37_80':	2,      #特殊	两面	单双
            '64_48_98':	2,      #龙虎和	龙虎和	龙虎
            # '64_48_99':	龙虎和	龙虎和	和	X,
            '10_10_10':	100000, #五星	直选	复式
            '10_10_11':	100000, #五星	直选	单式
            '10_11_43':	252,    #五星	组选	组选120
            '10_11_44':	840,    #五星	组选	组选60
            '10_11_45':	360,    #五星	组选	组选30
            '10_11_46':	360,    #五星	组选	组选20
            '10_11_47':	90,     #五星	组选	组选10
            '10_11_48':	90,     #五星	组选	组选5
            '10_12_40':	10,     #五星	不定位	一码不定位
            '10_12_41':	45,     #五星	不定位	二码不定位
            '10_12_42':	120,    #五星	不定位	三码不定位
            '10_13_53':	10,	    #五星	趣味	一帆风顺
            '10_13_54':	10,     #五星	趣味	好事成双
            '10_13_55':	10,     #五星	趣味	三星报喜
            '10_13_56':	10,     #五星	趣味	四季发财
            '11_10_10':	10000,  #四星	直选	复式
            '11_10_11':	10000,  #四星	直选	单式
            '11_11_49':	210,    #四星	组选	组选24
            '11_11_50':	360,    #四星	组选	组选12
            '11_11_51':	45,     #四星	组选	组选6
            '11_11_52':	90,     #四星	组选	组选4
            '11_12_40':	10,     #四星	不定位	一码不定位
            '11_12_41':	45,     #四星	不定位	二码不定位
            '12_10_10':	1000,   #前三	直选	复式
            '12_10_11':	1000,   #前三	直选	单式
            '12_10_33':	1000,   #前三	直选	直选和值
            '12_10_34':	1000,   #前三	直选	跨度
            '12_11_33':	210,    #前三	组选	组选和值
            '12_11_35':	90,     #前三	组选	组三
            '12_11_36':	120,    #前三	组选	组六
            '12_11_37':	120,    #前三	组选	混合组选
            '12_11_39':	540,    #前三	组选	组选包胆
            '12_11_62':	90,     #前三	组选	组三单式
            '12_11_63':	120,    #前三	组选	组六单式
            '12_12_40':	10,     #前三	不定位	一码不定位
            '12_12_41':	45,     #前三	不定位	二码不定位
            '13_10_10':	1000,   #三星	直选	复式
            '13_10_10':	1000,   #后三	直选	复式
            '13_10_11':	1000,   #三星	直选	单式
            '13_10_11':	1000,   #后三	直选	单式
            '13_10_33':	1000,   #三星	直选	直选和值
            '13_10_33':	1000,   #后三	直选	直选和值
            '13_10_34':	1000,   #三星	直选	跨度
            '13_10_34':	1000,   #后三	直选	跨度
            '13_11_33':	210,    #三星	组选	组选和值
            '13_11_33':	210,    #后三	组选	组选和值
            '13_11_35':	90,     #三星	组选	组三
            '13_11_35':	90,     #后三	组选	组三
            '13_11_36':	120,    #三星	组选	组六
            '13_11_36':	120,    #后三	组选	组六
            '13_11_37':	120,    #三星	组选	混合组选
            '13_11_37':	120,    #后三	组选	混合组选
            '13_11_39':	540,    #三星	组选	组选包胆
            '13_11_39':	540,    #后三	组选	组选包胆
            '13_11_62':	90,     #三星	组选	组三单式
            '13_11_62':	90,     #后三	组选	组三单式
            '13_11_63':	120,    #三星	组选	组六单式
            '13_11_63':	120,    #后三	组选	组六单式
            '13_12_40':	10,     #三星	不定位	一码不定位
            '13_12_40':	10,     #后三	不定位	一码不定位
            '13_12_41':	45,     #三星	不定位	二码不定位
            '13_12_41':	45,     #后三	不定位	二码不定位
            '14_10_10':	100,    #后二	直选	直选复式
            '14_10_11':	100,    #后二	直选	直选单式
            '14_10_33':	100,    #后二	直选	直选和值
            '14_10_34':	100,    #后二	直选	跨度
            '14_11_10':	45,     #后二	组选	组选复式
            '14_11_11':	45,     #后二	组选	组选单式
            '14_11_33':	45,     #后二	组选	组选和值
            '14_11_39':	81,     #后二	组选	组选包胆
            '15_10_10':	100,    #前二	直选	直选复式
            '15_10_11':	100,    #前二	直选	直选单式
            '15_10_33':	100,    #前二	直选	直选和值
            '15_10_34':	100,    #前二	直选	跨度
            '15_11_10':	45,     #前二	组选	组选复式
            '15_11_11':	45,     #前二	组选	组选单式
            '15_11_33':	45,     #前二	组选	组选和值
            '15_11_39':	81,     #前二	组选	组选包胆
            # '16_14_10':	一星	定位胆	复式	10(每位數),
            '33_10_10':	1000,   #中三	直选	复式
            '33_10_11':	1000,   #中三	直选	单式
            '33_10_33':	1000,   #中三	直选	直选和值
            '33_10_34':	1000,   #中三	直选	跨度
            '33_11_33':	210,    #中三	组选	组选和值
            '33_11_35':	90,     #中三	组选	组三
            '33_11_36':	120,    #中三	组选	组六
            '33_11_37':	120,    #中三	组选	混合组选
            '33_11_39':	540,    #中三	组选	组选包胆
            '33_11_62':	90,     #中三	组选	组三单式
            '33_11_63':	120,    #中三	组选	组六单式
            '33_12_40':	10,     #中三	不定位	一码不定位
            '33_12_41':	45,     #中三	不定位	二码不定位
            '47_10_10':	1000,   #超级2000_后三	直选	复式
            '47_10_11':	1000,   #超级2000_后三	直选	单式
            '47_10_33':	1000,   #超级2000_后三	直选	直选和值
            '47_10_34':	1000,   #超级2000_后三	直选	跨度
            '47_11_33':	210,    #超级2000_后三	组选	组选和值
            '47_11_35':	90,     #超级2000_后三	组选	组三
            '47_11_36':	120,    #超级2000_后三	组选	组六
            '47_11_37':	120,    #超级2000_后三	组选	混合组选
            '47_11_39':	540,    #超级2000_后三	组选	组选包胆
            '47_11_62':	90,     #超级2000_后三	组选	组三单式
            '47_11_63':	120,    #超级2000_后三	组选	组六单式
            '47_12_40':	10,     #超级2000_后三	不定位	一码不定位
            '47_12_41':	45,     #超级2000_后三	不定位	二码不定位
            '48_10_10':	100,    #超级2000_后二	直选	直选复式
            '48_10_11':	100,    #超级2000_后二	直选	直选单式
            '48_10_33':	100,    #超级2000_后二	直选	直选和值
            '48_10_34':	100,    #超级2000_后二	直选	跨度
            '48_11_10':	45,     #超级2000_后二	组选	组选复式
            '48_11_11':	45,     #超级2000_后二	组选	组选单式
            '48_11_33':	45,     #超级2000_后二	组选	组选和值
            '48_11_39':	81,     #超级2000_后二	组选	组选包胆
            # '50_14_10':	超级2000_一星	定位胆	复式	10(每位數),
            '51_10_10':	10000,  #超级2000_四星	直选	复式
            '51_10_11':	10000,  #超级2000_四星	直选	单式
            '51_11_49':	210,    #超级2000_四星	组选	组选24
            '51_11_50':	360,    #超级2000_四星	组选	组选12
            '51_11_51':	45,     #超级2000_四星	组选	组选6
            '51_11_52':	90,     #超级2000_四星	组选	组选4
            '51_12_40':	10,     #超级2000_四星	不定位	一码不定位
            '51_12_41':	45,     #超级2000_四星	不定位	二码不定位
            '52_10_10':	1000,   #超级2000_中三	直选	复式
            '52_10_11':	1000,   #超级2000_中三	直选	单式
            '52_10_33':	1000,   #超级2000_中三	直选	直选和值
            '52_10_34':	1000,   #超级2000_中三	直选	跨度
            '52_11_33':	210,    #超级2000_中三	组选	组选和值
            '52_11_35':	90,     #超级2000_中三	组选	组三
            '52_11_36':	120,    #超级2000_中三	组选	组六
            '52_11_37':	120,    #超级2000_中三	组选	混合组选	
            '52_11_39':	540,    #超级2000_中三	组选	组选包胆
            '52_11_62':	90,     #超级2000_中三	组选	组三单式	
            '52_11_63':	120,    #超级2000_中三	组选	组六单式	
            '52_12_40':	10,     #超级2000_中三	不定位	一码不定位	
            '52_12_41':	45,     #超级2000_中三	不定位	二码不定位	
            '62_45_100': 4,     #大小单双	大小单双	总和大小单双	
            '62_45_101': 4,     #大小单双	大小单双	前一大小单双	
            '62_45_102': 4,     #大小单双	大小单双	前二大小单双	
            '62_45_103': 4,     #大小单双	大小单双	后一大小单双	
            '62_45_104': 4,     #大小单双	大小单双	后二大小单双	
            # '63_49_10':	龙虎	龙虎斗	复式	X,
            # '67_75_111':	双面盘	总和	总和龙虎和	X,
            '67_75_112': 2,     #双面盘	总和	总和大小	
            '67_75_113': 2,     #双面盘	总和	总和单双	
            '67_76_114': 2,     #双面盘	选码	选码大小	
            '67_76_115': 2,     #双面盘	选码	选码单双	
            # '67_76_116':	双面盘	选码	选码球号	,
            # '67_77_117':	双面盘	前三	前三豹子	X,
            # '67_77_118':	双面盘	前三	前三顺子	X,
            # '67_77_119':	双面盘	前三	前三对子	X,
            # '67_77_120':	双面盘	前三	前三半顺	X,
            # '67_77_121':	双面盘	前三	前三杂六	X,
            # '67_78_117':	双面盘	中三	中三豹子	X,
            # '67_78_118':	双面盘	中三	中三顺子	X,
            # '67_78_119':	双面盘	中三	中三对子	X,
            # '67_78_120':	双面盘	中三	中三半顺	X,
            # '67_78_121':	双面盘	中三	中三杂六	X,
            # '67_79_117':	双面盘	后三	后三豹子	X,
            # '67_79_117':	双面盘	后三	后三顺子	X,
            # '67_79_119':	双面盘	后三	后三对子	X,
            # '67_79_120':	双面盘	后三	后三半顺	X,
            # '67_79_121':	双面盘	后三	后三杂六	X,
            # '65_72_105':	冲天炮	冲天炮	冲天炮	X
        }
    
        self.exception = [
            '18_16_70', '66_13_109', '35_29_72', '35_29_72', '64_48_99', '63_49_10', '67_75_111',
            '67_77_117', '67_77_117', '67_77_118', '67_77_119', '67_77_120', '67_77_121', '67_78_117',
            '67_78_118', '67_78_119', '67_78_120', '67_78_121', '67_79_117', '67_79_119', '67_79_120', '67_79_121',
            '65_72_105', '55_39_88', '55_39_89', '55_39_90', '55_39_91', '32_71_67', '32_71_68', '32_71_69'
        ]
        self.nums11 = [
            '22_14_10'
        ]

        self.nums10 = [
            '16_14_10', '31_14_10', '61_14_96', '50_14_10', '61_14_97'
        ]

        self.nums4 = [
            '62_45_10'
        ]

        self.nums2 = [
            '63_46_10'
        ]

        self.shuangmian = [
            '67_75_112', '67_75_113', '67_76_114', '67_76_115', '67_76_116'
        ]

    def checkNuns11(self, betContent: str) -> float:
        bet = betContent.split(',')
        max_ratio = 0
        for slip in bet:
            s = slip.split(' ')
            if s != ['_']:
                ratio = len(s)/11
                max_ratio = max(max_ratio, ratio)
        return round(max_ratio, 6)
    
    def checkNuns10(self, betContent):
        bet = betContent.split(',')
        max_ratio = 0
        for slip in bet:
            if slip != '_':
                ratio = len(slip)/10
                max_ratio = max(max_ratio, ratio)
        return round(max_ratio, 6)
    
    def checkNuns4(self, betContent):
        if not betContent:
            return None

        check = {}
        for slip in betContent:
            key, value = slip[:-1], slip[-1:]
            if key not in check:
                check[key] = set(value)
            else:
                check[key].add(value)
        
        max_ratio = 0
        for k, v in check.items():
            ratio = len(v)/4
    
    def checkNuns2(self, betContent):
        ...

if __name__ == '__main__':
    betContent = '012789,5,56,578,-,-'

    print(BetNumsConfig().checkNuns10(betContent))
    import collections
    res = collections.defaultdict(int)

    for i in range(10):
        res['r'] += 0
    print(res)