"""
ref: http://www.cdyszyxy.cn/jingdian/358335.html
"""

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
    lunar_date = zhdate.ZhDate.from_datetime(dt_date)
    return lunar_date.lunar_year, lunar_date.lunar_month, lunar_date.lunar_day


def cal_gz_year(nl_year):  # 返回干支纪年
    year = nl_year - 3 - 1  # 农历年份减3 （说明：补减1）
    G = year % 10  # 模10，得到天干数
    Z = year % 12  # 模12，得到地支数
    return TIANGAN[G] + DIZHI[Z]


def cal_jieqi(dt):  # 返回农历节气
    def cal_rulian_day(dt):
        year = dt.year
        month = dt.month
        day = dt.day
        if month <= 2:
            month += 12
            year -= 1

        B = year / 100
        B = 2 - B + year / 400

        dd = day + 0.5000115740  # 本日12:00后才是儒略日的开始(过一秒钟)*/
        return int(365.25 * (year + 4716) + 0.01) + int(30.60001 * (month + 1)) + dd + B - 1524.5

    def cal_julian_day_of_ln_jie(year, st):  # 返回指定年份的节气的儒略日数
        s_stAccInfo = [
            0.00, 1272494.40, 2548020.60, 3830143.80, 5120226.60, 6420865.80,
            7732018.80, 9055272.60, 10388958.00, 11733065.40, 13084292.40, 14441592.00,
            15800560.80, 17159347.20, 18513766.20, 19862002.20, 21201005.40, 22529659.80,
            23846845.20, 25152606.00, 26447687.40, 27733451.40, 29011921.20, 30285477.60]

        # 已知1900年小寒时刻为1月6日02:05:00
        base1900_SlightColdJD = 2415025.5868055555

        if (st < 0) or (st > 24):
            return 0.0

        stJd = 365.24219878 * (year - 1900) + s_stAccInfo[st] / 86400.0
        return base1900_SlightColdJD + stJd

    for i in range(24):
        delta = cal_rulian_day(dt) - cal_julian_day_of_ln_jie(dt.year, i)
        if -.5 <= delta <= .5:     # 因为两个都是浮点数，不能用相等表示
            return JIEQI[i * 2:(i + 1) * 2]
    return ""


def cal_gz_month(year, month, day, nl_year, nl_month, gz_year):  # 返回干支纪月
    """
    干支纪月的计算规则较为复杂，是本人在前人的基础上实现的，填补了空白。
    1、首先判断当前日期所处的节气范围，
    2、特别要考虑年数是否需要增减，以立春为界，如正月尚未立春的日子年数减一，
    3、月的天干公式 （年干序号 * 2 + 月数） % 10 ，其中 0 表示最后一个天干，
    4、月的地支是固定的，查表可得。
    """
    dt = datetime.datetime(year, month, day)
    jie_qi = cal_jieqi(dt)

    def _at_jieqi_day(nl_year):
        year = nl_year - 3  # 虽然农历已经是腊月，但是已经立春， 所以年加一
        G = year % 10  # 模10，得到天干数
        Z = year % 12  # 模12，得到地支数
        nl_year = TIANGAN[G] + DIZHI[Z]
        nl_month = 0
        return nl_year, nl_month

    if len(jie_qi) > 0 and jie_qi in JIEQI_JIE:   # 如果恰好是节气当日
        if JIEQI_MONTH[jie_qi][0] == 0 and nl_month == 12:
            nl_year, nl_month = _at_jieqi_day(nl_year)
        else:
            nl_year = gz_year  # 干支纪年
            nl_month = JIEQI_MONTH[jie_qi][0]  # 计算出干支纪月
    else:      # 如果不是节气日，则循环判断后一个分月节气是什么
        nl_year = gz_year
        nl_month = 0
        for i in range(-1, -40, -1):
            var_days = dt + datetime.timedelta(days=i)
            jie_qi = cal_jieqi(var_days)
            if len(jie_qi) > 0 and jie_qi in JIEQI_JIE:
                if JIEQI_MONTH[jie_qi][0] > 0:
                    nl_month = JIEQI_MONTH[jie_qi][0]
                elif JIEQI_MONTH[jie_qi][0] == 0 and nl_month == 12:
                    nl_year, nl_month = _at_jieqi_day(nl_year)
                else:
                    nl_month = 0
                break
    gan_str = TIANGAN
    month_num = (gan_str.find(nl_year[0])+1) * 2 + nl_month + 1
    M = month_num % 10
    if M == 0:
        M = 10
    return TIANGAN[M-1] + JIEQI_MONTH[jie_qi][1]


def cal_gz_day(year, month, day):  # 返回干支纪日
    C = year // 100  # 取世纪数，减一
    y = year % 100  # 取年份后两位（若为1月、2月则当前年份减一）
    y = y - 1 if month == 1 or month == 2 else y
    M = month  # 取月份（若为1月、2月则分别按13、14来计算）
    M = M + 12 if month == 1 or month == 2 else M
    d = day  # 取日数
    i = 0 if month % 2 == 1 else 6  # 取i （奇数月i=0，偶数月i=6）

    # 下面两个是网上的公式
    # http://baike.baidu.com/link?url=MbTKmhrTHTOAz735gi37tEtwd29zqE9GJ92cZQZd0X8uFO5XgmyMKQru6aetzcGadqekzKd3nZHVS99rewya6q
    # 计算干（说明：补减1）
    G = 4 * C + C // 4 + 5 * y + y // 4 + 3 * (M + 1) // 5 + d - 3 - 1
    G = G % 10
    # 计算支（说明：补减1）
    Z = 8 * C + C // 4 + 5 * y + y // 4 + 3 * (M + 1) // 5 + d + 7 + i - 1
    Z = Z % 12
    return TIANGAN[G] + DIZHI[Z]


def cal_gz_hour(hour, gz_day):  # 返回干支纪时（时辰）
    """
    时干数 = ((日干 % 5)*2 + 时辰 -2) % 10
    """
    # 计算支
    Z = round((hour / 2) + 0.1) % 12  # 之所以加0.1是因为round的bug!!
    gz_day_num = TIANGAN.find(gz_day[0]) + 1
    gz_day_yu = gz_day_num % 5
    hour_num = Z + 1
    if gz_day_yu == 0:
        gz_day_yu = 5
    gz_hour_num = (gz_day_yu * 2 - 1 + hour_num-1) % 10
    if gz_hour_num == 0:
        gz_hour_num = 10
    return TIANGAN[gz_hour_num-1] + DIZHI[Z]


def get_shishen(wuxing, rizhu):
    attr, yy = wuxing
    _, rz_attr, rz_yy = rizhu

    link = WuXingLink()
    if attr == link.who_improve_me(rz_attr):
        res = '正印' if yy != rz_yy else '偏印'
    elif attr == link.who_impair_me(rz_attr):
        res = '正官' if yy != rz_yy else '七杀'
    elif attr == link.me_improve_who(rz_attr):
        res = '伤官' if yy != rz_yy else '食神'
    elif attr == link.me_impair_who(rz_attr):
        res = '正财' if yy != rz_yy else '偏财'
    else:
        res = '劫财' if yy != rz_yy else '比肩'
    del link
    return res


def cal_wx_intensity(bazi, base):
    # ref: https://www.buyiju.com/bzzs/qufa.html

    def get_gan_month_intensity(gan):
        df = pd.DataFrame(GAN_MONTH_INTENSITY_TABLE)
        df.index = df['月支']
        return df.at[base, gan]

    def get_zhi_month_intensity(zhi):
        df = pd.DataFrame(ZHI_MONTH_INTENSITY_TABLE[zhi])
        df.set_index = ([pd.Index(ZHI_MONTH_INTENSITY_TABLE['月支']), '月支'])

        canggan = df.loc[:, 0]
        if canggan.shape[0] == 13:        # 单藏干
            return {canggan[0]: canggan[LUNAR_MONTH_ZHI_2_NUM[base]]}
        else:
            return dict(zip(canggan, df.loc[:, LUNAR_MONTH_ZHI_2_NUM[base]]))

    day_gan = bazi[4]

    attr_map = {'水': 0, '火': 1, '木': 2, '土': 3, '金': 4}
    attr_values = [0. for i in range(5)]
    for i in range(0, 8, 2):
        gan = bazi[i]
        gan_attr = GAN_2_WX_YY[gan][0]
        gan_it = get_gan_month_intensity(gan)
        attr_values[attr_map[gan_attr]] += gan_it
    for i in range(1, 8, 2):
        zhi = bazi[i]
        zhi_it = get_zhi_month_intensity(zhi)
        for k, v in zhi_it.items():
            k_attr = GAN_2_WX_YY[k][0]
            attr_values[attr_map[k_attr]] += v
    v_wx_it = {}
    for attr, idx in attr_map.items():
        v_wx_it[attr] = attr_values[idx]

    # cal category intensity
    day_gan_attr = GAN_2_WX_YY[day_gan][0]
    link = WuXingLink()
    same_category = [day_gan_attr, link.who_improve_me(day_gan_attr)]
    diff_category = [link.who_impair_me(day_gan_attr), link.me_impair_who(day_gan_attr),
                     link.me_improve_who(day_gan_attr)]
    del link
    v_same_category = v_diff_category = 0
    for k, v in v_wx_it.items():
        if k in same_category:
            v_same_category += v
        else:
            v_diff_category += v
    v_wx_it['同类'] = [same_category, v_same_category]
    v_wx_it['异类'] = [diff_category, v_diff_category]
    return v_wx_it


def relation_matrix():
    '''
        金  木  水   火  土  (base)
    金      -   +   +   -
    木  +       -   +   -
    水  -   +       -   +
    火  -   -   +       +
    土  +   +   -   -
    '''
    WX_RELATION_MATRIX = [[0, -1, 1, 1, -1],
                          [1, 0, -1, 1, -1],
                          [-1, 1, 0, -1, 1],
                          [-1, -1, 1, 0, 1],
                          [1, 1, -1, -1, 0]]

    wx = [1, 2, 0, 3, 2]  # [金，木，水，火，土]

    A = np.array(WX_RELATION_MATRIX)
    M = np.empty(shape=[0, 5])
    for i in range(5):
        m = A[i, :] * wx[i]
        M = np.vstack((M, m))

    M = np.array([wx] * 5) + M
    return M



if __name__ == '__main__':
    print(transfer_lunar_to_dt(1994, 5, 4))
    print(transfer_dt_to_lunar(1994, 6, 12))
    print(0)
