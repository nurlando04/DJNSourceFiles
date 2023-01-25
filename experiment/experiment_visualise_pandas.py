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
    #for robot trial
    if user==27:
        robot=True
    if user==29 or user==31:
        robot2=True
numofusers=len(userdataframe)

df=pd.concat(userdataframe,keys=['user'+str(i) for i in range(numofusers)])

timee=df['Time_novibro'].loc['user0'][2000:5000]-df['Time_novibro'].loc['user0'][2000]

#for robot trial
if robot:
    df['force_desired_novibro'] = -abs(df['force_desired_novibro'])
    fig,ax= plt.subplots(1,1)
    ax.plot(range(3000),df['force_desired'+names_arr[0]].loc['user'+str(0)][2000:5000],'g',ls='--',label='Desired Force')
    ax.plot(range(3000),df['force_event'+names_arr[0]].loc['user'+str(0)][2000:5000],'r',label="Sensed Force")
    #ax.plot(range(3000),df['force_weiss'+names_arr[0]].loc['user'+str(0)][0:3000],label="weiss Force")
    ax.legend(loc="lower right")
    ax.set_ylabel('Force(N)')
    ax.set_xlabel('Time')
    plt.show()

    
    deltastart=df['delta_z'+names_arr[0]].loc['user'+str(0)][0]
    deltamax=np.min(df['delta_z'+names_arr[0]].loc['user'+str(0)][2000:5000]) #0.5809163702894807
    #delta_z=df.index[df['delta_z'+names_arr[0]]>deltastart]
    #df['delta_z'+names_arr[0]][delta_z]=0
    df['delta_z'+names_arr[0]]=df['delta_z'+names_arr[0]]-deltastart
    print(timee[4999])
    print(timee[2000])
    print((timee[4999]-timee[2000])/15)
    for x in range(0,1):
        figdelta,axdelta= plt.subplots(2,1)
        axdelta[1].plot(timee,df['delta_z'+names_arr[x]].loc['user'+str(0)][2000:5000]-df['delta_z'+names_arr[x]].loc['user'+str(0)][3700],'b',label='z',linewidth=3)
        axdelta[1].plot(timee,[0]*3000,'grey',ls='--',alpha=0.5)
        axdelta[1].legend(loc="lower right")
        axdelta[0].plot(timee,abs(df['force_event'+names_arr[x]].loc['user'+str(0)][2000:5000]),'r',label='Sensed Force',linewidth=3)
        axdelta[0].plot(timee,abs(df['force_desired'+names_arr[x]].loc['user'+str(0)][2000:5000]),'g',ls='--',label='Desired Force',linewidth=3)
        #axdelta[0].plot(timee[:500],df['force_weiss'+names_arr[x]].loc['user'+str(0)][3700:4200],'#077B8A',label="Weiss Force")
        axdelta[0].legend(loc="lower right")
        axdelta[0].set_title(titles[x])
        axdelta[1].set_xlabel('Time(s)')
        axdelta[1].set_ylabel('Distance(m)')
        axdelta[0].set_ylabel('Force(N)')
        for ax in axdelta:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            #ax.grid(which='minor',color='grey', axis='x', linestyle='-', linewidth=0.25, alpha=0.5)
            #ax.grid(color='grey', axis='x', linestyle='-', linewidth=1, alpha=0.7)
            ax.tick_params(axis='both', which='minor', labelsize=8)
            ax.tick_params(axis='both', which='major', labelsize=10)
    plt.show()


if robot2:
    df['force_desired_novibro'] = -abs(df['force_desired_novibro'])
    fig,ax= plt.subplots(1,1)
    ax.plot(range(3000),df['force_weiss'+names_arr[0]].loc['user'+str(0)][0:3000],'g',ls='--',label='Human Force')
    ax.plot(range(3000),df['force_robot'+names_arr[0]].loc['user'+str(0)][0:3000],'black',ls='--',label='Robot Force')
    ax.plot(range(3000),df['force_event'+names_arr[0]].loc['user'+str(0)][0:3000],'r',label="Sensed Force")
    # ax.plot(range(3000),df['force_weiss2'+names_arr[0]].loc['user'+str(0)][0:3000],'o',label="weiss2 Force")
    ax.legend(loc="lower right")
    ax.set_ylabel('Force(N)')
    ax.set_xlabel('Time')
    plt.show()

    
    deltastart=df['delta_z'+names_arr[0]].loc['user'+str(0)][0]
    deltamax=np.min(df['delta_z'+names_arr[0]].loc['user'+str(0)][2500:5500]) #0.5809163702894807

    #delta_z=df.index[df['delta_z'+names_arr[0]]>deltastart]
    #df['delta_z'+names_arr[0]][delta_z]=0
    df['delta_z'+names_arr[0]]=df['delta_z'+names_arr[0]]-deltastart
    print(timee[4999])
    print(timee[2000])
    print((timee[4999]-timee[2000])/15)
    for x in range(0,1):
        figdelta,axdelta= plt.subplots(2,1)
        axdelta[1].plot(timee[:500],df['delta_z'+names_arr[x]].loc['user'+str(0)][3700:4200]-df['delta_z'+names_arr[x]].loc['user'+str(0)][3700],'b',label='z')
        axdelta[1].plot(timee[:500],[0]*500,'grey',ls='--',alpha=0.5)
        axdelta[1].legend(loc="lower right")
        #axdelta[0].plot(timee[:500],df['force_desired'+names_arr[x]].loc['user'+str(0)][3749:4249],'g',ls='--',label='Desired Force')
        axdelta[0].plot(timee[:500],abs(df['force_robot'+names_arr[x]].loc['user'+str(0)][3700:4200]),'green',label='Robot Force')
        axdelta[0].plot(timee[:500],abs(df['force_weiss'+names_arr[x]].loc['user'+str(0)][3700:4200]),'black',label='Human Force')
        axdelta[0].plot(timee[:500],abs(df['force_event'+names_arr[x]].loc['user'+str(0)][3700:4200]),'r',label='Sensed Force')
        # axdelta[0].plot(timee[:500],df['force_weiss2'+names_arr[x]].loc['user'+str(0)][3700:4200],'#077B8A',label="Human Force")
        axdelta[0].legend(loc="lower right")
        axdelta[0].set_title(titles[x])
        axdelta[1].set_xlabel('Time(s)')
        axdelta[1].set_ylabel('Distance(m)')
        axdelta[0].set_ylabel('Force(N)')
        for ax in axdelta:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            #ax.grid(which='minor',color='grey', axis='x', linestyle='-', linewidth=0.25, alpha=0.5)
            ax.grid(color='grey', axis='x', linestyle='-', linewidth=1, alpha=0.7)
    plt.show()



#print(df['eeeeee'])
grapherror=df.index[df['force_desired_novibro']<0]
arerror=df.index[df['desire_ar_holovibro']<0]
grapherrorindex=[grapherror[0][1]]
for i in range(int(numberofpoints/2)):
    if abs(grapherror[i][1]-grapherror[i+1][1])>2:
        grapherrorindex.append(grapherror[i][1])
        grapherrorindex.append(grapherror[i+1][1])
    
grapherrorindex.append(grapherror[len(grapherror)-1][1])




arerrorindex=[arerror[0][1]]
for i in range(int(numberofpoints/2)):
    if abs(arerror[i][1]-arerror[i+1][1])>3:
        arerrorindex.append(arerror[i][1])
        if len(arerrorindex)==60:
            break
        arerrorindex.append(arerror[i+1][1])

#print(arerrorindex)
#print(len(arerrorindex))

errors=np.zeros((numoftrials*numofusers,numofmodes))

if robot:
    numofmodes=1

for i in range(numofusers):
    for j in range(numofmodes):
        count=0+i*numoftrials
        for k in range(0,2*numoftrials-1,2):
            if j<=1:
                desire=df.loc['user'+str(i)]['force_desired'+names_arr[j]][grapherrorindex[k]:grapherrorindex[k+1]]
                event=df.loc['user'+str(i)]['force_event'+names_arr[j]][grapherrorindex[k]:grapherrorindex[k+1]]
                errortemp=(((desire-event)**2).sum()/(grapherrorindex[k+1]-grapherrorindex[k]))**(1/2)
                errors[count,j]=errortemp
            else:
                desire=df.loc['user'+str(i)]['desire_ar'+names_arr[j]][arerrorindex[k]:arerrorindex[k+1]]
                event=df.loc['user'+str(i)]['sense_ar'+names_arr[j]][arerrorindex[k]:arerrorindex[k+1]]
                errortemp=(((desire-event)**2).sum()/(arerrorindex[k+1]-arerrorindex[k]))**(1/2)
                errors[count,j]=errortemp
            count+=1
#pd.DataFrame(errors).to_csv('foo2.csv')
a=[]
b=[]
for i in range(numofusers):
    a+=['user'+str(i)]*numoftrials
    b+=[i for i in range(30)]

#a=[a,[b]]
ind=pd.MultiIndex.from_arrays([a,b])
errors2=pd.DataFrame(errors,columns=names_arr, index=ind)
errors2.to_csv('foo2.csv')


ind=pd.MultiIndex.from_arrays([b,a])
errorssorted=pd.DataFrame(errors,columns=names_arr, index=ind)
errorssorted=errorssorted.sort_index()
errorssorted.to_csv('foo2sorted.csv')


#fig1.suptitle('6 Modes Each Trial Error')

for i in range(2,6):
    fig1,axs1=plt.subplots(1)
    for x in range(10,25):
        axs1.boxplot(errorssorted[names_arr[i]].loc[x],positions=[x-9],widths=0.6,showfliers=False,showmeans=True)
    axs1.set(ylabel='RMSE',xlabel='Trial')
    axs1.set_title(titles[i])
    axs1.set_ylim(0,5)
    plt.show()
    

fig2,axs2 = plt.subplots(1,1)


colors = [ '#426A8C', '#D94D1A']
novibro = dict(color=colors[0])
vibro = dict(color=colors[1])
vibnovib=[novibro,vibro]

darkcolors= ['#203446','#6c260c']
novibro2 = dict(color=darkcolors[0])
vibro2 = dict(color=darkcolors[1])
vibnovib2=[novibro2,vibro2]
errorarray=[]


colors=['#D72631','#c003ba','#077B8A','#5C3C92','#B91655','#3B4D62']
colour=[]
for i in range(len(colors)):
    colour.append(dict(color=colors[i]))


for i in range(2,numofmodes):
    a=[]
    for j in range(numofusers):
        a.append(np.mean(errors2[names_arr[i]].loc['user'+str(j)][10:25]))    
    axs2.boxplot(a,positions=[i],widths=0.5, \
    boxprops=colour[i], \
    medianprops=colour[i], \
    meanprops=colour[i], \
    whiskerprops=colour[i], \
    capprops=colour[i],showmeans=True,showfliers=False)
    errorarray.append(a) 
axs2.set_title("All errors boxplot")
axs2.set_xticklabels(titles[2:])
axs2.set_ylabel("RMSE")
axs2.spines['top'].set_visible(False)
axs2.spines['right'].set_visible(False)
axs2.spines['left'].set_visible(False)
axs2.set_ylim(1,4)
axs2.grid(color='grey', axis='y', linestyle='-', linewidth=0.2, alpha=0.8)
plt.show()



figanova,axsanova= plt.subplots(1)

axsanova.boxplot([i for i in errorarray[0]]+[i for i in errorarray[2]],positions=[1],boxprops=colour[0],medianprops=colour[0],whiskerprops=colour[0],capprops=colour[0],widths=0.5,showfliers=False,showmeans=True)                 
axsanova.boxplot([i for i in errorarray[1]]+[i for i in errorarray[3]],positions=[2],boxprops=colour[1],medianprops=colour[1],whiskerprops=colour[1],capprops=colour[1],widths=0.5,showfliers=False,showmeans=True)
axsanova.boxplot([i for i in errorarray[2]]+[i for i in errorarray[3]],positions=[3],boxprops=colour[2],medianprops=colour[2],whiskerprops=colour[2],capprops=colour[2],widths=0.5,showfliers=False,showmeans=True)
axsanova.boxplot([i for i in errorarray[0]]+[i for i in errorarray[1]],positions=[4],boxprops=colour[3],medianprops=colour[3],whiskerprops=colour[3],capprops=colour[3],widths=0.5,showfliers=False,showmeans=True)
axsanova.boxplot([i for i in errorarray[3]],positions=[5],                           boxprops=colour[4],medianprops=colour[4],whiskerprops=colour[4],capprops=colour[4],widths=0.5,showfliers=False,showmeans=True)
axsanova.boxplot([i for i in errorarray[1]],positions=[6],                           boxprops=colour[5],medianprops=colour[5],whiskerprops=colour[5],capprops=colour[5],widths=0.5,showfliers=False,showmeans=True)
axsanova.set_xticklabels(['novib','vib','noobstacle','obstacle','novib noobs','vib obs'])
axsanova.set_ylabel('RMSE')
axsanova.set_title('Two way ANOVA test')
axsanova.spines['top'].set_visible(False)
axsanova.spines['right'].set_visible(False)
axsanova.spines['left'].set_visible(False)
axsanova.grid(color='grey', axis='y', linestyle='-', linewidth=0.25, alpha=0.5)
axsanova.set_ylim(1,4)

plt.show()





array=[]
for i in range(numofmodes):
    array.append(list(errorssorted[names_arr[i]].loc[9:23]))

a=[]
vibronovibro=['novibro','vibro']
for i in range(numofmodes):
    a.append([vibronovibro[i%2]]*len(array[i]))

modenames=['graph','pass','holo','pass','all']
dfarray=[]
for i in range(0,6,2):
    df_aov=pd.DataFrame(list(zip(array[i]+array[i+1],a[i]+a[i+1])),columns=['error','mode'])
    df_aov.to_csv(modenames[i]+'.csv',index=False)
    dfarray.append(df_aov)

for i in range(3):
    aov=pg.anova(dv='error', between='mode',data=dfarray[i],detailed=True)
    print(aov)

#for i in range(3):
#    aov=pg.welch_anova(dv='error', between='mode',data=dfarray[i])
#    print(aov)

array2=[item for sublist in array for item in sublist ]
a2=[item for sublist in a for item in sublist]

mode2names=['graph']*300
temp=['AR']*600
mode2names=mode2names+temp


df_aov2=pd.DataFrame(list(zip(array2,a2,mode2names)),columns=['error','mode','mode2']).round(3)
df_aov2.to_csv('aov2.csv',index=False)
aov2=pg.anova(dv='error',between=['mode','mode2'],data=df_aov2,detailed=True)
print(aov2)


array3=[item for sublist in array[2:6] for item in sublist ]
a3=[item for sublist in a[2:6] for item in sublist]

mode3names=['with_obs']*300
temp=['without_obs']*600
mode3names=mode3names+temp

df_aov3=pd.DataFrame(list(zip(array3,a3,mode3names)),columns=['error','vibrations','obstacle']).round(3)
df_aov3.to_csv('aov3.csv',index=False)
aov3=pg.anova(dv='error',between=['vibrations','obstacle'],data=df_aov3,detailed=True)
print(aov3)




'''
figanova,axsanova= plt.subplots(1)
                 
axsanova.boxplot([i for i in errorarray[2]],positions=[1],boxprops=colour[2],medianprops=colour[2],meanprops=colour[2],whiskerprops=colour[2],capprops=colour[2])
axsanova.boxplot([i for i in errorarray[3]],positions=[2],boxprops=colour[3],medianprops=colour[3],meanprops=colour[3],whiskerprops=colour[3],capprops=colour[3])
axsanova.boxplot([i for i in errorarray[4]],positions=[3],boxprops=colour[4],medianprops=colour[4],meanprops=colour[4],whiskerprops=colour[4],capprops=colour[4])
axsanova.boxplot([i for i in errorarray[5]],positions=[4],boxprops=colour[5],medianprops=colour[5],meanprops=colour[5],whiskerprops=colour[5],capprops=colour[5])
axsanova.set_xticklabels(['novib obs','vib obs','novib clear','vib cear'])
axsanova.set_ylabel('RMSE')
axsanova.set_title('Two way ANOVA test')
axsanova.spines['top'].set_visible(False)
axsanova.spines['right'].set_visible(False)
axsanova.spines['left'].set_visible(False)
axsanova.grid(color='grey', axis='y', linestyle='-', linewidth=0.25, alpha=0.5)
axsanova.set_ylim(1,4)

plt.show()
'''


#a=[]
#print(a[1])

'''
#Normalized
for i in range(numofmodes):
    for j in range(numofusers):
        max=np.max(errors2[names_arr[i]].loc['user'+str(j)])
        errors2[names_arr[i]].loc['user'+str(j)]=np.array(errors2[names_arr[i]].loc['user'+str(j)])/max

errors2.to_csv('foonormalize.csv')

errorssorted=pd.DataFrame(errors,columns=names_arr, index=ind)
errorssorted=errorssorted.sort_index()
errorssorted.to_csv('foo2sortednorm.csv')

fig3,axs3=plt.subplots(3,2)
fig3.suptitle('All errors Normalized')
i=0
for ax in axs3.flat:
    for x in range(numoftrials):
        ax.boxplot(errorssorted[names_arr[i]].loc[x],positions=[x-9])
    ax.set(xlabel='trial',ylabel='RMSE')
    ax.set_title(titles[i])
    ax.set_ylim(0,5)
    i+=1

fig4,axs4 = plt.subplots(1,1)
i=0
for i in range(numofmodes):
    a=[]
    for j in range(numofusers):
        a.append(np.mean(errors2[names_arr[i]].loc['user'+str(j)]))
    axs4.boxplot(a,positions=[i],widths=0.8) #,positions=names_arr
axs4.set_title("All errors mean Normalized")
axs4.set_xticklabels(names_arr)
plt.show()
'''
'''
#event vs desired force for each user
for i in range(numofusers):
    figuser,axsuser = plt.subplots(3,2)
    j=0
    for ax in axsuser.flat:
        if j<=1:
            ax.plot(range(int(numberofpoints/2+1)),df['force_desired'+names_arr[j]].loc['user'+str(i)][2000:5000],'g',ls='--')
            ax.plot(range(int(numberofpoints/2+1)),df['force_event'+names_arr[j]].loc['user'+str(i)][2000:5000],'r')
        else:
            ax.plot(range(int(numberofpoints/2+1)),df['desire_ar'+names_arr[j]].loc['user'+str(i)][2000:5000],'g')
            ax.plot(range(int(numberofpoints/2+1)),df['sense_ar'+names_arr[j]].loc['user'+str(i)][2000:5000],'r')
        ax.set_title(titles[j])
        ax.set_ylabel('Force(N)')
        j+=1
plt.show()
'''
for i in range(numofmodes):
    positive=df.index[df['force_weiss'+names_arr[i]]>0]
    df['force_weiss'+names_arr[i]][positive]=0

for i in range(9,10):
    for x in range(6):
        figuser,axsuser = plt.subplots(1,1)
        

        if x<=1:
            axsuser.plot(timee,abs(df['force_desired'+names_arr[x]].loc['user'+str(i)][2000:5000]),'g',ls='--',label='Desired Force')
            axsuser.plot(timee,abs(df['force_event'+names_arr[x]].loc['user'+str(i)][2000:5000]),'r', label='Sensor Force')
            axsuser.plot(timee,abs(df['force_weiss'+names_arr[x]].loc['user'+str(i)][2000:5000]),'b',alpha=0.5,label='Weiss Force')
        else:
            axsuser.plot(timee[:1500],abs(df['desire_ar'+names_arr[x]].loc['user'+str(i)][3500:5000]),'g',label='Desired Force',linewidth=4)
            axsuser.plot(timee[:1500],abs(df['sense_ar'+names_arr[x]].loc['user'+str(i)][3500:5000]),'r', label='Sensor Force',linewidth=4)
            axsuser.plot(timee[:1500],abs(df['force_weiss'+names_arr[x]].loc['user'+str(i)][3500:5000]),'b',alpha=0.5,label='Weiss Force',linewidth=4)
        axsuser.set_title(titles[x]+str(i+1))
        axsuser.set_ylabel('Force(N)')
        axsuser.set_xlabel('Time(s)')
        axsuser.spines['top'].set_visible(False)
        axsuser.spines['right'].set_visible(False)
        axsuser.spines['left'].set_visible(False)
        #axsuser.grid(color='grey', axis='x', linestyle='-', linewidth=1, alpha=0.7)
        axsuser.legend(loc="lower right")
            

    plt.show()



#weiss_force

fig5,axs5 = plt.subplots(1,1)

for i in range(2,numofmodes):
    a=[]
    for j in range(numofusers):
        z=[]

        for x in df['force_weiss'+names_arr[i]].loc['user'+str(j)][2000:5000]:
            if x<0:
                z.append(abs(x))
        a.append(np.mean(z))
    axs5.boxplot(a,positions=[i],widths=0.4,showmeans=True,boxprops=colour[i],medianprops=colour[i],meanprops=colour[i],whiskerprops=colour[i],capprops=colour[i])
axs5.set_title("Weiss Mean Force of Each Mode")
axs5.set_xticklabels(titles[2:])
axs5.spines['top'].set_visible(False)
axs5.spines['right'].set_visible(False)
axs5.spines['left'].set_visible(False)
axs5.grid(color='grey', axis='y', linestyle='-', linewidth=0.25, alpha=0.5)
axs5.set_ylabel('Force(N)')
axs5.set_ylim(3,15)

plt.show()














