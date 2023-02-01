"""
ref: http://www.cdyszyxy.cn/jingdian/358335.html
"""

import datetime

# 数组LunarMonthDay存入阴历1901年到2050年每年中的月天数信息。阴历每月只能是29或30天，一年用12（或13）个二进制位表示，对应位为1表30天，否则为29天。
LunarMonthDay = [
    0x4ae0, 0xa570, 0x5268, 0xd260, 0xd950, 0x6aa8, 0x56a0, 0x9ad0, 0x4ae8, 0x4ae0,  # 1910
    0xa4d8, 0xa4d0, 0xd250, 0xd548, 0xb550, 0x56a0, 0x96d0, 0x95b0, 0x49b8, 0x49b0,  # 1920
    0xa4b0, 0xb258, 0x6a50, 0x6d40, 0xada8, 0x2b60, 0x9570, 0x4978, 0x4970, 0x64b0,  # 1930
    0xd4a0, 0xea50, 0x6d48, 0x5ad0, 0x2b60, 0x9370, 0x92e0, 0xc968, 0xc950, 0xd4a0,  # 1940
    0xda50, 0xb550, 0x56a0, 0xaad8, 0x25d0, 0x92d0, 0xc958, 0xa950, 0xb4a8, 0x6ca0,  # 1950
    0xb550, 0x55a8, 0x4da0, 0xa5b0, 0x52b8, 0x52b0, 0xa950, 0xe950, 0x6aa0, 0xad50,  # 1960
    0xab50, 0x4b60, 0xa570, 0xa570, 0x5260, 0xe930, 0xd950, 0x5aa8, 0x56a0, 0x96d0,  # 1970
    0x4ae8, 0x4ad0, 0xa4d0, 0xd268, 0xd250, 0xd528, 0xb540, 0xb6a0, 0x96d0, 0x95b0,  # 1980
    0x49b0, 0xa4b8, 0xa4b0, 0xb258, 0x6a50, 0x6d40, 0xada0, 0xab60, 0x9370, 0x4978,  # 1990
    0x4970, 0x64b0, 0x6a50, 0xea50, 0x6b28, 0x5ac0, 0xab60, 0x9368, 0x92e0, 0xc960,  # 2000
    0xd4a8, 0xd4a0, 0xda50, 0x5aa8, 0x56a0, 0xaad8, 0x25d0, 0x92d0, 0xc958, 0xa950,  # 2010
    0xb4a0, 0xb550, 0xb550, 0x55a8, 0x4ba0, 0xa5b0, 0x52b8, 0x52b0, 0xa930, 0x74a8,  # 2020
    0x6aa0, 0xad50, 0x4da8, 0x4b60, 0x9570, 0xa4e0, 0xd260, 0xe930, 0xd530, 0x5aa0,  # 2030
    0x6b50, 0x96d0, 0x4ae8, 0x4ad0, 0xa4d0, 0xd258, 0xd250, 0xd520, 0xdaa0, 0xb5a0,  # 2040
    0x56d0, 0x4ad8, 0x49b0, 0xa4b8, 0xa4b0, 0xaa50, 0xb528, 0x6d20, 0xada0, 0x55b0,  # 2050
]

# 数组LunarMonth存放阴历1901年到2050年闰月的月份，如没有则为0，每字节存两年。
LunarMonth = [
    0x00, 0x50, 0x04, 0x00, 0x20,  # 1910
    0x60, 0x05, 0x00, 0x20, 0x70,  # 1920
    0x05, 0x00, 0x40, 0x02, 0x06,  # 1930
    0x00, 0x50, 0x03, 0x07, 0x00,  # 1940
    0x60, 0x04, 0x00, 0x20, 0x70,  # 1950
    0x05, 0x00, 0x30, 0x80, 0x06,  # 1960
    0x00, 0x40, 0x03, 0x07, 0x00,  # 1970
    0x50, 0x04, 0x08, 0x00, 0x60,  # 1980
    0x04, 0x0a, 0x00, 0x60, 0x05,  # 1990
    0x00, 0x30, 0x80, 0x05, 0x00,  # 2000
    0x40, 0x02, 0x07, 0x00, 0x50,  # 2010
    0x04, 0x09, 0x00, 0x60, 0x04,  # 2020
    0x00, 0x20, 0x60, 0x05, 0x00,  # 2030
    0x30, 0xb0, 0x06, 0x00, 0x50,  # 2040
    0x02, 0x07, 0x00, 0x50, 0x03  # 2050
]

START_YEAR = 1901
TianGan = '甲乙丙丁戊己庚辛壬癸'
DiZhi = '子丑寅卯辰巳午未申酉戌亥'
ShengXiao = '鼠牛虎兔龙蛇马羊猴鸡狗猪'
JieQi = '小寒大寒立春雨水惊蛰春分清明谷雨立夏小满芒种夏至小暑大暑立秋处暑白露秋分寒露霜降立冬小雪大雪冬至'
JieQi_Odd = "立春惊蛰清明立夏芒种小暑立秋白露寒露立冬大雪小寒"  # 节气节点，如立春-惊蛰是正月，两个节气一个月
JieQi_Month = {
    "立春": [0, "寅"],
    "惊蛰": [1, "卯"],
    "清明": [2, "辰"],
    "立夏": [3, "巳"],
    "芒种": [4, "午"],
    "小暑": [5, "未"],
    "立秋": [6, "申"],
    "白露": [7, "酉"],
    "寒露": [8, "戌"],
    "立冬": [9, "亥"],
    "大雪": [10, "子"],
    "小寒": [11, "丑"],
}


Gz_2_Wuxing = {
    '甲': '木',
    '乙': '木',
    '丙': '火',
    '丁': '火',
    '戊': '土',
    '己': '土',
    '庚': '金',
    '辛': '金',
    '壬': '水',
    '癸': '水',
    '子': '水',
    '丑': '土',
    '寅': '木',
    '卯': '木',
    '辰': '土',
    '巳': '火',
    '午': '火',
    '未': '土',
    '申': '金',
    '酉': '金',
    '戌': '土',
    '亥': '水',
}
# WuXing = ["金", "木", "水", "火", "土"]


class Lunar(object):
    def __init__(self, year, month, day, hour):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.nl_year = self.nl_month = self.nl_day = 1
        self.gz_year = self.gz_month = self.gz_day = self.gz_hour = ""
        self.shengxiao = ""

        self.set_nl_date()
        self.set_shengxiao()
        self.set_gz_year()
        self.set_gz_month()
        self.set_gz_day()
        self.set_gz_hour()
        self.bazi = [self.gz_year, self.gz_month, self.gz_day, self.gz_hour]

        self.wuxing = []
        self.set_wuxing()

    def set_nl_date(self):  # 返回农历日期整数元组（年、月、日）（查表法）
        delta_days = self._date_diff()

        # 阳历1901年2月19日为阴历1901年正月初一
        # 阳历1901年1月1日到2月19日共有49天
        if delta_days < 49:
            self.nl_year = START_YEAR - 1
            if delta_days < 19:
                self.nl_month = 11
                self.nl_day = 11 + delta_days
            else:
                self.nl_month = 12
                self.nl_day = delta_days - 18
            return self.nl_year, self.nl_month, self.nl_day

        # 下面从阴历1901年正月初一算起
        delta_days -= 49
        self.nl_year, self.nl_month, self.nl_day = START_YEAR, 1, 1
        # 计算年
        tmp = self._lunar_year_days(self.nl_year)
        while delta_days >= tmp:
            delta_days -= tmp
            self.nl_year += 1
            tmp = self._lunar_year_days(self.nl_year)

        # 计算月
        (foo, tmp) = self._lunar_month_days(self.nl_year, self.nl_month)
        while delta_days >= tmp:
            delta_days -= tmp
            if self.nl_month == self._get_leap_month(self.nl_year):
                (tmp, foo) = self._lunar_month_days(self.nl_year, self.nl_month)
                if delta_days < tmp:
                    return 0, 0, 0
                delta_days -= tmp
            self.nl_month += 1
            (foo, tmp) = self._lunar_month_days(self.nl_year, self.nl_month)

        # 计算日
        self.nl_day += delta_days
        return 0

    def set_shengxiao(self):  # 返回生肖年
        year = self.nl_year - 3 - 1  # 农历年份减3 （说明：补减1）
        year = year % 12  # 模12，得到地支数
        self.shengxiao = ShengXiao[year]
        return 0

    def set_gz_year(self):  # 返回干支纪年
        year = self.nl_year - 3 - 1  # 农历年份减3 （说明：补减1）
        G = year % 10  # 模10，得到天干数
        Z = year % 12  # 模12，得到地支数
        self.gz_year = TianGan[G] + DiZhi[Z]
        return 0

    def set_gz_month(self):  # 返回干支纪月
        """
        干支纪月的计算规则较为复杂，是本人在前人的基础上实现的，填补了空白。
        1、首先判断当前日期所处的节气范围，
        2、特别要考虑年数是否需要增减，以立春为界，如正月尚未立春的日子年数减一，
        3、月的天干公式 （年干序号 * 2 + 月数） % 10 ，其中 0 表示最后一个天干，
        4、月的地支是固定的，查表可得。
        """
        dt = datetime.datetime(self.year, self.month, self.day)
        jie_qi = self._get_jieqi(dt)

        def _at_jieqi_day():
            year = self.nl_year - 3  # 虽然农历已经是腊月，但是已经立春， 所以年加一
            G = year % 10  # 模10，得到天干数
            Z = year % 12  # 模12，得到地支数
            nl_year = TianGan[G] + DiZhi[Z]
            nl_month = 0
            return nl_year, nl_month

        if len(jie_qi) > 0 and jie_qi in JieQi_Odd:   # 如果恰好是节气当日
            if JieQi_Month[jie_qi][0] == 0 and self.nl_month == 12:
                nl_year, nl_month = _at_jieqi_day()
            else:
                nl_year = self.gz_year  # 干支纪年
                nl_month = JieQi_Month[jie_qi][0]  # 计算出干支纪月
        else:      # 如果不是节气日，则循环判断后一个分月节气是什么
            nl_year = self.gz_year
            nl_month = 0
            for i in range(-1, -40, -1):
                var_days = dt + datetime.timedelta(days=i)
                jie_qi = self._get_jieqi(var_days)
                if len(jie_qi) > 0 and jie_qi in JieQi_Odd:
                    if JieQi_Month[jie_qi][0] > 0:
                        nl_month = JieQi_Month[jie_qi][0]
                    elif JieQi_Month[jie_qi][0] == 0 and self.nl_month == 12:
                        nl_year, nl_month = _at_jieqi_day()
                    else:
                        nl_month = 0
                    break
        gan_str = TianGan
        month_num = (gan_str.find(nl_year[0])+1) * 2 + nl_month + 1
        M = month_num % 10
        if M == 0:
            M = 10
        self.gz_month = TianGan[M-1] + JieQi_Month[jie_qi][1]
        return 0

    def set_gz_day(self):  # 返回干支纪日
        C = self.year // 100  # 取世纪数，减一
        y = self.year % 100  # 取年份后两位（若为1月、2月则当前年份减一）
        y = y - 1 if self.month == 1 or self.month == 2 else y
        M = self.month  # 取月份（若为1月、2月则分别按13、14来计算）
        M = M + 12 if self.month == 1 or self.month == 2 else M
        d = self.day  # 取日数
        i = 0 if self.month % 2 == 1 else 6  # 取i （奇数月i=0，偶数月i=6）

        # 下面两个是网上的公式
        # http://baike.baidu.com/link?url=MbTKmhrTHTOAz735gi37tEtwd29zqE9GJ92cZQZd0X8uFO5XgmyMKQru6aetzcGadqekzKd3nZHVS99rewya6q
        # 计算干（说明：补减1）
        G = 4 * C + C // 4 + 5 * y + y // 4 + 3 * (M + 1) // 5 + d - 3 - 1
        G = G % 10
        # 计算支（说明：补减1）
        Z = 8 * C + C // 4 + 5 * y + y // 4 + 3 * (M + 1) // 5 + d + 7 + i - 1
        Z = Z % 12

        self.gz_day = TianGan[G] + DiZhi[Z]
        return 0

    def set_gz_hour(self):  # 返回干支纪时（时辰）
        """
        时干数 = ((日干 % 5)*2 + 时辰 -2) % 10
        """
        # 计算支
        Z = round((self.hour / 2) + 0.1) % 12  # 之所以加0.1是因为round的bug!!
        gz_day_num = TianGan.find(self.gz_day[0]) + 1
        gz_day_yu = gz_day_num % 5
        hour_num = Z + 1
        if gz_day_yu == 0:
            gz_day_yu = 5
        gz_hour_num = (gz_day_yu * 2 - 1 + hour_num-1) % 10
        if gz_hour_num == 0:
            gz_hour_num = 10
        self.gz_hour = TianGan[gz_hour_num-1] + DiZhi[Z]
        return 0

    # TODO
    def set_wuxing(self):
        gz_list = self.bazi
        wu_xing_str = ""
        for g in gz_list:
            wu_xing_str = wu_xing_str + self._gz_to_wu_xing(g)
        count = {}
        for i in wu_xing_str:
            if i not in count:
                count[i] = 1
            else:
                count[i] += 1
        self.wuxing = count
        return 0

    def print_info(self):    # 返回公历日期字符串
        print('公历生日：' + str(self.year) + '年' + str(self.month) + '月' + str(self.day) + '日' + "\n" +
              '农历生日：' + str(self.nl_year) + '年' + str(self.nl_month) + '月' + str(self.nl_day) + '日' + '\n' +
              '生肖：' + self.shengxiao + '\n' +
              '八字：' + ' '.join(self.bazi) + '\n' +
              '五行：' + ' '.join(self.wuxing)
              )
        return 0

    def _date_diff(self):
        """ 返回基于1901/01/01日差数 """
        return (datetime.datetime(self.year, self.month, self.day) - datetime.datetime(1901, 1, 1)).days

    def _get_leap_month(self, lunar_year):
        flag = LunarMonth[(lunar_year - START_YEAR) // 2]
        if (lunar_year - START_YEAR) % 2:
            return flag & 0x0f
        else:
            return flag >> 4

    def _lunar_month_days(self, lunar_year, lunar_month):
        if lunar_year < START_YEAR:
            return 30

        high, low = 0, 29
        iBit = 16 - lunar_month

        if lunar_month > self._get_leap_month(lunar_year) and self._get_leap_month(lunar_year):
            iBit -= 1

        if LunarMonthDay[lunar_year - START_YEAR] & (1 << iBit):
            low += 1

        if lunar_month == self._get_leap_month(lunar_year):
            if LunarMonthDay[lunar_year - START_YEAR] & (1 << (iBit - 1)):
                high = 30
            else:
                high = 29

        return high, low

    def _lunar_year_days(self, year):
        days = 0
        for i in range(1, 13):
            (high, low) = self._lunar_month_days(year, i)
            days += high
            days += low
        return days

    def _get_jieqi(self, dt):  # 返回农历节气
        for i in range(24):
            delta = self._rulian_day(dt) - self._julian_day_of_ln_jie(dt.year, i)
            if -.5 <= delta <= .5:     # 因为两个都是浮点数，不能用相等表示
                return JieQi[i * 2:(i + 1) * 2]
        return ""

    def _rulian_day(self, dt):
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

    def _julian_day(self, ct):
        year = ct.year
        month = ct.month
        day = ct.day

        if month <= 2:
            month += 12
            year -= 1

        B = year / 100
        B = 2 - B + year / 400

        dd = day + 0.5000115740  # 本日12:00后才是儒略日的开始(过一秒钟)*/
        return int(365.25 * (year + 4716) + 0.01) + int(30.60001 * (month + 1)) + dd + B - 1524.5

    def _julian_day_of_ln_jie(self, year, st):   # 返回指定年份的节气的儒略日数
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

    def _gz_to_wu_xing(self, gz_str):
        if len(gz_str) > 0:
            wu_xing = ""
            for gz in list(gz_str):
                wu_xing = wu_xing + Gz_2_Wuxing[gz]
            return wu_xing
        else:
            return ""


if __name__ == "__main__":
    example = Lunar(1994, 6, 12, 4)
    example.print_info()

