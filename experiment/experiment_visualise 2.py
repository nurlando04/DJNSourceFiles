import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

trial=1
names=['novibro_'+str(trial),'vibro_'+str(trial),'holonovibro_'+str(trial),'holovibro_'+str(trial),'allnovibro_'+str(trial),'allvibro_'+str(trial)]
data=[0,0,0,0,0,0]

t=[0,0,0,0,0,0]

desiredforces=[0,0,0,0,0,0]
eventforces=[0,0,0,0,0,0]
weissforces=[0,0,0,0,0,0]
robotforces=[0,0,0,0,0,0]
errors=[0,0,0,0,0,0]


for i in range(6):
    data[i]=pd.read_csv('~/experiment/test_'+names[i]+'/SE.csv')
    data[i]=data[i].to_numpy()
    if i <=1:
        t[i]=data[i][:,0]
        desiredforces[i]=-abs(data[i][:,2])
        eventforces[i]=data[i][:,3]
        weissforces[i]=data[i][:,6]
        robotforces[i]=data[i][:,5]
        errors[i]=data[i][:,1]
    else:
        t[i]=data[i][:,0][:-40]
        desiredforces[i]=-abs(data[i][:,2])[:-40]
        #desiredforces[i]=desiredforces[i][:-40]
        eventforces[i]=data[i][:,3][40:]
        #eventforces[i]=eventforces[i][40:]
        weissforces[i]=data[i][:,6]
        robotforces[i]=data[i][:,5]
        errors[i]=data[i][:,1]

fig, axs = plt.subplots(2, 3)
axs[0, 0].plot(t[0], desiredforces[0],'tab:green')
axs[0, 0].plot(t[0], eventforces[0],'tab:red')
axs[0, 0].set_title('no vibro')
axs[1, 0].plot(t[1], desiredforces[1], 'tab:green')
axs[1, 0].plot(t[1], eventforces[1], 'tab:red')
axs[1, 0].set_title('vibro')
axs[0, 1].plot(t[2], desiredforces[2], 'tab:green')
axs[0, 1].plot(t[2],eventforces[2], 'tab:red')
axs[0, 1].set_title('holo no vibro with obstacle')
axs[1, 1].plot(t[3], desiredforces[3], 'tab:green')
axs[1, 1].plot(t[3], eventforces[3], 'tab:red')
axs[1, 1].set_title('holo vibro with obstacle')
axs[0, 2].plot(t[4], desiredforces[4], 'tab:green')
axs[0, 2].plot(t[4], eventforces[4], 'tab:red')
axs[0, 2].set_title('holo no vibro without obstacle')
axs[1, 2].plot(t[5], desiredforces[5], 'tab:green')
axs[1, 2].plot(t[5], eventforces[5], 'tab:red')
axs[1, 2].set_title('holo vibro without obstacle')




for ax in axs.flat:
    ax.set(xlabel='Time', ylabel='Force(N)')





sixerrors=[]
for x in range(2):
    desiredforce=desiredforces[x]
    eventforce=eventforces[x]
    p=0
    thirtyerrors=[]
    for i in range(len(desiredforce)-1):
        if desiredforce[i]==0 and desiredforce[i+1]<0:
            thirtyerrors.append(((desiredforce[p:i+1]-eventforce[p:i+1])**2).mean()/(i+1-p))
            p=i+1
    sixerrors.append(thirtyerrors)
    print(len(thirtyerrors))

for x in range(2,6):
    desiredforce=desiredforces[x]
    eventforce=eventforces[x]
    p=0
    thirtyerrors=[]
    for i in range(len(desiredforce)-1):
        if desiredforce[i]==0 and desiredforce[i+1]<0:
            thirtyerrors.append(((desiredforce[p:i+1]-eventforce[p+40:i+1+40])**2).mean()/(i+1-p))
            p=i+1
    sixerrors.append(thirtyerrors)
    print(len(thirtyerrors))


fig2, axs2 = plt.subplots(2, 3)
axs2[0, 0].bar(range(len(sixerrors[0])),sixerrors[0])
axs2[0, 0].set_title('no vibro')
axs2[1, 0].bar(range(len(sixerrors[1])),sixerrors[1])
axs2[1, 0].set_title('vibro')
axs2[0, 1].bar(range(len(sixerrors[2])),sixerrors[2])
axs2[0, 1].set_title('holo no vibro with obstacle')
axs2[1, 1].bar(range(len(sixerrors[3])),sixerrors[3])
axs2[1, 1].set_title('holo vibro with obstacle')
axs2[0, 2].bar(range(len(sixerrors[4])),sixerrors[4])
axs2[0, 2].set_title('holo no vibro without obstacle')
axs2[1, 2].bar(range(len(sixerrors[5])),sixerrors[5])
axs2[1, 2].set_title('holo vibro without obstacle ')

for ax2 in axs2.flat:
    ax2.set_ylim(0,0.20)
    ax2.set(xlabel='number of trial', ylabel='MSE')
plt.show()

#for i in range(6):
#    print(i)
#    print(sixerrors[i])




