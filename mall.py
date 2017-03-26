import numpy as np
import csv
import os
import shutil

debug = 1

#file_name donot have .csv
def creat_file(path, file_name, data_list):
    tmp = ''
    name = ''
    creat_name = ''
    name = [path, file_name, '.csv']
    creat_name = tmp.join(name)
    with open(creat_name, 'w') as opt_func:
        writer = csv.writer(opt_func)
        writer.writerows(data_list)
    opt_func.close()

#file_name have .csv
def get_file_path(path, file_name):
    tmp = ''
    name_container = [path, file_name]
    name = tmp.join(name_container)

    return name

#file_name donot have .csv
def get_file_path_csv(path, file_name):
    tmp = ''
    name_container = [path, file_name, '.csv']
    name = tmp.join(name_container)

    return name

#file_name add .csv
def filename_add_csv(file_name):
    tmp = ''
    name_container = [file_name, '.csv']
    name = tmp.join(name_container)

    return name

def get_csv_list_data(file_path):
    
    data = np.loadtxt(file_path, delimiter=',', dtype=str)

    return data

#get item list
def get_item_id_list():
    id_list = []
    data = get_csv_list_data("item_id_list.csv")

    for row in data:
        id_list.append(int(row[0]))

    return id_list

#get cate list
def get_cate_id_list():
    id_list = []
    record_list = []
    data = get_csv_list_data("item_id_list.csv")

    for row in data:
        cate_id = int(row[1])
        if cate_id not in id_list:
            id_list.append(cate_id)

    return id_list

#save item list to file
def format_item_csv():
    item = []
    item_id_list = []
    item_record_list = []
    item_data = np.loadtxt('tianchi_fresh_comp_train_item.csv', delimiter=',', dtype=str)
    item_data_lenth = len(item_data)
    if debug == 1:
        print item_data_lenth

    for i in range(item_data_lenth):
        if i == 0:
            continue
        else:
            item_row = []
            item_id = int(item_data[i][0])
            cate_id = int(item_data[i][2])

            if item_id not in item_record_list:
                if debug == 1:
                    print i
                    print item_id
                item_row.append(item_id)
                item_row.append(cate_id)
                item_id_list.append(item_row)
                item_record_list.append(item_id)

    if debug == 1:
        print item_id_list
    with open('item_id_list.csv', 'w') as item_func:
        writer = csv.writer(item_func)
        writer.writerows(item_id_list)
    item_func.close()

#split tianchi_fresh_comp_train_item.csv to "$cate_id".csv by cate id
def split_item_csv():
    data = get_csv_list_data("item_id_list.csv")
    sorted_data = sorted(data, key=lambda x:x[1], reverse=True)
    lenth = len(sorted_data)
    if debug == 1:
        print lenth

    cate = []

    for i in range(lenth):
        if i == 0:
            continue
        elif i == lenth - 2:#last item dismissed
            break
        else:
            row = []
            row.append(int(sorted_data[i][0]))
            row.append(0)
            cate.append(row)

            if sorted_data[i][1] != sorted_data[i+1][1]:
                creat_file('item_data/', str(sorted_data[i][1]), cate)
                cate = []

#get best item of cate
def save_item_sell_to_cateid_csv():
    file_list = os.listdir("clean_data/")
    file_list = file_list[1:]
    cnt = 0

    item_file_list = os.listdir("item_data/")
    item_file_list = item_file_list[1:]

    for row in file_list:
        name = get_file_path('clean_data/', row)
        user_data=np.loadtxt(name, delimiter=',', dtype=str)
        user_data_lenth=len(user_data)
        if debug == 1:
            cnt = cnt + 1
            print cnt
            print name
   
        for i in range(user_data_lenth):
            if int(user_data[i][2]) == 4:
                file_name = filename_add_csv(user_data[i][4])
                if file_name not in item_file_list:
                    continue
                cate_name = get_file_path_csv('item_data/', user_data[i][4])
                cate_data = np.loadtxt(cate_name, delimiter=',', dtype=str)
                cate_data_lenth = len(cate_data)

                if cate_data_lenth < 3:
                    continue
                new_data = []

                for row in cate_data:
                    new_row = []
                    if int(row[0]) == int(user_data[i][1]):
                        row[1] = int(row[1]) + 1
                     
                    new_row.append(int(row[0]))
                    new_row.append(int(row[1]))
                    new_data.append(new_row)

                with open(cate_name, 'w') as opt_func:
                    writer = csv.writer(opt_func)
                    writer.writerows(new_data)
                opt_func.close()

def sort_cateid_csv():
    file_list = os.listdir("item_data/")
    file_list = file_list[1:]
   
    for row in file_list:
        name = get_file_path('item_data/', row)
        data = np.loadtxt(name, delimiter=',', dtype=str)
        data_len = len(data)
        new_data = []
        for i in range(data_len):
            line = []
            line.append(int(data[i][0]))
            line.append(int(data[i][1]))
            new_data.append(line)

        sorted_data = sorted(new_data, key=lambda x:x[1], reverse=True)
        
        with open(name, 'w') as opt_func:
            writer = csv.writer(opt_func)
            writer.writerows(sorted_data)
        opt_func.close()

#split tianchi_fresh_comp_train_user.csv to "$user_id".csv by user id
def split_user_csv():
    file_list = os.listdir("user_data/")
    file_list = file_list[1:]

    for row in file_list:
        name = get_file_path('user_data/', row)
        os.remove(name)
   
    user_data = np.loadtxt('tianchi_fresh_comp_train_user.csv', delimiter=',', dtype=str)
    user_data_lenth = len(user_data)
    
    user = []

    if debug == 1:
        print user_data_lenth
        cnt = 0

    item_id_list = get_item_id_list()
    cate_id_list = get_cate_id_list()
    flag = 0

    for i in range(user_data_lenth):
        if i == 0:
            continue

        if  i == user_data_lenth - 2:#last item dismissed
            break
        else:
            if user_data[i][0] != user_data[i+1][0]:
                if flag == 1:
                    flag = 0
                    if debug == 1:
                        print '******'
                    creat_file('user_data/', str(user_data[i][0]), user)
                user = []

            else:
                cate_id = int(user_data[i][4])
                if cate_id not in cate_id_list:
                    continue

                item_id = int(user_data[i][1])
                if item_id not in item_id_list:
                    continue

                if debug == 1:
                    print '======'

                user_row = []
                user_row.append(int(user_data[i][0]))
                user_row.append(int(user_data[i][1]))
                user_row.append(int(user_data[i][2]))
                user_row.append(user_data[i][3][0:5])
                user_row.append(int(user_data[i][4]))
                user_row.append(user_data[i][5])
                user.append(user_row)
                flag = 1

def user_data_clean():    
    file_list = os.listdir('user_data/')
    file_list = file_list[1:]

    for row in file_list:
        name = get_file_path('user_data/', row)
        user_data=np.loadtxt(name, delimiter=',', dtype=str)
        user_data_lenth=len(user_data)

        if user_data_lenth < 10:
            if debug == 1:
                print "disgard"
                print name
            continue

        for i in range(user_data_lenth):
            if user_data[i][5][0:10] == '2014-11-18':
                user_data[i][5] = 1
            if user_data[i][5][0:10] == '2014-11-19':
                user_data[i][5] = 2
            if user_data[i][5][0:10] == '2014-11-20':
                user_data[i][5] = 3
            if user_data[i][5][0:10] == '2014-11-21':
                user_data[i][5] = 4
            if user_data[i][5][0:10] == '2014-11-22':
                user_data[i][5] = 5
            if user_data[i][5][0:10] == '2014-11-23':
                user_data[i][5] = 6
            if user_data[i][5][0:10] == '2014-11-24':
                user_data[i][5] = 7
            if user_data[i][5][0:10] == '2014-11-25':
                user_data[i][5] = 8
            if user_data[i][5][0:10] == '2014-11-26':
                user_data[i][5] = 9
            if user_data[i][5][0:10] == '2014-11-27':
                user_data[i][5] = 10
            if user_data[i][5][0:10] == '2014-11-28':
                user_data[i][5] = 11
            if user_data[i][5][0:10] == '2014-11-29':
                user_data[i][5] = 12
            if user_data[i][5][0:10] == '2014-11-30':
                user_data[i][5] = 13
            if user_data[i][5][0:10] == '2014-12-01':
                user_data[i][5] = 14
            if user_data[i][5][0:10] == '2014-12-02':
                user_data[i][5] = 15
            if user_data[i][5][0:10] == '2014-12-03':
                user_data[i][5] = 16
            if user_data[i][5][0:10] == '2014-12-04':
                user_data[i][5] = 17
            if user_data[i][5][0:10] == '2014-12-05':
                user_data[i][5] = 18
            if user_data[i][5][0:10] == '2014-12-06':
                user_data[i][5] = 19
            if user_data[i][5][0:10] == '2014-12-07':
                user_data[i][5] = 20
            if user_data[i][5][0:10] == '2014-12-08':
                user_data[i][5] = 21
            if user_data[i][5][0:10] == '2014-12-09':
                user_data[i][5] = 22
            if user_data[i][5][0:10] == '2014-12-10':
                user_data[i][5] = 23
            if user_data[i][5][0:10] == '2014-12-11':
                user_data[i][5] = 24
            if user_data[i][5][0:10] == '2014-12-12':
                user_data[i][5] = 25
            if user_data[i][5][0:10] == '2014-12-13':
                user_data[i][5] = 26
            if user_data[i][5][0:10] == '2014-12-14':
                user_data[i][5] = 27
            if user_data[i][5][0:10] == '2014-12-15':
                user_data[i][5] = 28
            if user_data[i][5][0:10] == '2014-12-16':
                user_data[i][5] = 29
            if user_data[i][5][0:10] == '2014-12-17':
                user_data[i][5] = 30
            if user_data[i][5][0:10] == '2014-12-18':
                user_data[i][5] = 31

        creat_file('clean_data/', str(user_data[0][0]), user_data)

#generate test data, split date by day
def get_test_day_data(day):
    file_list = os.listdir("clean_data/")
    file_list = file_list[1:]

    for row in file_list:
        name = get_file_path('clean_data/', row)
        user_data=np.loadtxt(name, delimiter=',', dtype=str)
        user_data_lenth=len(user_data)

        if user_data_lenth < 10:
            if debug == 1:
                print "disgard"
                print name
            continue

        line_test_day_list = []
        line_result_day_list = []

        for i in range(user_data_lenth):
            if (int(user_data[i][5]) == day):
                line = []
                line.append(user_data[i][0])
                line.append(user_data[i][1])
                line.append(user_data[i][2])
                line.append(user_data[i][3])
                line.append(user_data[i][4])
                line.append(user_data[i][5])
                line_result_day_list.append(line)
            elif (int(user_data[i][5]) < day):       
                line = []
                line.append(user_data[i][0])
                line.append(user_data[i][1])
                line.append(user_data[i][2])
                line.append(user_data[i][3])
                line.append(user_data[i][4])
                line.append(user_data[i][5])
                line_test_day_list.append(line)
            else:
                if debug == 1:
                    print user_data[0][0]
                    print user_data[i][5]
                    print 'abandon'

        if len(line_test_day_list) != 0:
            creat_file('test/', str(user_data[0][0]), line_test_day_list)
        if len(line_result_day_list) != 0:
            creat_file('result/', str(user_data[0][0]), line_result_day_list)

#clean test/ and result/ data
def clean_test_data():
    file_list = os.listdir("test/")
    file_list = file_list[1:]

    for row in file_list:
        name = get_file_path('test/', row)
        os.remove(name)

    file_list = os.listdir("result/")
    file_list = file_list[1:]

    for row in file_list:
        name = get_file_path('result/', row)
        os.remove(name)

def clean_all_data():
    file_list = os.listdir("f1/")
    file_list = file_list[1:]

    for row in file_list:
        name = get_file_path('f1/', row)
        os.remove(name)

    file_list = os.listdir("user_data/")
    file_list = file_list[1:]

    for row in file_list:
        name = get_file_path('user_data/', row)
        os.remove(name)

    file_list = os.listdir("clean_data/")
    file_list = file_list[1:]

    for row in file_list:
        name = get_file_path('clean_data/', row)
        os.remove(name)

    file_list = os.listdir("item_data/")
    file_list = file_list[1:]

    for row in file_list:
        name = get_file_path('item_data/', row)
        os.remove(name)


#calculate out result day buy list
def get_result_day_buy_list(iorc):
    file_list = os.listdir("result/")
    file_list = file_list[1:]

    line_list = []
    for row in file_list:
        name = get_file_path('result/', row)
        user_data=np.loadtxt(name, delimiter=',', dtype=str)
        user_data_lenth=len(user_data)

        if user_data_lenth == 6:
            if debug == 1:
                print "disgard"
                print name
            continue

        if debug == 1:
            print row

        for i in range(user_data_lenth):
            if (int(user_data[i][2]) == 4):
                line = []
                line.append(user_data[i][0])

                if iorc == 1:
                    line.append(user_data[i][1])
                else:
                    line.append(user_data[i][4])

                line_list.append(line)

    creat_file('f1/', 'test_result', line_list)
    return line_list

#calculate out f1
def f1_result(calc_result, real_result):
    yes = 0
    total = len(real_result)
    my_total = len(calc_result)

    if (int(my_total) == 0):
        print ("my_total", my_total)
        return 0,0,0,total,my_total,0

    if (int(total) == 0):
        print ("total", total)
        return 0,0,0,total,my_total,0

    for cline in calc_result:
        for rline in real_result:
            if int(cline[0]) == int(rline[0]):
                if int(cline[1]) == int(rline[1]):
                    yes = yes + 1
                    break

    no = total - yes

    if debug == 1:
        print my_total
        print total   
        print yes

    pre = float(yes)/float(my_total)
    recall = float(yes)/float(total)
    f3 = 2*pre*recall
    f2 = pre+recall

    print ("f2,f3,yes,my_total,total")
    print (f2, f3, yes, my_total, total)
    if (f2 == 0):
        return 0,f2,f3,total,my_total,yes

    f1 = f3/f2

    if debug == 1:
        print ("pre, recall", pre, recall)
        print ('f1', f1)

    return f1,f2,f3,total,my_total,yes

#calculate test_day = result_day - 1
#1 use operation
#2 clean items of low freq
#3 opt high freq item in same cate
def calculate_item(test, test_day, mid_day, i_buy, i_car, i_keep, i_look, i_hold):
    item_id_list = get_item_id_list()

    if test == 1:
        file_list = os.listdir("test")
    else:
        file_list = os.listdir("clean_data")
    file_list = file_list[1:]

    iresult_list = []
    cnt = 0

    for row in file_list:
        if debug == 1:
            cnt = cnt + 1
            print cnt

        if test == 1:
            name = get_file_path('test/', row)
            if debug == 1:
                print name
        else:
            name = get_file_path('clean_data/', row)
            test_day = 32 #warning

        user_data=np.loadtxt(name, delimiter=',', dtype=str)
        user_data_lenth=len(user_data)

        if (user_data_lenth < 10):
            continue

        item_att_list = []
        item_res = {}

#        for day in range(test_day):
 #           if day < mid_day:
 #               continue

        for row in user_data:
            user_id = int(row[0])
            item_id = int(row[1])
            opt_type = int(row[2])
            opt_day = int(row[5])
            if opt_day < mid_day:
                continue

            if item_id in item_att_list:
                continue

            if opt_type == 4:
                item_res[item_id] = 0   #clear zero
                item_res[item_id] = item_res.get(item_id, 0)+i_buy
            if opt_type == 3:
                item_res[item_id] = item_res.get(item_id, 0)+i_car
            if opt_type == 2:
                item_res[item_id] = item_res.get(item_id, 0)+i_keep
            if opt_type == 1:
                item_res[item_id] = item_res.get(item_id, 0)+i_look

            if item_res[item_id] > i_hold:
                if item_id in item_id_list:
                    item_att_list.append(item_id)
                    user_result_list = []
                    user_result_list.append(user_id)
                    user_result_list.append(item_id)
                    iresult_list.append(user_result_list)

    if test == 0:
        creat_file('f1/', 'tianchi_mobile_recommendation_predict', iresult_list)

    return iresult_list

