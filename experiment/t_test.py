from os import name
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import mean
from numpy.lib.function_base import append
from numpy.lib.twodim_base import tri
import pandas as pd
import numpy as np
from itertools import chain
import pingouin as pg
import math




numoftrials=30
numofmodes=6
numberofpoints=5999

robot=False
robot2=False
# mean error for robot = 1.58

names_arr=['_novibro','_vibro','_holonovibro','_holovibro','_allnovibro','_allvibro']
titles=['Graph','Graph with haptics','AR with obstacle','AR with haptics and obstacle','AR without obstacle','AR with haptics without obstacle']

userdataframe=[]
# 6, 7? ,9, 11, 13, 14?
# Penetration is stored in 29 trial, Robot trials are stored in 27 trial
for user in [7,10,11,12,13,16,19,20,21,24]: #chain(range(7,8), range(10,17),range(18,23),range(24,26)):
    data=[]
    for i in range(numofmodes):
        data.append(pd.read_csv('/home/nurlando/AllExperiments/experiment'+str(user)+'/trial'+str(user)+'/'+str(user)+names_arr[i]+'.csv'))
        data[i].rename(columns={col: col+names_arr[i] for col in data[i].columns},inplace=True)
    userdataframe.append(pd.concat(data,axis=1))
numofusers=len(userdataframe)

df=pd.concat(userdataframe,keys=['user'+str(i) for i in range(numofusers)])

timee=df['Time_novibro'].loc['user0'][2000:5000]-df['Time_novibro'].loc['user0'][2000]


# modenames=['graph','pass','holo','pass','all']
# dfarray=[]
# for i in range(0,6,2):
#     df_aov=pd.DataFrame(list(zip(array[i]+array[i+1],a[i]+a[i+1])),columns=['error','mode'])
#     df_aov.to_csv(modenames[i]+'.csv',index=False)
#     dfarray.append(df_aov)




