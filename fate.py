import utils


class Lunar(object):
    def __init__(self, year, month, day, hour, if_dt=True, gender='male', if_leap_month=False):
        self.hour = hour
        self.gender = gender     # female, male

        if if_dt:
            self.year = year
            self.month = month
            self.day = day
            self.nl_year, self.nl_month, self.nl_day = utils.transfer_dt_to_lunar(self.year, self.month, self.day)
        else:
            self.nl_year = year
            self.nl_month = month
            self.nl_day = day
            self.year, self.month, self.day = utils.transfer_lunar_to_dt(self.year, self.month, self.day, if_leap_month)

        self.gz_year = self.gz_month = self.gz_day = self.gz_hour = ""
        self.bazi = []
        self.rigan = []
        self.wuxing = []
        self.wuxing_it = {'火': 0, '土': 0, '水': 0, '金': 0, "木": 0}
        self.shishen = []
        self.yongshen = ''
        self.dayun = {}
        self.shengxiao = ""

    def init(self):
        print('公历生日：' + str(self.year) + '年' + str(self.month) + '月' + str(self.day) + '日' + "\n" +
              '农历生日：' + str(self.nl_year) + '年' + str(self.nl_month) + '月' + str(self.nl_day) + '日')

        self.set_shengxiao()
        self.set_bazi()
        self.set_wuxing()
        self.set_shishen()
        self.set_yongshen()
        self.set_dayun()
        self.set_xingxiushensha()

    def set_shengxiao(self):
        year = self.nl_year - 3 - 1     # 农历年份减3 （说明：补减1）
        year = year % 12                # 模12，得到地支数
        self.shengxiao = utils.SHENGXIAO[year]
        print('生肖：' + self.shengxiao)

    def set_bazi(self):
        self.gz_year = utils.cal_gz_year(self.nl_year)
        self.gz_month = utils.cal_gz_month(self.year, self.month, self.day, self.nl_year, self.nl_month, self.gz_year)
        self.gz_day = utils.cal_gz_day(self.year, self.month, self.day)
        self.gz_hour = utils.cal_gz_hour(self.hour, self.gz_day)
        self.bazi = [self.gz_year, self.gz_month, self.gz_day, self.gz_hour]

        rizhu = self.bazi[2][0]
        wuxing = utils.GAN_2_WX_YY[rizhu]
        self.rigan = [rizhu, wuxing[0], wuxing[1]]
        print('八字：' + ' '.join(self.bazi) + ', 日干为：' + self.rigan[0] + self.rigan[1])

    def set_wuxing(self):
        for gz in self.bazi:
            gan, zhi = gz[0], gz[1]
            self.wuxing.extend(utils.GAN_2_WX_YY[gan][0])
            self.wuxing.extend(utils.ZHI_2_WX_YY[zhi][0])

        # count
        attrs = set(self.wuxing)
        wx_str = ''
        for attr in attrs:
            wx_str += str(self.wuxing.count(attr)) + attr + ','
        if len(attrs) != 5:
            wx_str += '五行缺'
            for attr in utils.WUXING:
                if attr not in attrs:
                    wx_str += attr

        print('五行：' + wx_str)

    def set_shishen(self):     # TODO：count and analyze
        for gz in self.bazi:
            gan, zhi = gz[0], gz[1]
            gan_wuxing = utils.GAN_2_WX_YY[gan]
            shishen = utils.get_shishen(gan_wuxing, self.rigan)
            self.shishen.append([gan, gan_wuxing[0], gan_wuxing[1], shishen])
            zhi_wuxing = utils.ZHI_2_WX_YY[zhi]
            shishen = utils.get_shishen(zhi_wuxing, self.rigan)
            self.shishen.append([zhi, zhi_wuxing[0], zhi_wuxing[1], shishen])
        del (self.shishen[4])  # remove rigan
        print('十神：' + ','.join(self.shishen[i][3] for i in range(7)))

    def set_yongshen(self):
        bazi = ''.join(self.bazi)
        v_wx_it = utils.cal_wx_intensity(bazi, base=bazi[3])    # 以月支来计算五行强度
        self.wuxing_it['火'] = v_wx_it['火']
        self.wuxing_it['土'] = v_wx_it['土']
        self.wuxing_it['金'] = v_wx_it['金']
        self.wuxing_it['木'] = v_wx_it['木']
        self.wuxing_it['水'] = v_wx_it['水']
        same_cate, same_v = v_wx_it['同类']
        diff_cate, diff_v = v_wx_it['异类']

        '''
        "命以用神为紧要，看命神之法，不过扶抑而已。
        凡弱者宜扶，扶之者即用神也，扶之太过，抑其扶者为用神，扶之不及，扶其扶者为用神；
        凡强者宜抑，抑之者为用神也，抑之太过，抑其抑者为用神，抑之不及，扶其抑者为用神。
        --陈素庵《命理约言》卷一《看用神法》
        '''
        # TODO： how to calculate yongshen
        if same_v <= diff_v:
            print('日主自身偏弱，需要补强。')
            self.yongshen = same_cate[1]
        else:
            print('日主自身偏强，需要抑制。')
            self.yongshen = diff_cate

    def set_dayun(self):
        self.dayun = utils.get_dayun_ages(self.year, self.month, self.day, self.bazi, self.gender)

    def set_xingxiushensha(self):
        print("星宿神煞如下：")
        utils.check_xingxiushensha(self.bazi)



if __name__ == "__main__":
    example = Lunar(1994, 6, 12, 4, if_dt=True, gender='female', if_leap_month=False)
    # if_leap_month表示农历闰月，仅在if_dt=False时要求usr输入

    example.init()
