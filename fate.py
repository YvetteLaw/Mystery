from utils import *


class Lunar(object):
    def __init__(self, year, month, day, hour, gender='male', if_dt=True, if_leap_month=False):
        self.gender = gender
        self.hour = hour
        if if_dt:
            self.year, self.month, self.day = year, month, day
            self.nl_year, self.nl_month, self.nl_day = transfer_dt_to_lunar(self.year, self.month, self.day)
        else:
            self.nl_year, self.nl_month, self.nl_day = year, month, day
            self.year, self.month, self.day = transfer_lunar_to_dt(self.year, self.month, self.day, if_leap_month)
        self.gz_year = self.gz_month = self.gz_day = self.gz_hour = ""
        self.bazi = []
        self.rigan = None
        self.wuxing = {'火': 0, '土': 0, '水': 0, '金': 0, "木": 0}
        self.shishen = []
        self.yongshen = []
        self.mingge = ''
        self.dayun = {}
        self.shengxiao = ""
        self.xxss = []

    def set_shengxiao(self):
        year = self.nl_year - 3 - 1     # 农历年份减3（补减1）
        year = year % 12                # 模12，得到地支数
        self.shengxiao = SHENGXIAO[year]

    def set_bazi(self):
        self.gz_year = cal_gz_year(self.nl_year)
        self.gz_month = cal_gz_month(self.year, self.month, self.day, self.nl_year, self.nl_month, self.gz_year)
        self.gz_day = cal_gz_day(self.year, self.month, self.day)
        self.gz_hour = cal_gz_hour(self.hour, self.gz_day)
        self.bazi = [self.gz_year, self.gz_month, self.gz_day, self.gz_hour]
        self.rigan = GAN_NODE[self.bazi[2][0]]

    def set_wuxing(self):
        wuxing = []
        for gz in self.bazi:
            gan, zhi = gz[0], gz[1]
            wuxing.extend(GAN_NODE[gan].wuxing)
            wuxing.extend(ZHI_NODE[zhi].wuxing)

        self.wuxing['金'] = wuxing.count('金')
        self.wuxing['木'] = wuxing.count('木')
        self.wuxing['水'] = wuxing.count('水')
        self.wuxing['火'] = wuxing.count('火')
        self.wuxing['土'] = wuxing.count('土')

    def set_shishen(self):
        for gz in self.bazi:
            gan, zhi = gz[0], gz[1]
            self.shishen.append(get_shishen(GAN_NODE[gan], self.rigan))
            self.shishen.append(get_shishen(ZHI_NODE[zhi], self.rigan))
        del (self.shishen[4])  # remove rigan

    def set_yongshen(self):
        """
        命以用神为紧要，看命神之法，不过扶抑而已。
        凡弱者宜扶，扶之者即用神也，扶之太过，抑其扶者为用神，扶之不及，扶其扶者为用神；
        凡强者宜抑，抑之者为用神也，抑之太过，抑其抑者为用神，抑之不及，扶其抑者为用神。
        --陈素庵《命理约言》卷一《看用神法》
        """

        bazi = ''.join(self.bazi)
        v_wx_it = cal_wx_intensity(bazi, self.rigan, base=bazi[3])

        same_cate, same_v = v_wx_it['同类']
        diff_cate, diff_v = v_wx_it['异类']
        if same_v <= diff_v:
            self.yongshen = [same_cate[1]]
            print('日主自身偏弱，需要补强。用神为：' + ','.join(self.yongshen))
        else:
            self.yongshen = diff_cate               # TODO： how to calculate yongshen
            print('日主自身偏强，需要抑制。用神为：' + ','.join(self.yongshen))

    def set_mingge(self):
        self.mingge = get_mingge(self.bazi, self.shishen, self.rigan)

    def set_dayun(self):
        self.dayun = get_dayun_ages(self.year, self.month, self.day, self.bazi, self.gender)

    def set_xingxiushensha(self):
        self.xxss = check_xingxiushensha(self.bazi)

    def set_xingchonghaihua(self):            # TODO
        return 0

    def init(self):
        print('公历生日：' + str(self.year) + '年' + str(self.month) + '月' + str(self.day) + '日')
        print('农历生日：' + str(self.nl_year) + '年' + str(self.nl_month) + '月' + str(self.nl_day) + '日')

        self.set_shengxiao()
        print('生肖：' + self.shengxiao)

        self.set_bazi()
        print('八字：' + ' '.join(self.bazi) + ', 日干为：' + self.rigan.name + self.rigan.wuxing)

        self.set_wuxing()
        wx_str = '五行：'
        for k, v in self.wuxing.items():
            wx_str += str(v) + k + ', '
        print(wx_str[:-2])

        self.set_shishen()
        print('十神：' + ','.join(self.shishen[i] for i in range(7)))

        self.set_yongshen()

        self.set_mingge()
        print("命格为：" + self.mingge)

        self.set_dayun()
        dy_str = '大运：'
        for k, v in self.dayun.items():
            dy_str += str(k) + '-' + v + ', '
        print(dy_str[:-2])

        self.set_xingxiushensha()
        print("星宿神煞：含有" + '、'.join(self.xxss))

        self.set_xingchonghaihua()


def analyze():
    example = Lunar(1994, 6, 12, 4, gender='female', if_dt=True, if_leap_month=False)
    # if_leap_month表示农历闰月，仅在if_dt=False时要求usr输入
    # gender输入为male或female

    example.init()


if __name__ == "__main__":
    analyze()
