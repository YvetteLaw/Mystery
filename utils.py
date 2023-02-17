# http://www.cdyszyxy.cn/jingdian/358335.html

import datetime
import numpy as np
import pandas as pd
import zhdate
from wuxing import *


def transfer_lunar_to_dt(year, month, day, if_leap_month=False):
    lunar_date = zhdate.ZhDate(year, month, day, leap_month=if_leap_month)  # leap_month为闰月出生
    dt_date = lunar_date.to_datetime()
    return dt_date.year, dt_date.month, dt_date.day


def transfer_dt_to_lunar(year, month, day):
    dt_date = datetime.datetime(year, month, day)
    ln_date = zhdate.ZhDate.from_datetime(dt_date)
    return ln_date.lunar_year, ln_date.lunar_month, ln_date.lunar_day


def cal_gz_year(nl_year):
    year = nl_year - 3 - 1  # 农历年份减3（补减1）
    return TIANGAN[year % 10] + DIZHI[year % 12]


def cal_jieqi(dt):  # 返回农历节气

    def cal_julian_day_of_year(year, st):  # 返回指定年份的节气的儒略日数
        if st < 0 or st > 24:
            return 0.0

        s_stAccInfo = [
            0.00, 1272494.40, 2548020.60, 3830143.80, 5120226.60, 6420865.80,
            7732018.80, 9055272.60, 10388958.00, 11733065.40, 13084292.40, 14441592.00,
            15800560.80, 17159347.20, 18513766.20, 19862002.20, 21201005.40, 22529659.80,
            23846845.20, 25152606.00, 26447687.40, 27733451.40, 29011921.20, 30285477.60]
        base1900_SlightColdJD = 2415025.5868055555  # 已知1900年小寒时刻为1月6日02:05:00
        stJd = 365.24219878 * (year - 1900) + s_stAccInfo[st] / 86400.0
        return base1900_SlightColdJD + stJd

    # 计算儒略日
    year, month, day = dt.year, dt.month, dt.day
    if month <= 2:
        month += 12
        year -= 1

    b = 2 - year / 100 + year / 400
    dd = day + 0.5000115740  # 本日12:00后才是儒略日的开始(过一秒钟)
    rulian_day = int(365.25 * (year + 4716) + 0.01) + int(30.60001 * (month + 1)) + dd + b - 1524.5

    for i in range(24):
        delta = rulian_day - cal_julian_day_of_year(year, i)
        if -.5 <= delta <= .5:  # 因为两个都是浮点数，不能用相等表示
            return [JIEQI[i], True] if i % 2 == 0 else [JIEQI[i], False]
    return "", None


def cal_gz_month(year, month, day, nl_year, nl_month, gz_year):  # 返回干支纪月
    """
    1、首先判断当前日期所处的节气范围。特别要考虑年数是否需要增减，以立春为界，如正月尚未立春的日子年数减一
    2、月的天干公式为（年干序号 * 2 + 月数） % 10，其中 0 表示最后一个天干
    3、月的地支是固定的。
    """
    JIEQI_MONTH = {
        "立春": [0, "寅"], "惊蛰": [1, "卯"], "清明": [2, "辰"], "立夏": [3, "巳"],
        "芒种": [4, "午"], "小暑": [5, "未"], "立秋": [6, "申"], "白露": [7, "酉"],
        "寒露": [8, "戌"], "立冬": [9, "亥"], "大雪": [10, "子"], "小寒": [11, "丑"]
    }
    dt = datetime.datetime(year, month, day)
    jie_qi, flag = cal_jieqi(dt)

    if len(jie_qi) > 0 and flag:    # 如果恰好是节气当日
        if JIEQI_MONTH[jie_qi][0] == 0 and nl_month == 12:
            nl_year, nl_month = TIANGAN[(nl_year - 3) % 10] + DIZHI[(nl_year - 3) % 12], 0
        else:
            nl_year, nl_month = gz_year, JIEQI_MONTH[jie_qi][0]
    else:                           # 循环判断后一个节气是什么
        nl_year, nl_month = gz_year, 0
        for i in range(-1, -40, -1):
            var_days = dt + datetime.timedelta(days=i)
            jie_qi, flag = cal_jieqi(var_days)
            if len(jie_qi) > 0 and flag:
                if JIEQI_MONTH[jie_qi][0] > 0:
                    nl_month = JIEQI_MONTH[jie_qi][0]
                elif JIEQI_MONTH[jie_qi][0] == 0 and nl_month == 12:
                    nl_year = TIANGAN[(nl_year - 3) % 10] + DIZHI[(nl_year - 3) % 12]
                break
    month_num = (TIANGAN.index(nl_year[0]) + 1) * 2 + nl_month + 1
    m = 10 if month_num % 10 == 0 else month_num % 10
    return TIANGAN[m - 1] + JIEQI_MONTH[jie_qi][1]


def cal_gz_day(year, month, day):  # 返回干支纪日
    c, y = divmod(year, 100)
    y = y - 1 if month == 1 or month == 2 else y
    m = month + 12 if month == 1 or month == 2 else month  # 取月份（若为1、2月则分别按13、14来计算）
    i = 0 if month % 2 == 1 else 6  # 取i(奇数月0，偶数月6)
    g = 4 * c + c // 4 + 5 * y + y // 4 + 3 * (m + 1) // 5 + day - 3 - 1
    z = 8 * c + c // 4 + 5 * y + y // 4 + 3 * (m + 1) // 5 + day + 7 + i - 1
    return TIANGAN[g % 10] + DIZHI[z % 12]


def cal_gz_hour(hour, gz_day):  # 返回干支纪时
    # 时干数 = ((日干 % 5)*2 + 时辰 -2) % 10
    z = round((hour / 2) + 0.1) % 12  # 加0.1因为round的bug
    gz_day_yu = (TIANGAN.index(gz_day[0]) + 1) % 5
    if gz_day_yu == 0:
        gz_day_yu = 5
    gz_hour_num = (gz_day_yu * 2 - 1 + (z + 1) - 1) % 10
    if gz_hour_num == 0:
        gz_hour_num = 10
    return TIANGAN[gz_hour_num - 1] + DIZHI[z]


def get_shishen(gan_node, rizhu_node):
    link = WuxingLink()
    if gan_node.wuxing == link.who_improve_me(rizhu_node.wuxing):
        res = '正印' if gan_node.yinyang != rizhu_node.yinyang else '偏印'
    elif gan_node.wuxing == link.who_impair_me(rizhu_node.wuxing):
        res = '正官' if gan_node.yinyang != rizhu_node.yinyang else '七杀'
    elif gan_node.wuxing == link.me_improve_who(rizhu_node.wuxing):
        res = '伤官' if gan_node.yinyang != rizhu_node.yinyang else '食神'
    elif gan_node.wuxing == link.me_impair_who(rizhu_node.wuxing):
        res = '正财' if gan_node.yinyang != rizhu_node.yinyang else '偏财'
    else:
        res = '劫财' if gan_node.yinyang != rizhu_node.yinyang else '比肩'
    del link
    return res


def cal_wx_intensity(bazi, rigan, base):
    # ref: https://www.buyiju.com/bzzs/qufa.html

    GAN_MONTH_INTENSITY_TABLE = {
        '月支': ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'],
        '甲': [1.14, 1.2, 1.1, 1, 1, 1.04, 1.06, 1, 1, 1.2, 1.2, 1.06],
        '乙': [1.14, 1.2, 1.1, 1, 1, 1.04, 1.06, 1, 1, 1.2, 1.2, 1.06],
        '丙': [1.2, 1.2, 1.06, 1.14, 1.2, 1.1, 1, 1, 1.04, 1, 1, 1],
        '丁': [1.2, 1.2, 1.06, 1.14, 1.2, 1.1, 1, 1, 1.04, 1, 1, 1],
        '戊': [1.06, 1, 1.1, 1.14, 1.2, 1.16, 1, 1, 1.14, 1, 1, 1.1],
        '己': [1.06, 1, 1.1, 1.14, 1.2, 1.16, 1, 1, 1.14, 1, 1, 1.1],
        '庚': [1, 1, 1.1, 1.06, 1, 1.1, 1.14, 1.2, 1.16, 1, 1, 1.14],
        '辛': [1, 1, 1.1, 1.06, 1, 1.1, 1.14, 1.2, 1.16, 1, 1, 1.14],
        '壬': [1, 1, 1.04, 1.06, 1, 1, 1.2, 1.2, 1.06, 1.14, 1.2, 1.1],
        '癸': [1, 1, 1.04, 1.06, 1, 1, 1.2, 1.2, 1.06, 1.14, 1.2, 1.1]
    }
    ZHI_MONTH_INTENSITY_TABLE = {
        '月支': ['藏干', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'],
        '子': ['癸', 1, 1, 1.04, 1.06, 1, 1, 1.2, 1.2, 1.06, 1.14, 1.2, 1.1],
        '丑': [['癸', 0.3, 0.3, 0.312, 0.318, 0.3, 0.3, 0.36, 0.36, 0.318, 0.342, 0.36, 0.33],
               ['辛', 0.2, 0.2, 0.23, 0.212, 0.2, 0.22, 0.228, 0.248, 0.232, 0.2, 0.2, 0.228],
               ['己', 0.53, 0.5, 0.55, 0.57, 0.6, 0.58, 0.5, 0.5, 0.57, 0.5, 0.5, 0.55]],
        '寅': [['丙', 0.36, 0.36, 0.318, 0.342, 0.36, 0.33, 0.3, 0.3, 0.342, 0.318, 0.3, 0.3],
               ['甲', 0.798, 0.84, 0.77, 0.7, 0.7, 0.728, 0.742, 0.7, 0.7, 0.84, 0.84, 0.742]],
        '卯': ['乙', 1.14, 1.2, 1.1, 1, 1, 1.04, 1.06, 1, 1, 1.2, 1.2, 1.06],
        '辰': [['乙', 0.342, 0.36, 0.33, 0.3, 0.3, 0.312, 0.318, 0.3, 0.3, 0.36, 0.36, 0.318],
               ['癸', 0.2, 0.2, 0.208, 0.2, 0.2, 0.2, 0.24, 0.24, 0.212, 0.228, 0.24, 0.22],
               ['戊', 0.53, 0.5, 0.55, 0.6, 0.6, 0.58, 0.5, 0.5, 0.57, 0.5, 0.5, 0.55]],
        '巳': [['庚', 0.3, 0.3, 0.33, 0.3, 0.3, 0.33, 0.342, 0.36, 0.348, 0.3, 0.3, 0.342],
               ['丙', 0.84, 0.84, 0.742, 0.84, 0.84, 0.798, 0.7, 0.7, 0.728, 0.742, 0.7, 0.7]],
        '午': ['丁', 1.2, 1.2, 1.06, 1.14, 1.2, 1.1, 1, 1, 1.04, 1.06, 1, 1],
        '未': [['丁', 0.36, 0.36, 0.318, 0.342, 0.36, 0.33, 0.3, 0.3, 0.312, 0.318, 0.318, 0.3, 0.3],
               ['乙', 0.228, 0.24, 0.22, 0.2, 0.2, 0.208, 0.212, 0.2, 0.2, 0.24, 0.24, 0.212],
               ['己', 0.53, 0.5, 0.55, 0.57, 0.6, 0.58, 0.5, 0.5, 0.57, 0.5, 0.5, 0.55]],
        '申': [['壬', 0.3, 0.3, 0.312, 0.318, 0.3, 0.3, 0.36, 0.36, 0.318, 0.342, 0.36, 0.33],
               ['庚', 0.7, 0.7, 0.77, 0.742, 0.7, 0.77, 0.798, 0.84, 0.812, 0.7, 0.7, 0.798]],
        '酉': ['辛', 1, 1, 1.1, 1.06, 1, 1.1, 1.14, 1.2, 1.16, 1, 1, 1.14],
        '戌': [['辛', 0.3, 0.3, 0.33, 0.318, 0.3, 0.33, 0.342, 0.36, 0.348, 0.3, 0.3, 0.342],
               ['丁', 0.24, 0.24, 0.212, 0.228, 0.24, 0.22, 0.2, 0.2, 0.208, 0.212, 0.2, 0.2],
               ['戊', 0.53, 0.5, 0.55, 0.57, 0.6, 0.58, 0.5, 0.5, 0.57, 0.5, 0.5, 0.55]],
        '亥': [['甲', 0.342, 0.36, 0.33, 0.3, 0.3, 0.312, 0.318, 0.3, 0.3, 0.36, 0.36, 0.318],
               ['壬', 0.7, 0.7, 0.728, 0.742, 0.7, 0.7, 0.84, 0.84, 0.724, 0.798, 0.84, 0.77]]
    }

    def get_gan_month_intensity(gan):
        df = pd.DataFrame(GAN_MONTH_INTENSITY_TABLE)
        df.index = df['月支']
        return df.at[base, gan]

    def get_zhi_month_intensity(zhi):
        df = pd.DataFrame(ZHI_MONTH_INTENSITY_TABLE[zhi])
        df.set_index = ([pd.Index(ZHI_MONTH_INTENSITY_TABLE['月支']), '月支'])
        canggan = df.loc[:, 0]
        if canggan.shape[0] == 13:  # 单藏干
            return {canggan[0]: canggan[ZHI_NODE[base].month]}
        else:
            return dict(zip(canggan, df.loc[:, ZHI_NODE[base].month]))

    # 以月支来计算五行强度
    attr_map = {'水': 0, '火': 1, '木': 2, '土': 3, '金': 4}
    attr_values = [0. for _ in range(5)]
    for i in range(0, 8, 2):
        gan = bazi[i]
        gan_it = get_gan_month_intensity(gan)
        attr_values[attr_map[GAN_NODE[gan].wuxing]] += gan_it
    for i in range(1, 8, 2):
        zhi = bazi[i]
        cg_it_list = get_zhi_month_intensity(zhi)
        for cg, cg_it in cg_it_list.items():
            attr_values[attr_map[GAN_NODE[cg].wuxing]] += cg_it
    v_wx_it = {}
    for attr, idx in attr_map.items():
        v_wx_it[attr] = attr_values[idx]

    # cal category intensity
    link = WuxingLink()
    same_category = [rigan.wuxing, link.who_improve_me(rigan.wuxing)]
    diff_category = [link.who_impair_me(rigan.wuxing), link.me_impair_who(rigan.wuxing),
                     link.me_improve_who(rigan.wuxing)]

    v_same_category = v_diff_category = 0
    for k, v in v_wx_it.items():
        if k in same_category:
            v_same_category += v
        else:
            v_diff_category += v
    v_wx_it['同类'] = [same_category, v_same_category]
    v_wx_it['异类'] = [diff_category, v_diff_category]
    return v_wx_it


# TODO: used for yongshen, but how to model?
def relation_matrix():
    '''
        金  木  水   火  土  (base)
    金      -   +   +   -
    木  +       -   +   -
    水  -   +       -   +
    火  -   -   +       +
    土  +   +   -   -
    '''
    wx_relation_matrix = [[0, -1, 1, 1, -1],
                          [1, 0, -1, 1, -1],
                          [-1, 1, 0, -1, 1],
                          [-1, -1, 1, 0, 1],
                          [1, 1, -1, -1, 0]]

    wx = [1, 2, 0, 3, 2]  # [金，木，水，火，土]

    a = np.array(wx_relation_matrix)
    m = np.empty(shape=[0, 5])
    for i in range(5):
        s = a[i, :] * wx[i]
        m = np.vstack((m, s))

    m = np.array([wx] * 5) + m
    return m


def get_mingge(bazi, shishen, rigan):

    def check_exist(cg):
        if cg in bazi[0][0]:
            return shishen[0]
        elif cg in bazi[1][0]:
            return shishen[2]
        elif cg in bazi[3][0]:
            return shishen[5]
        else:
            return ''

    canggan = ZHI_NODE[bazi[1][1]].canggan
    biange_table = [rigan.name, GAN_NODE[rigan.name].lu, GAN_NODE[rigan.name].ren]
    for i in range(len(canggan)):
        res = check_exist(canggan[i])
        if res != '' and canggan[i] not in biange_table:
            return res
        if len(canggan) == 1:
            return shishen[3]

    return get_shishen(GAN_NODE[canggan[0]], rigan)


def get_dayun_ages(year, month, day, bazi, gender):
    # https://www.zhihu.com/search?type=content&q=%E5%A6%82%E4%BD%95%E6%8E%92%E5%A4%A7%E8%BF%90

    def find_next_jieqi(order):
        dt = datetime.datetime(year, month, day)
        jie_qi, flag = cal_jieqi(dt)

        # 若是节气当日
        if len(jie_qi) > 0 and flag:
            return 0

        # 寻找临近节
        if order > 0:
            for i in range(1, 40, 1):
                var_days = dt + datetime.timedelta(days=i)
                jie_qi, flag = cal_jieqi(var_days)
                if len(jie_qi) > 0 and flag:
                    return i
        else:
            for i in range(-1, -40, -1):
                var_days = dt + datetime.timedelta(days=i)
                jie_qi, flag = cal_jieqi(var_days)
                if len(jie_qi) > 0 and flag:
                    return abs(i)

    dayun_ages = {}
    start_id = SIXTY_JIAZI.index(bazi[1])
    if (bazi[0][1] == '阳' and gender == 'male') or (bazi[0][1] == '阴' and gender == 'female'):  # 阳年生男，阴年生女
        delta_days = find_next_jieqi(1)
        start_age = delta_days // 3
        for i in range(8):
            dayun_ages[start_age + i * 10] = SIXTY_JIAZI[start_id + i + 1]
    else:  # 阳年生女，阴年生男
        delta_days = find_next_jieqi(-1)
        start_age = delta_days // 3
        for i in range(8):
            dayun_ages[start_age + i * 10] = SIXTY_JIAZI[start_id - i - 1]
    return dayun_ages


def check_xingxiushensha(bazi):
    xxss = []
    three_dizhi = [bazi[0][1], bazi[1][1], bazi[3][1]]

    m = [bazi[2][0], bazi[2][1], bazi[3][0], bazi[3][1]]
    v = ZHI_NODE[bazi[1][1]].xxss_tiande
    if v[0] in m or v[1] in m:
        xxss.append("天德贵人")

    if ZHI_NODE[bazi[1][1]].xxss_yuede == bazi[2][0]:
        xxss.append("月德贵人")

    v = GAN_NODE[bazi[2][0]].xxss_tianyi
    if v[0] in three_dizhi or v[1] in three_dizhi:
        xxss.append("天乙贵人")

    if ZHI_NODE[bazi[1][1]].xxss_tianshe == bazi[2]:
        xxss.append("天赦星")

    if GAN_NODE[bazi[2][0]].xxss_wenchang in three_dizhi:
        xxss.append("文昌星")

    if ZHI_NODE[bazi[2][1]].xxss_jiangxing in three_dizhi:
        xxss.append("将星")

    if ZHI_NODE[bazi[2][1]].xxss_huagai in three_dizhi:
        xxss.append("华盖星")

    if ZHI_NODE[bazi[2][1]].xxss_yima in three_dizhi:
        xxss.append("驿马星")

    v = ZHI_NODE[bazi[2][1]].xxss_taohua
    if v == bazi[0][1] or v == bazi[1][1]:
        xxss.append("桃花煞（墙里）")
    if v == bazi[3][1]:
        xxss.append("桃花煞（墙外）")

    if ZHI_NODE[bazi[0][1]].xxss_guchen in [bazi[1][1], bazi[2][1], bazi[3][1]]:
        xxss.append("孤辰")

    if ZHI_NODE[bazi[0][1]].xxss_guxiu in [bazi[1][1], bazi[2][1], bazi[3][1]]:
        xxss.append("孤宿")

    if ZHI_NODE[bazi[2][1]].xxss_wangshen in three_dizhi:
        xxss.append("亡神")

    # 禄
    lu = GAN_NODE[bazi[2][0]].lu
    if bazi[0][1] == lu:
        xxss.append("岁禄")
    if bazi[1][1] == lu:
        xxss.append("建禄")
    if bazi[2][1] == lu:
        xxss.append("坐禄")
    if bazi[3][1] == lu:
        xxss.append("归禄")

    # 羊刃
    yangren = GAN_NODE[bazi[2][0]].ren
    if bazi[0][1] == yangren:
        xxss.append("羊刃（年支）")
    if bazi[1][1] == yangren:
        xxss.append("羊刃（月支）")
    if bazi[2][1] == yangren:
        xxss.append("羊刃（日支）")
    if bazi[3][1] == yangren:
        xxss.append("羊刃（时支）")

    # 三奇
    three_tiangan = [bazi[0][0], bazi[1][0], bazi[2][0]]
    if three_tiangan == ['甲', '戊', '庚']:
        xxss.append("天上三奇")
    elif three_tiangan == ['乙', '丙', '丁']:
        xxss.append("地上三奇")
    elif three_tiangan == ['壬', '癸', '辛']:
        xxss.append("人中三奇")

    # 魁罡
    if bazi[2] == "戊戌" or bazi[2] == "庚戌":
        xxss.append("天罡")
    if bazi[2] == "庚辰" or bazi[2] == "壬辰":
        xxss.append("地罡")

    # 十恶大败
    XXSS_SHIEDABAI_TABLE = {'庚戌': '甲辰', '辛亥': '乙巳', '壬寅': '丙申', '癸巳': '丁亥', '甲戌': '庚辰',
                            '甲辰': '戊戌', '乙亥': '辛巳', '乙未': '己丑', '丙寅': '壬申', '丁巳': '癸亥'}
    if XXSS_SHIEDABAI_TABLE[bazi[0]] == bazi[2]:
        xxss.append("十恶大败")

    # 六甲空亡
    xun = SIXTY_JIAZI.index(bazi[2]) // 10
    if DIZHI[10 - 2 * xun] in three_dizhi or DIZHI[11 - 2 * xun] in three_dizhi:
        xxss.append("空亡")

    return xxss


if __name__ == '__main__':
    print(0)
