import mall as x
import time
import sys
import os

if os.path.exists('log.txt'):
    os.remove('log.txt')

loop = 0

f1 = 0
f2 = 0
f3 = 0
total = 0
mytotal = 0
yes = 0

print "===================start======================"
test_day = 31
step = 10

#x.clean_test_data()
#x.get_test_day_data(test_day)
look = 1

for mid_day in range(20,27,3):
#   for look in range(1,20,step):
    for keep in range(1,20,8):
        for car in range(1,30,5):
            buy = car
#            for buy in range(1,30,5):
            hold_l = car
            hold_h = car+30
            hold_step = 8
            for hold in range(hold_l,hold_h,hold_step):
                loop = loop + 1

                log = "==========[%s][start]========== \n" %time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                print log
                f = open('log.txt', 'a+')
                f.write(log)
                f.close()

                log = "round [%d] test_day %d, mid_day %d, buy %d, car %d, keep %d, look %d, hold %d \n" %(loop, test_day, mid_day, buy, car, keep, look, hold)
                print log
                f = open('log.txt', 'a+')
                f.write(log)
                f.close()

                calc_list = x.calculate_item(1, test_day, mid_day, buy, car, keep, look, hold)
                real_list = x.get_result_day_buy_list(1)
                f1,f2,f3,total,mytotal,yes = x.f1_result(calc_list,real_list)

                log = "[f1 %f] f2 %f f3 %f total %d mytotal %d yes %d \n" %(f1,f2,f3,total,mytotal,yes)
                print log
                f = open('log.txt', 'a+')
                f.write(log)
                f.close()

                log = "==========[%s][end]========== \n" %time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                print log
                f = open('log.txt', 'a+')
                f.write(log)
                f.close()

print "===================end======================"

