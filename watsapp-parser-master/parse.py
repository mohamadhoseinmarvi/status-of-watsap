from numpy import *
import datetime as dt
import string
import re
import time
import pandas as pd

f = open('kuwb-chats.txt', 'r')
d = f.readlines()
d = [i.strip() for i in d]
sz = len(d)
df = pd.DataFrame(columns=['dtime', 'name', 'message'])

tic = time.time()
count = 0
failCount = 0
for i in range(sz):
    if (i%500 == 0): print i
    line = d[i]
    spaces = [m.start() for m in re.finditer(' ',line)]

    try:
      dtim_tmp = line[:spaces[2]-1]
      dtim_st = dt.datetime.strptime(dtim_tmp,"%m/%d/%y, %H:%M")
      name_st = line[spaces[3]+1:spaces[4]-1]
      name_st_scrubbed = ''.join(e for e in name_st if e.isalnum())
      # if (name_st_scrubbed.equals("Jo")):
      #   print "name: %s" %name_st_scrubbed
      mess_st =  line[spaces[4]+1:]
      df.loc[i] = [dtim_st,name_st_scrubbed,mess_st]
      count=+count
    except:
      print "line %s is misbehaving" %line
      failCount=+failCount

print time.time() - tic
print "lines read: %d" %count
print "line failed: %d" %failCount
df.to_pickle('batooro.pkl')



