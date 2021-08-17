from math import *
import csv
from datetime import datetime
from  statistics import stdev
import json

'''
ENMO : The Eucliden Norm Minus One 
its to correlate with magnitude of acceleration and 
human energy

'''
def ENMO(x,y,z):
  return max(0,sqrt((x*x)+(y*y)+(z*z))-1)



def activity_count(ENMO_VAL):
  fx = lambda x : max(0,x-0.002)
  return sum([fx(x) for x in ENMO_VAL])


'''
LIDS : Locomoter inactivity During Sleep
involves non linear conversion of locomoter activity
'''
def LIDS(activity_c):
  return 100.0/(activity_c+1)



'''
Angle related to Z axis
'''
def anglez(x,y,z):
  return atan(z/sqrt((x*x)+(y*y)))*(180/pi)



def readcsv(file):
  data = []
  cr = csv.reader(open(file,'r'),delimiter=',')
  for x in cr:
    if len(x) == 4:
      try: data.append(x)
      except: pass
  return data


def strtotime(text):
  return datetime.strptime(text,"%H:%M:%S")


def calculate_q_time(csv_file):
   t = [x[0] for x in csv_file]
   ta = strtotime(t[0])
   tb = strtotime(t[-1])
   return (tb-ta).total_seconds()


def divide_data(data,n):
  return [data[i * n:(i + 1) * n] for i in range((len(data) + n - 1) // n )]
  
  

def analyze(file):
   deep_sleep = 0
   wake_time = 0
   normal_sleep =0
   total_sleep = 0 
   avg_activity = 0
   avg_lids = 0
   fcsv = readcsv(file)
   dtime = calculate_q_time(fcsv)
   deach_t = dtime/len(fcsv)
   nd = divide_data(fcsv,5)
   AVG = lambda A: sum(A)/float(len(A))
   for Z in nd:
      JE = [ENMO(float(G[1]),float(G[2]),float(G[3])) for G in Z]
      X_A = AVG([float(G[1]) for G in Z])
      Y_A = AVG([float(G[2]) for G in Z])
      Z_A = AVG([float(G[3]) for G in Z])
      activity = activity_count(JE)
      lids_val = LIDS(activity)
      avg_activity+=activity
      avg_lids+=lids_val
      try: std_val = stdev([anglez(float(G[1]),float(G[2]),float(G[3])) for G in Z])
      except: std_val = None
      angle_val = anglez(X_A,Y_A,Z_A)
      #print("ACTIVITY : {}  LIDS : {} ANGLE : {}° STD : {}".format(activity,lids_val,angle_val,std_val))
      if std_val !=None and std_val < 0.3:
         deep_sleep+=deach_t*len(Z)
      if std_val != None and std_val > 2:
         wake_time+=deach_t*len(Z)
      if std_val != None and std_val > 0.3 and std_val < 1:
         normal_sleep+=deach_t*len(Z)

   r_data = {
    'total_accelerometer_recoding':dtime,
    'deep_sleep_time':deep_sleep,
    'normal_sleep_time':normal_sleep,
    'total_sleep_time':deep_sleep+normal_sleep,
    'wake_time':wake_time,
    'average_activity':avg_activity/float(len(nd)),
    'average_lids':avg_lids/float(len(nd))
   } 
   return json.dumps(r_data, indent=4, sort_keys=True)
