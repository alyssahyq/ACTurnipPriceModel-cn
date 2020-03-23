import re

pricePattern = re.compile('[0-9]+')
info = '''白萝卜价格趋势模型(简体中文)
Github: InsulatingShell
https://github.com/InsulatingShell/ACTurnipPriceModel-cn/
微博：@绝缘壳
版本：v 1.0
最后更新时间： Mar 23
目前如果输入了不含数字的内容，会直接退出，重新运行即可
'''


def readInput():
    price_raw = input()
    price = re.search(pricePattern, price_raw)
    return price.group(0)

def SunPriceCheck(price):
    if float(price) < 90 or float(price) > 110 :
        print("一般来说，白萝卜的购入价在 90-110 之间，如果确定没有输错，请再输入一次")
        new_price = readInput()
        if new_price == price:
            return new_price
        else:
            SunPriceCheck(new_price)
    else:
        return price

def priceCheck(price):
    if float(price) < 1 :
        print("白萝卜的价格应该是一个正整数")
        new_price = readInput()
        if new_price == price:
            return new_price
        else:
            SunPriceCheck(new_price)
    else:
        return price

class Turnip:
    sun = -1
    mon = -1
    tue = -1
    wed = -1
    thu = -1
    fri = -1
    sat = -1
    dec = 0
    inc = 0
    fir = 0
    sec = 0
    thr = 0
    fou = 0
    flag_fluc = False
    flag_decr = False
    flag_3 = False
    flag_4 = False
    lock_fluc = False
    expe_fluc = 0
    expe_3 = 0
    expe_4 = 0
    today = -1
    yesterday = -1
    def makePrediction(self):
        if Turnip.lock_fluc:
            Turnip.flag_fluc = True
            Turnip.flag_decr = False
            Turnip.flag_3 = False
            Turnip.flag_4 = False
        if Turnip.inc == 0 and Turnip.dec >=4 :
            Turnip.flag_decr = True
            Turnip.flag_3 = False
            Turnip.flag_4 = False
        if Turnip.flag_fluc == True:
            Turnip.expe_fluc = int(1.1*int(Turnip.sun))
            if Turnip.flag_decr or Turnip.flag_3 or Turnip.flag_4:
                print("目前可能是波动型，",end='')
            else:
                print("目前就是波动型，",end='')
            print("则最大卖价范围在",Turnip.expe_fluc,"至",int(1.45*int(Turnip.sun)),"之间",end='')
            if float(1.45*int(Turnip.sun)) > float(Turnip.today) >= float(Turnip.expe_fluc):
                print("。今日售价已有可能是波动型价格的最大值，可以考虑今天卖出")
            if float(1.45*int(Turnip.sun)) <= float(Turnip.today):
                print("。今日售价就是波动型价格的最大值，建议今天卖出")
            else:
                print('')
        if Turnip.flag_3 == True:
            Turnip.expe_3 = int(2 * int(Turnip.sun))
            if Turnip.flag_decr or Turnip.flag_fluc or Turnip.flag_4:
                print("目前可能是三期型，", end='')
            else:
                lock_3 = True
                print("目前就是三期型，", end='')
            print("则最大卖价范围在", Turnip.expe_3, "至", int(6 * int(Turnip.sun)), "之间")
            if Turnip.thr != 0:
                if lock_3:
                    print("今天就是三期型的售价峰值，请卖出")
                else:
                    print("今天可能是三期型的售价峰值，可以考虑卖出")
        if Turnip.flag_4 == True:
            Turnip.expe_4 = int(1.4 * int(Turnip.sun))
            if Turnip.flag_decr or Turnip.flag_fluc or Turnip.flag_3:
                print("目前可能是四期型，", end='')
            else:
                lock_4 = True
                print("目前就是四期型，", end='')
            print("则最大卖价范围在", Turnip.expe_4, "至", int(2 * int(Turnip.sun)), "之间")
            if Turnip.fou != 0:
                if lock_4:
                    print("今天就是四期型的售价峰值，请卖出")
                else:
                    print("今天可能是四期型的售价峰值，可以考虑卖出")
        if Turnip.flag_decr == True:
            if Turnip.flag_4 or Turnip.flag_fluc or Turnip.flag_3:
                print("目前可能是递减型，要做好可能会亏的准备")
            else:
                print("目前就是递减型，只会越来越便宜，我建议你现在就卖了")

    def roughModel(self):
        X = (float(Turnip.mon)/float(Turnip.sun))*100
        if  91 <= X <= 100:
            #print('可能是"波动型"或"4期型"')
            Turnip.flag_fluc = True
            Turnip.flag_4 = True
        elif 85 <= X < 91:
            #print('可能是"3期型"或"4期型"或"递减型"')
            Turnip.flag_3 = True
            Turnip.flag_4 = True
            Turnip.flag_decr = True
        elif 80 <= X < 85:
            #print('可能是"3期型"或"4期型"')
            Turnip.flag_3 = True
            Turnip.flag_4 = True
        elif 60 <= X < 80:
            #print('可能是"波动型"或"4期型"')
            Turnip.flag_fluc = True
            Turnip.flag_4 = True
        elif X < 60:
            print('接近"四期型"')
            Turnip.flag_4 = True
        elif X > 100:
            #print('波动型，有这么好的事？最高售价预计',int(1.1*float(Turnip.sun)),'至',int(1.45*float(Turnip.sun)))
            Turnip.flag_fluc = True
            Turnip.lock_fluc = True

    def recordPrice(self):
        if Turnip.lock_fluc == False:
            if Turnip.flag_3 or Turnip.flag_4:
                if Turnip.inc == 1:
                    Turnip.fir = Turnip.today
                else:
                    if Turnip.fir != 0 and Turnip.sec == 0:
                        Turnip.sec = Turnip.today
                    if Turnip.fir != 0 and Turnip.sec != 0 and Turnip.thr == 0:
                        Turnip.thr = Turnip.today
                    if Turnip.flag_4 and Turnip.flag_3 == False and Turnip.fir != 0 and Turnip.sec != 0 and Turnip.thr != 0 and Turnip.fou ==0 :
                        Turnip.fou = Turnip.today

    def compareYesterday(self):
        if (float(Turnip.yesterday) <= float(Turnip.today)):
            if Turnip.inc == 0: #连续下跌
                Turnip.dec = Turnip.dec + 1
            else:
                Turnip.inc = Turnip.inc + 1
        else:
            Turnip.inc = Turnip.inc + 1
        if Turnip.dec == 3:
            Turnip.flag_4 = False
        if Turnip.dec == 4:
            Turnip.flag_3 = False


    def Sun(self):
        print('请输入周日买入价，回车结束输入')
        sun_raw = readInput()
        Turnip.sun = SunPriceCheck(sun_raw)
        print('周日买入价为：', Turnip.sun)
        Turnip.today = Turnip.sun
        print('')

    def Mon(self):
        Turnip.yeseterday = Turnip.today
        print('请输入周一收购价，回车结束输入')
        mon_raw = readInput()
        Turnip.mon = priceCheck(mon_raw)
        print('周一买入价为：', Turnip.mon)
        Turnip.today = Turnip.mon
        Turnip.roughModel(self)
        Turnip.makePrediction(self)
        if(Turnip.mon <= Turnip.sun):
            Turnip.dec = Turnip.dec+1
        else:
            Turnip.lock_fluc = True
        print('')

    def Tue(self):
        Turnip.yeseterday = Turnip.today
        print('请输入周二收购价，回车结束输入')
        tue_raw = readInput()
        Turnip.tue = priceCheck(tue_raw)
        print('周二买入价为：', Turnip.tue)
        Turnip.today = Turnip.tue
        Turnip.compareYesterday(self)
        Turnip.recordPrice(self)
        Turnip.makePrediction(self)

    def Wed(self):
        Turnip.yeseterday = Turnip.today
        print('请输入周三收购价，回车结束输入')
        wed_raw = readInput()
        Turnip.wed = priceCheck(wed_raw)
        print('周三买入价为：', Turnip.wed)
        Turnip.today = Turnip.wed
        Turnip.compareYesterday(self)
        Turnip.recordPrice(self)
        Turnip.makePrediction(self)

    def Thu(self):
        Turnip.yeseterday = Turnip.today
        print('请输入周四收购价，回车结束输入')
        thu_raw = readInput()
        Turnip.thu = priceCheck(thu_raw)
        print('周四买入价为：', Turnip.thu)
        Turnip.today = Turnip.thu
        Turnip.compareYesterday(self)
        Turnip.recordPrice(self)
        Turnip.makePrediction(self)

    def Fri(self):
        Turnip.yeseterday = Turnip.today
        print('请输入周五收购价，回车结束输入')
        fri_raw = readInput()
        Turnip.fri = priceCheck(fri_raw)
        print('周五买入价为：', Turnip.fri)
        Turnip.today = Turnip.fri
        Turnip.compareYesterday(self)
        Turnip.recordPrice(self)
        Turnip.makePrediction(self)

    def Sat(self):
        Turnip.yeseterday = Turnip.today
        print('请输入周六收购价，回车结束输入')
        sat_raw = readInput()
        Turnip.sat = priceCheck(sat_raw)
        print('周六买入价为：', Turnip.sat)
        Turnip.today = Turnip.sat
        Turnip.compareYesterday(self)
        Turnip.recordPrice(self)
        Turnip.makePrediction(self)
        print('不过今天都周六了，无论如何都请卖了，否则全烂了')


def main():
    try:
        turnip = Turnip()
        print(info)
        turnip.Sun()
        turnip.Mon()
        turnip.Tue()
        turnip.Wed()
        turnip.Thu()
        turnip.Fri()
        turnip.Sat()
    except EOFError:
        exit(0)

if __name__ == '__main__':
    main()