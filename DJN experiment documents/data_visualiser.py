import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data=pd.read_csv("force_data(try1).csv")
data=data.to_numpy()
time=data[:,0]

desiredforce=data[:,2]
eventforce=data[:,3]
weissforce=data[:,6]
robotforce=data[:,5]
error=data[:,1]


p=0
tenerrors=[]
for i in range(len(desiredforce)-1):
    if desiredforce[i]==0 and desiredforce[i+1]<0:
        tenerrors.append(((desiredforce[p:i+1]-eventforce[p:i+1])**2).mean()/(i+1-p))
        p=i+1

print(tenerrors)
desiredforce=-abs(desiredforce)
robotforce=-robotforce
plt.plot(time,desiredforce,c='green')
plt.plot(time,eventforce,c='red')
#plt.plot(time,weissforce,c='purple')
#plt.plot(time,robotforce,c='blue')
plt.show()