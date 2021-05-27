from datetime import datetime
import os
import json
import csv

from sleep_cal import *

#ACCELEROMETER_DATA
'''
{
  "ACCELEROMETER": {
    "values": [
      -0.7540000081062317,
      6.74399995803833,
      6.914000034332275
    ]
  }
}

'''

filename=input('File Name : ')
while True:
  c_time  = datetime.now()
  acc_read = json.loads(os.popen("termux-sensor -s ACCELEROMETER -n 1").read())
  x,y,z = acc_read['ACCELEROMETER']['values']
  print(c_time,x,y,z,anglez(x,y,z))  
  with open(filename,'a',newline='') as file:
    cwriter = csv.writer(file)
    cwriter.writerow([c_time,x,y,z])
