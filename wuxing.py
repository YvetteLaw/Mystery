
class WuxingNode(object):
    def __init__(self, name, pos, season, xwxqs):
        self.name = name
        self.left = None
        self.right = None
        self.direction = pos
        self.season = season
        self.xwxqs = xwxqs


wx_mu = WuxingNode('木', '东', '春', {'春': '旺', '冬': '相', '夏': '休', '四季': '囚', '秋': '死'})
wx_huo = WuxingNode('火', '南', '夏', {'夏': '旺', '春': '相', '四季': '休', '秋': '囚', '冬': '死'})
wx_tu = WuxingNode('土', '西', '秋', {'四季': '旺', '夏': '相', '秋': '休', '冬': '囚', '春': '死'})
wx_jin = WuxingNode('金', '北', '冬', {'秋': '旺', '四季': '相', '冬': '休', '春': '囚', '夏': '死'})
wx_shui = WuxingNode('水', '中', '四季', {'冬': '旺', '秋': '相', '春': '休', '夏': '囚', '四季': '死'})


class WuxingLink(object):
    def __init__(self):
        self.attrs = [wx_mu, wx_huo, wx_tu, wx_jin, wx_shui]

    def improve(self):
        wx_mu.left = wx_shui
        wx_mu.right = wx_huo
        wx_huo.left = wx_mu
        wx_huo.right = wx_tu
        wx_tu.left = wx_huo
        wx_tu.right = wx_jin
        wx_jin.left = wx_tu
        wx_jin.right = wx_shui
        wx_shui.left = wx_jin
        wx_shui.right = wx_mu

    def impair(self):
        wx_mu.left = wx_jin
        wx_mu.right = wx_tu
        wx_huo.left = wx_shui
        wx_huo.right = wx_jin
        wx_tu.left = wx_mu
        wx_tu.right = wx_shui
        wx_jin.left = wx_huo
        wx_jin.right = wx_mu
        wx_shui.left = wx_tu
        wx_shui.right = wx_huo

    def who_improve_me(self, attr):
        self.improve()
        for node in self.attrs:
            if node.name == attr:
                return node.left.name
        print('错误传参！仅限以下之一：金、木、水、火、土')
        return ''

    def me_improve_who(self, attr):
        self.improve()
        for node in self.attrs:
            if node.name == attr:
                return node.right.name
        print('错误传参！仅限以下之一：金、木、水、火、土')
        return ''

    def who_impair_me(self, attr):
        self.impair()
        for node in self.attrs:
            if node.name == attr:
                return node.left.name
        print('错误传参！仅限以下之一：金、木、水、火、土')
        return ''

    def me_impair_who(self, attr):
        self.impair()
        for node in self.attrs:
            if node.name == attr:
                return node.right.name
        print('错误传参！仅限以下之一：金、木、水、火、土')
        return ''


class GanNode(object):
    def __init__(self, name, wx, yy, lu, yangren, wenchang, tianyi):
        self.name = name
        self.wuxing = wx                    # 五行
        self.yinyang = yy                   # 阴阳
        self.lu = lu                        # 禄
        self.ren = yangren                  # 刃
        self.xxss_wenchang = wenchang       # 文昌
        self.xxss_tianyi = tianyi           # 天乙


GAN_JIA = GanNode('甲', '木', '阳', '寅', '卯', '巳', ['丑', '未'])
GAN_YI = GanNode('乙', '木', '阴', '卯', '辰', '午', ['子', '申'])
GAN_BING = GanNode('丙', '火', '阳', '巳', '午', '申', ['亥', '酉'])
GAN_DING = GanNode('丁', '火', '阴', '午', '未', '酉', ['亥', '酉'])
GAN_WU = GanNode('戊', '土', '阳', '巳', '午', '申', ['丑', '未'])
GAN_JI = GanNode('己', '土', '阴', '午', '未', '酉', ['子', '申'])
GAN_GENG = GanNode('庚', '金', '阳', '申', '酉', '亥', ['丑', '未'])
GAN_XIN = GanNode('辛', '金', '阴', '酉', '戌', '子', ['寅', '午'])
GAN_REN = GanNode('壬', '水', '阳', '亥', '子', '寅', ['巳', '卯'])
GAN_GUI = GanNode('癸', '水', '阴', '子', '丑', '卯', ['巳', '卯'])

GAN_NODE = {
    '甲': GAN_JIA, '乙': GAN_YI, '丙': GAN_BING, '丁': GAN_DING, '戊': GAN_WU,
    '己': GAN_JI, '庚': GAN_GENG, '辛': GAN_XIN, '壬': GAN_REN, '癸': GAN_GUI
}


class ZhiNode(object):
    def __init__(self, name, wx, yy, cg, month, hour, ss, xxss_tiande, xxss_yuede, xxss_tianshe, xxss_jiangxing,
                 xxss_huagai, xxss_yima, xxss_taohua, xxss_guchen, xxss_guxiu, xxss_wangshen):
        self.name = name
        self.wuxing = wx                # 五行
        self.yinyang = yy               # 阴阳
        self.canggan = cg               # 藏干(本气、中气、余气)
        self.month = month              # 阴历月份
        self.hour = hour                # 北京时间, [1, 2] means [1:00, 3:00)
        self.shengxiao = ss             # 生肖
        self.xxss_tiande = xxss_tiande            # 天德
        self.xxss_yuede = xxss_yuede              # 月德
        self.xxss_tianshe = xxss_tianshe          # 天赦
        self.xxss_jiangxing = xxss_jiangxing      # 将星
        self.xxss_huagai = xxss_huagai            # 华盖
        self.xxss_yima = xxss_yima                # 驿马
        self.xxss_taohua = xxss_taohua            # 桃花
        self.xxss_guchen = xxss_guchen            # 孤辰
        self.xxss_guxiu = xxss_guxiu              # 孤宿
        self.xxss_wangshen = xxss_wangshen        # 亡神


ZHI_ZI = ZhiNode('子', '水', '阳', ['癸'], 11, [23, 0], '鼠', ['巳', '申'], '壬', '甲子', '子', '辰', '寅', '酉', '寅', '戌', '亥')
ZHI_CHOU = ZhiNode('丑', '土', '阴', ['己', '癸', '辛'], 12, [1, 2], '牛', ['乙', '庚'], '庚', '甲子', '酉', '丑', '亥', '午', '寅', '戌', '申')
ZHI_YIN = ZhiNode('寅', '木', '阳', ['甲', '丙', '戊'], 1, [3, 4], '虎', ['壬', '丁'], '丙', '戊寅', '午', '戌', '申', '卯', '巳', '丑', '巳')
ZHI_MAO = ZhiNode('卯', '木', '阴', ['乙'], 2,  [5, 6], '兔', ['巳', '申'], '甲', '戊寅', '卯', '未', '巳', '子', '巳', '丑', '寅')
ZHI_CHEN = ZhiNode('辰', '土', '阳', ['戊', '乙', '癸'], 3, [7, 8], '龙', ['壬', '丁'], '壬', '戊寅', '子', '辰', '寅', '酉', '巳', '丑', '亥')
ZHI_SI = ZhiNode('巳', '火', '阴', ['丙', '庚', '戊'], 4, [9, 10], '蛇', ['丙', '辛'], '庚', '甲午', '酉', '丑', '亥', '午', '申', '辰', '申')
ZHI_WU = ZhiNode('午', '火', '阳', ['丁', '己'], 5,  [11, 12], '马', ['寅', '亥'], '丙', '甲午', '午', '戌', '申', '卯', '申', '辰', '巳')
ZHI_WEI = ZhiNode('未', '土', '阴', ['己', '丁', '乙'], 6, [13, 14], '羊', ['甲', '己'], '甲', '甲午', '卯', '未', '巳', '子', '申', '辰', '寅')
ZHI_SHEN = ZhiNode('申', '金', '阳', ['庚', '壬', '戊'], 7, [15, 16], '猴', ['戊', '癸'], '壬', '戊申', '子', '辰', '寅', '酉', '亥', '未', '亥')
ZHI_YOU = ZhiNode('酉', '金', '阴', ['辛'], 8,  [17, 18], '鸡', ['寅', '亥'], '庚', '戊申', '酉', '丑', '亥', '午', '亥', '未', '申')
ZHI_XU = ZhiNode('戌', '土', '阳', ['戊', '辛', '丁'], 9, [19, 20], '狗', ['甲', '己'], '丙', '戊申', '午', '戌', '申', '卯', '亥', '未', '巳')
ZHI_HAI = ZhiNode('亥', '水', '阴', ['壬', '甲'], 10, [21, 22], '猪', ['乙', '庚'], '甲', '甲子', '卯', '未', '巳', '子', '寅', '戌', '寅')

ZHI_NODE = {
    '子': ZHI_ZI, '丑': ZHI_CHOU, '寅': ZHI_YIN, '卯': ZHI_MAO, '辰': ZHI_CHOU, '巳': ZHI_SI,
    '午': ZHI_WU, '未': ZHI_WEI, '申': ZHI_SHEN, '酉': ZHI_YOU, '戌': ZHI_XU, '亥': ZHI_HAI
}

SHENGXIAO = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
JIEQI = ['小寒', '大寒', '立春', '雨水', '惊蛰', '春分', '清明', '谷雨', '立夏', '小满', '芒种', '夏至',
         '小暑', '大暑', '立秋', '处暑', '白露', '秋分', '寒露', '霜降', '立冬', '小雪', '大雪', '冬至']

# 六十甲子
SIXTY_JIAZI = ['甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉', '甲戌', '乙亥',
               '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未', '甲申', '乙酉', '丙戌', '丁亥',
               '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳', '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥',
               '庚子', '辛丑', '壬寅', '癸卯', '甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥',
               '壬子', '癸丑', '甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥']

# 寄生十二宫
JISHENGSHIERGONG = {
    '甲木': {'亥': '长生', '子': '沐浴', '丑': '冠带', '寅': '临官', '卯': '帝旺', '辰': '衰',
             '巳': '病', '午': '死', '未': '墓', '申': '绝', '酉': '胎', '戌': '养'},
    '丙火': {'寅': '长生', '卯': '沐浴', '辰': '冠带', '巳': '临官', '午': '帝旺', '未': '衰',
             '申': '病', '酉': '死', '戌': '墓', '亥': '绝', '子': '胎', '丑': '养'},
    '戊土': {'寅': '长生', '卯': '沐浴', '辰': '冠带', '巳': '临官', '午': '帝旺', '未': '衰',
             '申': '病', '酉': '死', '戌': '墓', '亥': '绝', '子': '胎', '丑': '养'},
    '庚金': {'巳': '长生', '午': '沐浴', '未': '冠带', '申': '临官', '酉': '帝旺', '戌': '衰',
             '亥': '病', '子': '死', '丑': '墓', '寅': '绝', '卯': '胎', '辰': '养'},
    '壬水': {'申': '长生', '酉': '沐浴', '戌': '冠带', '亥': '临官', '子': '帝旺', '丑': '衰',
             '寅': '病', '卯': '死', '辰': '墓', '巳': '绝', '午': '胎', '未': '养'},
    '乙木': {'午': '长生', '巳': '沐浴', '辰': '冠带', '卯': '临官', '寅': '帝旺', '丑': '衰',
             '子': '病', '亥': '死', '戌': '墓', '酉': '绝', '申': '胎', '未': '养'},
    '丁火': {'酉': '长生', '申': '沐浴', '未': '冠带', '午': '临官', '巳': '帝旺', '辰': '衰',
             '卯': '病', '寅': '死', '丑': '墓', '子': '绝', '亥': '胎', '戌': '养'},
    '己土': {'酉': '长生', '申': '沐浴', '未': '冠带', '午': '临官', '巳': '帝旺', '辰': '衰',
             '卯': '病', '寅': '死', '丑': '墓', '子': '绝', '亥': '胎', '戌': '养'},
    '辛金': {'子': '长生', '亥': '沐浴', '戌': '冠带', '酉': '临官', '申': '帝旺', '未': '衰',
             '午': '病', '巳': '死', '辰': '墓', '卯': '绝', '寅': '胎', '丑': '养'},
    '癸水': {'卯': '长生', '寅': '沐浴', '丑': '冠带', '子': '临官', '亥': '帝旺', '戌': '衰',
             '酉': '病', '申': '死', '未': '墓', '午': '绝', '巳': '胎', '辰': '养'}
}

# 干支的刑冲害化合
XCHHH_XING_ZHI = [['子', '卯'], ['寅', '巳', '申'], ['丑', '未', '戌']]                   # 即三刑
XCHHH_CHONG_GAN = [['甲', '庚'], ['乙', '辛'], ['壬', '丙'], ['癸', '丁']]
XCHHH_CHONG_ZHI = [['子', '午'], ['丑', '未'], ['寅', '申'], ['卯', '酉'], ['辰', '戌'], ['巳', '亥']]    # 即六冲
XCHHH_HAI_ZHI = [['子', '未'], ['丑', '午'], ['寅', '巳'], ['卯', '辰'], ['申', '亥'], ['酉', '戌']]      # 即六害
XCHHH_HUA_GAN = [['甲', '己'], ['乙', '庚'], ['丙', '辛'], ['壬', '丁'],  ['癸', '戊']]    # 即五化
XCHHH_HE_ZHI_6 = {('子', '丑'): '土', ('寅', '亥'): '木', ('卯', '戌'): '火',
                  ('辰', '酉'): '金', ('巳', '申'): '水', ('午', '未'): '太阳太阴'}         # 即六合
XCHHH_HE_ZHI_3 = {('子', '申', '辰'): '水', ('亥', '卯', '未'): '木',
                  ('寅', '午', '戌'): '火', ('巳', '酉', '丑'): '金'}                     # 即三合

# 属相的刑冲害化合
XCHHH_HE_SX_6 = [['鼠', '牛'], ['虎', '猪'], ['土', '狗'], ['龙', '鸡'], ['蛇', '猴'], ['马', '羊']]
XCHHH_HE_SX_3 = [['鼠', '猴', '龙'], ['猪', '土', '羊'], ['虎', '马', '狗'], ['蛇', '鸡', '牛']]
XCHHH_CHONG_SX = [['鼠', '马'], ['牛', '羊'], ['虎', '猴'], ['土', '鸡'], ['龙', '狗'], ['蛇', '猪']]
XCHHH_HAI_SX = [['鼠', '羊'], ['牛', '马'], ['虎', '蛇'], ['土', '龙'], ['猴', '猪'], ['鸡', '狗']]
