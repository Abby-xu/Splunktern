import csv
import random
import time
import os

## the last six digits ID the individual car
## Setting the VINs to 2019 Porsche Taycan
vin_seed = "WP1AA38743LLB0"
## build a list of numbers
vin_car  = (list(range(1000,9999)))
## randomize above list
random.shuffle(vin_car,random.random)
#  empty list for the VINs

vins = []
#  build the list of ~9000 cars by VIN

for v in vin_car :
    vin = str(vin_seed) + str(v)
    vins.append(vin)

#create a random sample of 50 vehicles which have the bad batteries.
bad_battery_vins = random.sample(vins, 50)

battery_warning = 0
battery_warning_var = 0
motor_warning = 0
event_count = 0
prob = 0
ratio = 0
filesize = 0
substring = str("00000")

readings = []
starttime = str(time.time())
print(starttime)

#readings.append(['timestamp', 'vin', 'batteryStatus', 'motorStatus', 'voltage'])
with open('voltage.csv', 'w', newline='') as csvfile:
    fieldnames = ['timestamp', 'vin', 'batteryStatus', 'motorStatus', 'voltage']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    while event_count < 1000000000 :

        for cars in vins:

            if cars not in bad_battery_vins :

                voltage_var = float("{0:.3f}".format(random.uniform(799, 801)))
                battery_status_var = None
                motor_status_var = None
            elif cars in bad_battery_vins :
                prob = random.choice(list(range(0, 100)))
                if prob == 5:
                    voltage_var = str(float("{0:.3f}".format(random.uniform(599, 780))))
                    battery_status_var = "Warning"
                    motor_status_var = "Warning"
                    battery_warning_var = battery_warning_var + 1

            timestamp = str(time.time())
            vin = cars
            batterystatus = str(battery_status_var)
            motorstatus = str(motor_status_var)
            voltage = str(voltage_var)

            #  readings = [{'timestamp' , timestamp}, {'vin' , cars}, {'batteryStatus' , battery_status}, {'motorStatus' , motor_status}, {'voltage' , voltage}]
            with open('voltage.csv', 'a', newline='') as csvfile:
                writer.writerow({'timestamp' : timestamp, 'vin' : vin, 'batteryStatus' : batterystatus, 'motorStatus' : motorstatus, 'voltage' : voltage})
            #filesize = round(os.path.getsize('voltage.csv') / 1000000000)
            event_count = event_count + 1
            #ratio = (battery_warning_var/event_count)*100
            if substring in str(event_count):
                print(event_count)

csvfile.close()
endtime = str(time.time())
print(starttime, endtime)