import matplotlib.pyplot as plt
from numpy.core.fromnumeric import mean
from numpy.lib.function_base import append
from numpy.lib.twodim_base import tri
import pandas as pd
import numpy as np
from itertools import chain
import pingouin as pg
import math


#user=1
mean1=[]
numoftrials=29
numofmodes=6
numberofpoints=5999
numofusers=1
allerrors=np.zeros((numofmodes,numofusers,numoftrials)) # number of graphs, number of users, number of trials of a user
allerrors2=np.zeros((numofmodes,numofusers,numoftrials))
allweissforces=np.zeros((numofmodes,numofusers,numberofpoints))


'''
mode1(novibro)[[trial1 . . . . . . . trial29] user1
               [                            ] user2
               [                            ] user3
               [                            ] .
               [                            ] .
               [                            ] .
               [                            ] .
               [                            ] .
               [                            ] .
               [                            ] .
               [                            ] user20 ]
mode2(vibro)[]
.
.
.
.
mode6(allvibro)
'''


usercount=0
negativeweissmean=np.zeros((numofmodes,numofusers,1))

names_arr=['_novibro','_vibro','_holonovibro','_holovibro','_allnovibro','_allvibro']
titles=['No Vibro','Vibro','Holo No Vibro with obstacle','Holo Vibro with obstacle','All No Vibro with obstacle','All Vibro with obstacle']

# 6, 7? ,9, 11, 13, 14?
for user in [27]: #chain(range(7,8), range(10,17),range(18,23),range(24,26)):
    
    data=[0,0,0,0,0,0]
    t=[0,0,0,0,0,0]
    desiredforces=[0,0,0,0,0,0]
    eventforces=[0,0,0,0,0,0]
    desiredcurves=[[],[],[],[],[],[]]
    eventcurves=[[],[],[],[],[],[]]
    weissforces=[0,0,0,0,0,0]
    robotforces=[0,0,0,0,0,0]
    errors=[0,0,0,0,0,0]

    delay=160
    for i in range(numofmodes):
        data[i]=pd.read_csv('/home/nurlando/AllExperiments/experiment'+str(user)+'/trial'+str(user)+'/'+str(user)+names_arr[i]+'.csv')
        data[i]=data[i].to_numpy()
        if i <=1:
            if user<=5:
                t[i]=data[i][:,0][delay:]
            else:
                t[i]=data[i][:,0]
            t[i]=t[i]-t[i][0]
            if user<=5:
                desiredforces[i]=-abs(data[i][:,2])[delay:]
                eventforces[i]=data[i][:,3][:-delay]
                for x in range(len(desiredforces[i])):
                    if desiredforces[i][x]<0:
                        desiredcurves[i].append(desiredforces[i][x])
                        eventcurves[i].append(eventforces[i][x])
            else:
                desiredforces[i]=-abs(data[i][:,2])
                eventforces[i]=data[i][:,3]
                for x in range(len(desiredforces[i])):
                    if desiredforces[i][x]<0:
                        desiredcurves[i].append(desiredforces[i][x])
                        eventcurves[i].append(eventforces[i][x])


            weissforces[i]=data[i][:,6]
            robotforces[i]=data[i][:,5]
            
            errors[i]=data[i][:,1]
        else:
            if user<=5:
                t[i]=data[i][:,0][delay:]
            else:
                t[i]=data[i][:,0]
            t[i]=t[i]-t[i][0]
            if user<=5:
                desiredforces[i]=-abs(data[i][:,2])[delay:]
                eventforces[i]=data[i][:,3][:-delay]
                for x in range(len(desiredforces[i])):
                    if desiredforces[i][x]<0:
                        desiredcurves[i].append(desiredforces[i][x])
                        eventcurves[i].append(eventforces[i][x]) 
            else:
                desiredforces[i]=-abs(data[i][:,8])
                eventforces[i]=data[i][:,9]
                for x in range(len(desiredforces[i])):
                    if desiredforces[i][x]<0:
                        desiredcurves[i].append(desiredforces[i][x])
                        eventcurves[i].append(eventforces[i][x])
            weissforces[i]=data[i][:,6]
            robotforces[i]=data[i][:,5]
            errors[i]=data[i][:,1]
        
        try:
            if True:
                #extract mean weisssforce from each user mode
                allweissforces[i,usercount,:]=weissforces[i]
                meanofusertrial=[]
                print(usercount)
                for j in range(numberofpoints):
                    if weissforces[i][j]<0:
                        meanofusertrial.append(weissforces[i][j])
                mean=np.mean(meanofusertrial)
                negativeweissmean[i,usercount,0]=mean
        except:
            print("passed")
            pass


    fig,axs=plt.subplots(2,2)
    z=2
    for ax in axs.flat:
        ax.plot(range(math.floor(len(desiredforces[z])/2)),desiredforces[z][-math.floor(len(desiredforces[z])/2)-1:-1],'g')
        ax.plot(range(math.floor(len(eventforces[z])/2)),eventforces[z][-math.floor(len(eventforces[z])/2)-1:-1],'r')
        ax.set(xlabel='Time', ylabel='Force(N)')
        z+=1

    
    figcurves,axcurves=plt.subplots(2,2)
    z=2
    for ax in axcurves.flat:
        ax.plot(range(math.floor(len(desiredcurves[z])/2)),desiredcurves[z][-math.floor(len(desiredcurves[z])/2)-1:-1],'g')
        ax.plot(range(math.floor(len(eventcurves[z])/2)),eventcurves[z][-math.floor(len(eventcurves[z])/2)-1:-1],'r')
        ax.set(xlabel='Time', ylabel='Force(N)')
        z+=1
    
    if True:    
        '''
        fig, axs = plt.subplots(2, 3)
        axs[0, 0].plot(t[0], desiredforces[0],'tab:green')
        axs[0, 0].plot(t[0], eventforces[0],'tab:red')
        axs[0, 0].set_title(str(user) + ' no vibro')
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
            ax.set_xlim(0,100)
        '''
    
    # for errora of th whole sinus
    sixerrors=[]
    for x in range(numofmodes):
        desiredforce=desiredforces[x]
        eventforce=eventforces[x]
        p=0
        thirtyerrors=[]
        for i in range(len(desiredforce)-1):
            if desiredforce[i]==0 and desiredforce[i+1]<0:
                thirtyerrors.append(np.sqrt((desiredforce[p:i+1]-eventforce[p:i+1])**2).mean()) #thirtyerrors.append(((desiredforce[p:i+1]-eventforce[p:i+1])**2).mean()/(i+1-p))
                p=i+1
        sixerrors.append(thirtyerrors)
       
    for i in range(numofmodes):
        for j in range(numoftrials):
            allerrors[i][usercount][j]=sixerrors[i][j]
    
    '''
    #for errors of only curves
    #ERRRRRRRRRRRRRRRrrrORRRRRRRRRRRRRRRRRRRRRRRRRRR need to be fixed wrong compare everything
        sixerrors2=[]
    for x in range(numofmodes):
        desiredforce=desiredcurves[x]
        eventforce=eventcurves[x]
        p=0
        thirtyerrors=[]
        for i in range(len(desiredforce)-1):
            if round(desiredforce[i],2)==-0.22 and round(desiredforce[i+1],2)==-0.44:
                thirtyerrors.append(np.sqrt((np.array(desiredforce[p:i+1])-np.array(eventforce[p:i+1]))**2).mean()) #thirtyerrors.append(((np.array(desiredforce[p:i+1])-np.array(eventforce[p:i+1]))**2).mean()/(i+1-p))
                p=i+1
        sixerrors2.append(thirtyerrors)
       
    for i in range(numofmodes):
        for j in range(numoftrials):
            allerrors2[i][usercount][j]=sixerrors2[i][j]
    '''

    if True:
        '''
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
        '''
    
    usercount+=1
plt.show()

#All errors during all trials of users in each mode
if True:  
    finalerrors=[[],[],[],[],[],[]]
    for i in range(numofmodes):
        for j in range(15,numoftrials):
            finalerrors[i].append(allerrors[i,:,j])


    fig3, axs3 = plt.subplots(3,2) 
    i=0
    for ax in axs3.flat:
        ax.boxplot(finalerrors[i])
        ax.set(xlabel='Time', ylabel='Force(N)')
        ax.set_ylim(0,5)
        ax.set_title(titles[i])
        i+=1
'''
#all errors during all trial CURVES of users in each mode
if True:  
    finalerrors2=[[],[],[],[],[],[]]
    for i in range(numofmodes):
        for j in range(15,numoftrials):
            finalerrors2[i].append(allerrors2[i,:,j])


    fig3curves, axs3curves = plt.subplots(3,2) 
    i=0
    for ax in axs3curves.flat:
        ax.boxplot(finalerrors[i])
        ax.set(xlabel='Time', ylabel='Force(N)')
        ax.set_ylim(0,5)
        ax.set_title(titles[i])
        i+=1
'''

#boxplot of all errors each mode
if True:
    
    allerrorsofeachmode=[]
    for i in range(numofmodes):
        allerrorsofeachmode.append(allerrors[i,:,15:28].flatten())

    fig4,axs4 = plt.subplots(1)
    axs4.boxplot(allerrorsofeachmode)
    axs4.set_ylim(0,5)
    axs4.set_xticklabels(titles)
    axs4.set_title("All errors of each mode")


'''
#boxplot of all errors each mode CURVES!!!
if True:
    
    allerrorsofeachmode=[]
    for i in range(numofmodes):
        allerrorsofeachmode.append(allerrors2[i,:,15:28].flatten())

    fig4curves,axs4curves = plt.subplots(1)
    axs4curves.boxplot(allerrorsofeachmode)
    axs4curves.set_xticklabels(titles)
    axs4curves.set_title("All errors of each mode CURVES")
    plt.show()
'''
#create csv file for means of each mode each user
if True:
    mean_error_each_mode_each_user=[[],[],[],[],[],[]]
    for i in range(numofmodes):
        for j in range(usercount):
            mean_error_each_mode_each_user[i].append(np.mean(allerrors[i,j,:]))

    a=[]
    vibronovibro=['vibro','novibro']
    for i in range(numofmodes):
        a.append([vibronovibro[i%2]]*len(mean_error_each_mode_each_user[i]))

    modenames=['graph','pass','holo','pass','all']
    dfarray=[]
    for i in range(0,6,2):
        df=pd.DataFrame(list(zip(mean_error_each_mode_each_user[i]+mean_error_each_mode_each_user[i+1],a[i]+a[i+1])),columns=["errors",'mode'])
        df.to_csv(modenames[i]+'.csv',index=False)
        dfarray.append(df)


    for i in range(3):
        aov=pg.anova(dv='errors', between='mode',data=dfarray[i],detailed=True)
        print(aov)

#csv and anova of all errors each mode
if True:
    a=[]
    vibronovibro=['vibro','novibro']
    for i in range(numofmodes):
        a.append([vibronovibro[i%2]]*len(allerrorsofeachmode[i]))

    modenames=['graph2','pass','holo2','pass','all2']
    dfarray=[]
    for i in range(0,6,2):
        df=pd.DataFrame(list(zip(np.concatenate((allerrorsofeachmode[i],allerrorsofeachmode[i+1]), axis=None),a[i]+a[i+1])),columns=["errors",'mode'])
        df.to_csv(modenames[i]+'.csv',index=False)
        dfarray.append(df)
    print("''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''\n")
    for i in range(3):
        aov=pg.anova(dv='errors', between='mode',data=dfarray[i],detailed=True)
        print(aov)
print(len(a[0]),len(allerrorsofeachmode[0]))


#Normalization
if True:
    allerrorsnormalize=np.zeros((numofmodes,usercount,numoftrials))
    for i in range(numofmodes):
        for j in range(usercount):
            MaxinRow=np.amax(allerrors[i,j,:])
            allerrorsnormalize[i,j,:]=allerrors[i,j,:]/MaxinRow

    finalerrors=[[],[],[],[],[],[]]
    for i in range(numofmodes):
        for j in range(numoftrials):
            finalerrors[i].append(allerrorsnormalize[i,:,j])


    fig5, axs5 = plt.subplots(3,2)

    i=0
    for ax in axs5.flat:
        ax.boxplot(finalerrors[i])
        ax.set_title(titles[i])
        ax.set(xlabel='Trial number', ylabel='MSE')
        ax.set_ylim(-1,2)
        ax.set
        i+=1

    plt.show()


if True:
    generalerror=[]
    for i in range(numofmodes):
        generalerror.append(allerrorsnormalize[i].flatten())

    fig4,axs4 = plt.subplots(1)
    axs4.boxplot(generalerror)
    axs4.set_ylim(-1,2)
    axs4.set_xticklabels(titles)
    axs4.set_title("All errors of each mode")
    plt.show()





if True:
    weissmeanarray2=[]
    for i in range(numofmodes):
        weissmeanarray2.append(negativeweissmean[i,:,0])

    fig7,axs7 = plt.subplots(1)
    axs7.boxplot(weissmeanarray2)
    axs7.set_ylim(-5,0)

    plt.show()




'''
sumnumpy=np.zeros(usercount)
for i in range(numofmodes):
    for j in range(usercount):
        rowsum=np.sum(allerrors[i,j,:])
        sumnumpy[j]+=rowsum
print(sumnumpy)
'''




