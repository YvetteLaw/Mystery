import utils


class Lunar(object):
    def __init__(self, year, month, day, hour, gender):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.gender = gender     # female, male

        self.nl_year = self.nl_month = self.nl_day = 1
        self.gz_year = self.gz_month = self.gz_day = self.gz_hour = ""
        self.bazi = []
        self.rigan = []
        self.yongshen = []
        self.wuxing = []
        self.wuxing_it = {'火': 0, '土': 0, '水': 0, '金': 0, "木": 0}
        self.shishen = []

        self.shengxiao = ""

        self.age_qiyun = 1

    def init(self):
        self.set_nl_date()
        self.set_shengxiao()
        self.set_bazi()
        self.set_wuxing()
        self.set_rizhu()
        self.set_shishen()
        self.set_yongshen()

    def set_nl_date(self):
        self.nl_year, self.nl_month, self.nl_day = utils.cal_nl_date(self.year, self.month, self.day)

    def set_shengxiao(self):
        year = self.nl_year - 3 - 1     # 农历年份减3 （说明：补减1）
        year = year % 12                # 模12，得到地支数
        self.shengxiao = utils.SHENGXIAO[year]

    def set_bazi(self):
        self.gz_year = utils.cal_gz_year(self.nl_year)
        self.gz_month = utils.cal_gz_month(self.year, self.month, self.day, self.nl_year, self.nl_month, self.gz_year)
        self.gz_day = utils.cal_gz_day(self.year, self.month, self.day)
        self.gz_hour = utils.cal_gz_hour(self.hour, self.gz_day)
        self.bazi = [self.gz_year, self.gz_month, self.gz_day, self.gz_hour]

    def set_wuxing(self):
        self.wuxing = utils.cal_wuxing(self.bazi)

    def set_rizhu(self):  # 日主，采用日干来推演
        rizhu = self.bazi[2][0]
        wuxing = utils.GAN_2_WX_YY[rizhu]
        self.rigan = [rizhu, wuxing[0], wuxing[1]]

    def set_shishen(self):
        self.shishen = utils.cal_shishen(self.rigan, self.bazi)

    def set_yongshen(self):
        bazi = ''.join(self.bazi)
        v_wx_it = utils.cal_wx_intensity(bazi)
        self.wuxing_it['火'] = v_wx_it['火']
        self.wuxing_it['土'] = v_wx_it['土']
        self.wuxing_it['金'] = v_wx_it['金']
        self.wuxing_it['木'] = v_wx_it['木']
        self.wuxing_it['水'] = v_wx_it['水']
        same_cate, same_v = v_wx_it['同类']
        diff_cate, diff_v = v_wx_it['异类']
        if same_v <= diff_v:
            print('日干偏弱，需要补强')
            self.yongshen = same_cate
        else:
            print('日干偏强，需要抑制')
            self.yongshen = diff_cate


    def print_info(self):
        print('公历生日：' + str(self.year) + '年' + str(self.month) + '月' + str(self.day) + '日' + "\n" +
              '农历生日：' + str(self.nl_year) + '年' + str(self.nl_month) + '月' + str(self.nl_day) + '日' + '\n' +
              '生肖：' + self.shengxiao + '\n' +
              '八字：' + ','.join(self.bazi) + '\n' +
              '五行：' + ','.join(self.wuxing) + '\n' +
              '十神：' + ','.join(self.shishen[i][3] for i in range(7))
              )


if __name__ == "__main__":
    # example = Lunar(1994, 6, 12, 4, 'female')
    example = Lunar(1968, 9, 29, 8, 'female')
    example.init()
    example.print_info()
