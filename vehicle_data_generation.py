import random
import time
import csv
from datetime import datetime
from decimal import Decimal

'''
1. Generate VIM numbers for 10 cars
2. Based on timestamp to generate the voltage each 10 cars loop (<=.5%) | target car or non-target car
3. Based on the voltage get the status
4. Write into the csv file
'''

def prepare_car_data():
    # test cars are Tesla 2020 model 3
    # example car VIN: 5YJ3E1EA6LF591138
    VIN_pre8 = "5YJ3E1EA"
    VIN_9_list = ['0','1','2','3','4','5','6','7','8','9','X']
    VIN_10to11 = "LF"
    VIN_list = []
    for i in range(0, 10):
        VIN_list.append(VIN_pre8+random.choice(VIN_9_list)+VIN_10to11+str(int(random.uniform(0,1) * 1000000)).zfill(6))

    # mark target car randomly
    tar_car = random.choice(VIN_list)

    return VIN_list, tar_car

def writing_file(time_limit, VIN_list, tar_car):

    # timestamp (test)
    start_time = time.time()

    # creat csv file
    with open(filename, 'w', newline='') as result: 
        fw = csv.writer(result, delimiter=",")
        fw.writerow(["timestamp","vin","batteryStatus","motorStatus","voltage"])
    
        # creat a list for tracking the data of target car
        # tar_car_vol = []
        tar_car_warn_count = 0
        datagen_count = 0

        while (time.time() - start_time < time_limit):
            # each loop for the cars on the list
            for car in VIN_list:
                ts = str('%.6f' % time.time())
                VIN_num = car

                if (car != tar_car):
                    vol = random.uniform(799, 801)
                # target car: may have warning cases
                else:
                    vol = random.uniform(400,750) if random.randint(1, 1000) <= 5 and tar_car_warn_count/int(datagen_count/10) < 0.005 else random.uniform(799, 801) # len(tar_car_vol)
                    tar_car_warn_count = tar_car_warn_count + 1 if vol < 799 else tar_car_warn_count
                    # tar_car_vol.append(Decimal(vol).quantize(Decimal("0.001"), rounding = "ROUND_HALF_UP"))
                
                # get the status based on voltage
                MS = BS = "None" if vol >= 799 and vol <=801 else "Warning"
                volt = str(Decimal(vol).quantize(Decimal("0.001"), rounding = "ROUND_HALF_UP"))

                # adding data to the csv file
                fw.writerow([ts, VIN_num, MS, BS, volt])
                datagen_count += 1
    
        # check the ratio between warning cases and total cases for target car
        print("The number of data generated:",datagen_count)
        print("The number of 'Warning' of target car:", tar_car_warn_count)
        print('The percentage of "Warning" for target car is :', Decimal(tar_car_warn_count/datagen_count).quantize(Decimal("0.0001"), rounding = "ROUND_HALF_UP"))
    
                
if __name__ == '__main__':
    start_time = time.time()
    print("start time:", datetime.fromtimestamp(start_time))
    time_limit = 60 # input("please input the time limit: ") # unit: s
    filename = "v1.csv" # input("please input the writing file name:")
    cars, tar_car = prepare_car_data()
    print("The car list:", cars)
    print("The target car is:", tar_car)
    timeLimit = time_limit - (time.time() - start_time)
    writing_file(timeLimit, cars, tar_car)
'''
Test result:
1.  1 min
    The number of data generated: 15043490
    The number of 'Warning' of target car: 7481
    The percentage of "Warning" for target car is : 0.0005

2.  2 min
    The number of data generated: 30193720
    The number of 'Warning' of target car: 15056
    The percentage of "Warning" for target car is : 0.0005

3.  5 min
    The number of data generated: 72849380
    The number of 'Warning' of target car: 36291
    The percentage of "Warning" for target car is : 0.0005

4.  10 min
    The number of data generated: 148587120
    The number of 'Warning' of target car: 73974
    The percentage of "Warning" for target car is : 0.0005

y = 39284.4898 + 14806476.2245 * x
By using linear exterpolation, one hour will generate 888427858 data.
'''