#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

df = pd.read_csv("local-data/wifi_map_6-10-2025_19_19_26_home_consum.csv", sep=";")

times = df["Time from start (seconds)"].unique()

# splitting the data base on same moment adquisition
subsets = []
for tm in times:
    sub = df.loc[df["Time from start (seconds)"] == tm]
    subsets.append(sub)
subsets[0]


# In[2]:


# get an array holding all the nearest APs
nearests_uniq = []
for sub in subsets:
    ap_hash = sub.iloc[0, 0]
    if len(nearests_uniq) == 0:
        nearests_uniq.append(ap_hash)
    else:
        if ap_hash not in nearests_uniq:
            nearests_uniq.append(ap_hash)
nearests_uniq


# In[3]:


# get all data related with the nearest APs
interest_aps = []
for closer in nearests_uniq:
    interest_aps.append(df.loc[df["AP hash"] == closer])
interest_aps


# In[30]:


# calculating the total distance walked

walked_distance = 0
time = 0
for i, aps in enumerate(interest_aps):
    if i == 0:
        walked_distance += interest_aps[i].tail(1).iloc[0, 1]
        time = interest_aps[i].tail(1).iloc[0, 3]
    else:
        row = interest_aps[i].loc[df["Time from start (seconds)"] == time]
        if not row.empty:
            latest_row = interest_aps[i].tail(1)
            time = latest_row.iloc[0, 3]
            start_dst = row.iloc[0, 1]
            end_dst = latest_row.iloc[0, 1]
            delta_dst = abs(start_dst - end_dst)
            walked_distance += delta_dst
            if len(interest_aps) - 1 == i:
                walked_distance += end_dst

(walked_distance, time)


# In[5]:


# drawing for the revelant APs the distance on time
# commented since seems that is very memory consuming

# for i_ap in interest_aps:
#     i_ap.plot.scatter(
#     x="Time from start (seconds)",
#     y="Distance (meters)",
#     grid=True,
#     title=i_ap.iloc[0,0],
#     figsize=(2,3))


# In[6]:


# drawing for the revelant AP the distance on time
i = 4
interest_aps[i].plot.scatter(
    x="Time from start (seconds)",
    y="Distance (meters)",
    grid=True,
    title=interest_aps[i].iloc[0, 0],
    figsize=(2, 3),
)


# In[7]:


# number of different APs
df["AP hash"].unique().size


# In[8]:


df.drop_duplicates(subset="AP hash").plot.scatter(x="AP hash", y="AP auth mode")


# In[9]:


# open auth mode APs
odf = df.loc[df["AP auth mode"] == 0]
odf.drop_duplicates(subset="AP hash")
