import re

pricePattern = re.compile('[0-9]+')
info = '''白萝卜价格趋势模型(简体中文)
Github: InsulatingShell
https://github.com/InsulatingShell/ACTurnipPriceModel-cn/
微博：@绝缘壳
版本：v 1.1
最后更新时间： Mar 25
感谢微博 @这个昵称还没有人注册 的反馈，现在已经考虑了每日上午和下午价格不同的情况
'''


def readInput():
    price_raw = input()
    price = re.search(pricePattern, price_raw)
    return price.group(0)

def SunPriceCheck(price):
    while float(price) < 90 or float(price) > 110 :
        print("一般来说，白萝卜的购入价在 90-110 之间，如果确定没有输错，请再输入一次")
        new_price = readInput()
        if int(new_price) == int(price):
            price = new_price
            break
        else:
            price = new_price
    return price

def priceCheck(price):
    while float(price) < 0 :
        print("白萝卜的价格应该是一个正整数")
        new_price = readInput()
        if new_price == price:
            price = new_price
            break
        else:
            price = new_price
    return price

class Turnip:
    sun = -1
    mon_am = -1
    mon_pm = -1
    tue_am = -1
    tue_pm = -1
    wed_am = -1
    wed_pm = -1
    thu_am = -1
    thu_pm = -1
    fri_am = -1
    fri_pm = -1
    sat_am = -1
    sat_pm = -1
    inc = 0 #记录是否上涨
    dec = 0 #记录连续下跌次数
    fir = 0
    sec = 0
    thr = 0
    fou = 0
    flag_fluc = False
    flag_decr = False
    flag_3 = False
    flag_4 = False
    lock_fluc = False
    #期望
    expe_fluc = 0
    expe_3 = 0
    expe_4 = 0
    now = -1
    last = -1
    lock_3 = False
    lock_4 = False

    def makePrediction(self):
        if Turnip.lock_fluc:
            Turnip.flag_fluc = True
            Turnip.flag_decr = False
            Turnip.flag_3 = False
            Turnip.flag_4 = False
        if Turnip.inc == 0 and Turnip.dec >=8 :
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
                Turnip.lock_3 = True
                print("目前就是三期型，", end='')
            print("则最大卖价范围在", Turnip.expe_3, "至", int(6 * int(Turnip.sun)), "之间")
            if Turnip.thr != 0:
                if Turnip.lock_3:
                    print("今天就是三期型的售价峰值，请卖出")
                else:
                    print("今天可能是三期型的售价峰值，可以考虑卖出")
        if Turnip.flag_4 == True:
            Turnip.expe_4 = int(1.4 * int(Turnip.sun))
            if Turnip.flag_decr or Turnip.flag_fluc or Turnip.flag_3:
                print("目前可能是四期型，", end='')
            else:
                Turnip.lock_4 = True
                print("目前就是四期型，", end='')
            print("则最大卖价范围在", Turnip.expe_4, "至", int(2 * int(Turnip.sun)), "之间")
            if Turnip.fou != 0:
                if Turnip.lock_4:
                    print("今天就是四期型的售价峰值，请卖出")
                else:
                    print("今天可能是四期型的售价峰值，可以考虑卖出")
        if Turnip.flag_decr == True:
            if Turnip.flag_4 or Turnip.flag_fluc or Turnip.flag_3:
                print("目前可能是递减型，要做好可能会亏的准备")
            else:
                print("目前就是递减型，只会越来越便宜，我建议你现在就卖了")

    def roughModel(self):
        X = (float(Turnip.mon_am)/float(Turnip.sun))*100
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

    def compareLastPrice(self):
        if (float(Turnip.last) >= float(Turnip.now)):
            if Turnip.inc == 0: #连续下跌
                Turnip.dec = Turnip.dec + 1
            #else:
                #Turnip.inc = Turnip.inc + 1
        else:
            #print("if (",float(Turnip.last)," <= ",float(Turnip.now),",:")
            Turnip.inc = Turnip.inc + 1
        if Turnip.dec == 8: #周四下午都没变调
            print("周四下午都没发生变调吗？情况不妙，趁早离手")
            Turnip.flag_4 = False
            Turnip.flag_3 = False
        #print("inc = ", Turnip.inc)
        #print("dec = ",Turnip.dec)


    def Sun(self):
        print('请输入周日买入价，回车结束输入')
        sun_raw = readInput()
        Turnip.sun = SunPriceCheck(sun_raw)
        print('周日买入价为：', Turnip.sun)
        Turnip.today = Turnip.sun
        print('')

    def Mon_AM(self):
        Turnip.last = Turnip.now
        print('请输入周一上午收购价，回车结束输入')
        raw_input = readInput()
        Turnip.mon_am = priceCheck(raw_input) #
        print('周一上午收购价为：', Turnip.mon_am) #
        Turnip.now = Turnip.mon_am #
        Turnip.roughModel(self)
        Turnip.makePrediction(self)
        if(float(Turnip.mon_am) <= float(Turnip.sun)):
            Turnip.dec = Turnip.dec+1
        else:
            Turnip.lock_fluc = True
        print('')

    def Mon_PM(self):
        Turnip.last = Turnip.now
        print('请输入周一下午收购价，回车结束输入')
        raw_input = readInput()
        Turnip.mon_pm = priceCheck(raw_input)  #
        print('周一下午收购价为：', Turnip.mon_pm)  #
        Turnip.now = Turnip.mon_pm  #
        Turnip.compareLastPrice(self)
        Turnip.recordPrice(self)
        Turnip.makePrediction(self)
        print('')

    def Tue_AM(self):
        Turnip.last = Turnip.now
        print('请输入周二上午收购价，回车结束输入')
        raw_input = readInput()
        Turnip.tue_am = priceCheck(raw_input)  #
        print('周二上午收购价为：', Turnip.tue_am)  #
        Turnip.now = Turnip.tue_am  #
        Turnip.compareLastPrice(self)
        Turnip.recordPrice(self)
        Turnip.makePrediction(self)
        print('')

    def Tue_PM(self):
        Turnip.last = Turnip.now
        print('请输入周二下午收购价，回车结束输入')
        raw_input = readInput()
        Turnip.tue_pm = priceCheck(raw_input)  #
        print('周二下午收购价为：', Turnip.tue_pm)  #
        Turnip.now = Turnip.tue_pm  #
        Turnip.compareLastPrice(self)
        Turnip.recordPrice(self)
        Turnip.makePrediction(self)
        print('')

    def Wed_AM(self):
        Turnip.last = Turnip.now
        print('请输入周三上午收购价，回车结束输入')
        raw_input = readInput()
        Turnip.wed_am = priceCheck(raw_input)  #
        print('周三上午收购价为：', Turnip.wed_am)  #
        Turnip.now = Turnip.wed_am  #
        Turnip.compareLastPrice(self)
        Turnip.recordPrice(self)
        Turnip.makePrediction(self)
        print('')

    def Wed_PM(self):
        Turnip.last = Turnip.now
        print('请输入周三下午收购价，回车结束输入')
        raw_input = readInput()
        Turnip.wed_pm = priceCheck(raw_input)  #
        print('周三下午收购价为：', Turnip.wed_pm)  #
        Turnip.now = Turnip.wed_pm  #
        Turnip.compareLastPrice(self)
        Turnip.recordPrice(self)
        Turnip.makePrediction(self)
        print('')

    def Thu_AM(self):
        Turnip.last = Turnip.now
        print('请输入周四上午收购价，回车结束输入')
        raw_input = readInput()
        Turnip.thu_am = priceCheck(raw_input)  #
        print('周四上午收购价为：', Turnip.thu_am)  #
        Turnip.now = Turnip.thu_am  #
        Turnip.compareLastPrice(self)
        Turnip.recordPrice(self)
        Turnip.makePrediction(self)
        print('')

    def Thu_PM(self):
        Turnip.last = Turnip.now
        print('请输入周四下午收购价，回车结束输入')
        raw_input = readInput()
        Turnip.thu_pm = priceCheck(raw_input)  #
        print('周四下午收购价为：', Turnip.thu_pm)  #
        Turnip.now = Turnip.thu_pm  #
        Turnip.compareLastPrice(self)
        Turnip.recordPrice(self)
        Turnip.makePrediction(self)
        print('')

    def Fri_AM(self):
        Turnip.last = Turnip.now
        print('请输入周五上午收购价，回车结束输入')
        raw_input = readInput()
        Turnip.fri_am = priceCheck(raw_input)  #
        print('周五上午收购价为：', Turnip.fri_am)  #
        Turnip.now = Turnip.fri_am  #
        Turnip.compareLastPrice(self)
        Turnip.recordPrice(self)
        Turnip.makePrediction(self)
        print('')

    def Fri_PM(self):
        Turnip.last = Turnip.now
        print('请输入周五下午收购价，回车结束输入')
        raw_input = readInput()
        Turnip.fri_pm = priceCheck(raw_input)  #
        print('周五下午收购价为：', Turnip.fri_pm)  #
        Turnip.now = Turnip.fri_pm  #
        Turnip.compareLastPrice(self)
        Turnip.recordPrice(self)
        Turnip.makePrediction(self)
        print('')

    def Sat_AM(self):
        Turnip.last = Turnip.now
        print('请输入周六上午收购价，回车结束输入')
        raw_input = readInput()
        Turnip.sat_am = priceCheck(raw_input)  #
        print('周六上午收购价为：', Turnip.sat_am)  #
        Turnip.now = Turnip.sat_am  #
        Turnip.compareLastPrice(self)
        Turnip.recordPrice(self)
        Turnip.makePrediction(self)
        print('')

    def Sat_PM(self):
        Turnip.last = Turnip.now
        print('请输入周六下午收购价，回车结束输入')
        raw_input = readInput()
        Turnip.sat_pm = priceCheck(raw_input)  #
        print('周六下午收购价为：', Turnip.sat_pm)  #
        Turnip.now = Turnip.sat_pm  #
        Turnip.compareLastPrice(self)
        Turnip.recordPrice(self)
        Turnip.makePrediction(self)
        print('不过现在都周六下午了，无论如何都请卖了，否则全烂了')
        print('')


def main():
    try:
        turnip = Turnip()
        print(info)
        turnip.Sun()
        turnip.Mon_AM()
        turnip.Mon_PM()
        turnip.Tue_AM()
        turnip.Tue_PM()
        turnip.Wed_AM()
        turnip.Wed_PM()
        turnip.Thu_AM()
        turnip.Thu_PM()
        turnip.Fri_AM()
        turnip.Fri_PM()
        turnip.Sat_AM()
        turnip.Sat_PM()
    except EOFError:
        exit(0)

if __name__ == '__main__':
    main()
