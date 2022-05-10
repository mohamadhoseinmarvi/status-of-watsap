
# from numpy import *
# import matplotlib
# get_ipython().magic(u'matplotlib inline')
# import matplotlib.pyplot as plt
from pylab import *
import datetime as dt
import string
import re
import time
import pandas as pd
import pickle

def txtsplit(tst):
    ''' Function to split a message line into its components 
        (day,time,name,message)
    '''
    h1 = tst.index(',')
    h2 = tst.index('-',h1)
    h3 = tst.index(':',h2)
    date = tst[:h1].strip()
    time = tst[h1+1:h2].strip()
    name = tst[h2+1:h3].strip()
    message = tst[h3+1:].strip()
    return ([date,time,name,message])

emoticons = set(range(int('1f600',16), int('1f650', 16)))


# OPEN WHATSAPP LOG
f = open('whatsapp_nathalie.txt','r')
d = f.readlines()
sz = len(d)


# CONSOLIDATE MULTI-LINE MESSAGES
bad = [not((len(d[i]) > 15) and ((d[i][1]=='/') or (d[i][2]=='/'))) for i in range(sz)]
dat = []
for i in range(sz):
    flag = (len(d[i]) > 15) and ((d[i][1]=='/') or (d[i][2]=='/'))
    if (flag == 1):
        dat.append(d[i])
    else:
        dat[-1] = dat[-1].rstrip() + ' ' + d[i]
dat = [k.strip() for k in dat]    
# print len(d),sum(bad),len(dat), sum(bad) + len(dat)
print 'Total number of messages: ', len(dat)

lend = len(dat)


# SAVE ALL MESSAGES INTO A DATAFRAME.
# PRINT PROGRESS AS YOU RUN
print 'creating dataframe ...'
df = pd.DataFrame(columns=['dtime', 'name','message'])

for i in range(lend):
    if (i%500 == 0): 
        print i 
    txt = txtsplit(dat[i])
    dtim_tmp = ' '.join(txt[:2])
    dtim_st = dt.datetime.strptime(dtim_tmp,"%m/%d/%y %I:%M %p")
    
    df.loc[i] = [dtim_st,txt[2],txt[3]]

print 'Done ...'
# PRINT CONTACT NAMES
names = unique(df['name'])
print names


# NUMBER OF MESSAGES PER CONTACT
plt.figure(1)
nmes = df.name.value_counts()
nmes.plot(kind='bar',title='Number of messages',rot=True);



# NUMBER OF IMAGES SENT PER CONTACT
plt.figure()
p1 = df.loc[df.message == '<Media omitted>',['name']]
p2 = p1.name.value_counts()
p3 = [p2[i]*100.0/nmes[i] for i in names]
p4 = pd.Series(p3, index=names)
p2.plot(kind='bar',title='Number of messages with pictures',rot=True);


# NUMBER OF LINKS PER CONTACT
plt.figure()
q1 = df.loc[['http' in ms for ms in df.message],:]
q2 = q1.name.value_counts()
q3 = [q2[i]*100.0/nmes[i] for i in names]
q4 = pd.Series(q3, index=names)
q2.plot(kind='bar',title='Number of messages with links',rot=True)


# NUMBER OF MESSAGES WITH 'lol' PER CONTACT
plt.figure()
w1 = df.loc[['lol' in ms.lower() for ms in df.message],:]
w2 = w1.name.value_counts()
w3 = [w2[i]*100.0/nmes[i] for i in names]
w4 = pd.Series(w3, index=names)
w2.plot(kind='bar',title='Number of messages with "lol"',rot=True);


# NUMBER OF MESSAGES WITH 'kk' PER CONTACT
plt.figure()
y1 = df.loc[['kk' in ms.lower() for ms in df.message],:]
y2 = y1.name.value_counts()
y3 = [y2[i]*100.0/nmes[i] for i in names]
y4 = pd.Series(y3, index=names)
y2.plot(kind='bar',title='Number of messages with "kk"',rot=True);


# NUMBER OF MESSAGES WITH '!' PER CONTACT
plt.figure()
s1 = df.loc[['!' in ms for ms in df.message],:]
s2 = s1.name.value_counts()
s3 = [s2[i]*100.0/nmes[i] for i in names]
s4 = pd.Series(s3, index=names)
s2.plot(kind='bar',title='Number of messages with ! (regardless of repetition)',rot=True);


# PERCENTAGE OF MESSAGES PER DAY PER CONTACT
plt.figure()
dow= ['M','Tu','W','Th','F','Sa','Su']
sz = len(df)
nbr_users = len(names)
dtmat = zeros((nbr_users,7))
names = list(df.name.unique())
for i in range(sz):
    dtmp = df.dtime[i].dayofweek
    ntmp = names.index(df.name[i])
    dtmat[ntmp,dtmp] += 1
# transpose this so that we can compare days from each users        
dtmat = dtmat.transpose()
dowf = pd.DataFrame()
for i in range(nbr_users):
    dtmat[:,i] = dtmat[:,i]*100.0/nmes[names[i]]
    dowf[names[i]] = dtmat[:,i]

dowf.index = dow
dowf.plot.bar(legend=True,title='% of messages per user per day',rot=True)



# TIME SERIES OF MESSAGES PER USER OVERTIME
plt.figure()
tic = min(df.dtime).date()
toc = max(df.dtime).date()
drange = pd.date_range(start=tic,end=toc)
ndays = len(drange)
ppd = zeros((ndays,nbr_users))
for i in range(ndays):
    tmp = df.loc[df.dtime < drange[i]]
    for j in range(nbr_users):
        ppd[i,j] = sum(tmp.name == names[j])

ppdf = pd.DataFrame(data=ppd, index = drange, columns=names)
ppdf.plot(title='Number of messages over time per person',rot=True,grid=True)


# AVERAGE LENGTH OF MESSAGES PER CONTACT
plt.figure()
mean_length = [0]* nbr_users
for i in range(nbr_users):
    mean_length[i] = mean([len(m) for m in df.loc[df.name == names[i]].message])

b2 = pd.Series(mean_length, index=names)    

b2.plot(kind='bar',title='Average message length',rot=True,grid=1);
ylim([0,100])



plt.show()
