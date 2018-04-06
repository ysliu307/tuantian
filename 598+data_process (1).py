
# coding: utf-8

# In[26]:


import numpy as np
import csv
k=0
Q = open('sort_data.txt','w')
with open('u.data','r') as s:
    data = s.readlines()
    for line in sorted(data, key = lambda line: (int(str(line.split('\t')[0])), int(str(line.split('\t')[3])))):
        Q.write(line)
Q.close()



# In[27]:


#time = np.sort(time)
U=0
k=0
count_user=0
count=0
with open('sort_data.txt', 'r') as g:
    data1 =g.readlines()
    D1=data1[0].split('\t')
    id_former=int(D1[0])
    count_user_former=0
    train_file = open('train_data.tsv', 'w')
    test_file = open('test_data.tsv', 'w')
    while(U<943):
        D=data1[k].split('\t')
        if len(D)!=4:
            continue
        current_id=int(D[0])
        if(current_id!=id_former):
           # print(current_id)
            count_user_train =count_user_former+ int(count * 0.9)
            m = -1
            w = -1
            for j in range(count_user_former, count_user_train):
                Dp=data1[j].split('\t')
                if(int(Dp[2])>=3):
                    m = 1
                if(int(Dp[2])<3):
                    m = 0
                train_file.write("%s %s %s\n" %(Dp[0], Dp[1], m))
            for p in range(count_user_train,count_user):
                Dp=data1[j].split('\t')
                if(int(Dp[2])>=3):
                    w = 1
                if(int(Dp[2])<3):
                    w = 0
                test_file.write("%s %s %s\n" %(Dp[0], Dp[1], w))
            id_former=current_id
            U=U+1 
            count_user_former = count_user
            count=0
        k+=1
        count_user+=1
        count+=1
        if(k==len(data1)):
            break
train_file.close()
test_file.close()


# In[28]:


#time = np.sort(time)
U=0
k=0
count_user=0
count=0
with open('sort_data.txt', 'r') as g:
    data1 =g.readlines()
    D1=data1[0].split('\t')
    id_former=int(D1[0])
    count_user_former=0
    train100_file = open('train100_data.tsv', 'w')
    test100_file = open('test100_data.tsv', 'w')
    while(U<100):
        D=data1[k].split('\t')
        if len(D)!=4:
            continue
        current_id=int(D[0])
        if(current_id!=id_former):
           # print(current_id)
            count_user_train =count_user_former+ int(count * 0.9)
            m = -1
            w = -1
            for j in range(count_user_former, count_user_train):
                Dp=data1[j].split('\t')
                if(int(Dp[2])>=3):
                    m = 1
                if(int(Dp[2])<3):
                    m = 0
                train100_file.write("%s %s %s\n" %(Dp[0], Dp[1], m))
            for p in range(count_user_train,count_user):
                Dp=data1[j].split('\t')
                if(int(Dp[2])>=3):
                    w = 1
                if(int(Dp[2])<3):
                    w = 0
                test100_file.write("%s %s %s\n" %(Dp[0], Dp[1], w))
            id_former=current_id
            U=U+1 
            count_user_former = count_user
            count=0
        k+=1
        count_user+=1
        count+=1
        if(k==len(data1)):
            break
train100_file.close()
test100_file.close()


# In[29]:


import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
#we don't want to show the data in scientific type
np.set_printoptions(suppress=True)

