#!/usr/bin/env python
# coding: utf-8

# In[110]:


import docplex.mp.model as cpx
import networkx as nx
import pandas as pd 
import matplotlib.pyplot as plt
from math import sqrt
import networkx as nx
from matplotlib.pyplot import figure


# In[120]:


location = 'C:/Users/dell pc/Desktop/Sem 8/INDR460-OPERATIONS RESEARCH APPLICATIONS/assignments/assignment 5/TSPdata.xlsx'
df_r =pd.read_excel(location,sheetname='Sheet3',header=None,skiprows=2)
lat = df_r[1].tolist()
long = df_r[2].tolist()
# df_r
df_r[0].tolist()
len(df_r[0].tolist())


# In[121]:


class MyClass(object):
    def __init__(self,n_id, lat,long):
        self.n_id = n_id
        self.lat = lat
        self.long = long  

my_objects = [] 


# In[122]:


for i in range(len(df_r[0].tolist())):
    my_objects.append(MyClass(df_r[0].tolist()[i],df_r[1].tolist()[i],df_r[2].tolist()[i]))

#my_objects[14].long
t_n = len(df_r[0].tolist())


# In[123]:


cij = [[0 for i in range(t_n)] for j in range(t_n)]
for i in range(t_n):
     for j in range(t_n):
         cij[i][j] = abs(sqrt((my_objects[i].lat-my_objects[j].lat)**2 + (my_objects[i].long-my_objects[j].long)**2))  


# In[124]:


G = nx.Graph()
G.add_nodes_from(range(t_n))
for i in range(t_n):
    for j in range(t_n):
             G.add_edge(i, j, length=cij[i][j])


# In[125]:


figure(num=None, figsize=(10, 10), dpi=80, facecolor='w', edgecolor='k')
# nx.draw(G,with_labels=True,pos=nx.circular_layout(G))
nx.draw(G,with_labels=True)
fig= plt.figure(figsize=(60,30))
plt.show()


# In[126]:


temp_G = G.copy()
temp_G.remove_node(0)
all_p_edges = [cij[0][j] for j in range(t_n)]
#all_p_edges
sorted(all_p_edges)[1] + sorted(all_p_edges)[2]


# In[127]:


all_sum_weights = []
for node in range(t_n):
    temp_G = G.copy()
    temp_G.remove_node(node)
    a = nx.minimum_spanning_edges(temp_G,weight='length')
    sum_weights = 0
    all_p_edges = [cij[node][j] for j in range(t_n)]
    for i in a:
        sum_weights = sum_weights +  i[2]['length']
    all_p_edges = [cij[node][j] for j in range(t_n)]
    #all_p_edges
    sum_weights = sorted(all_p_edges)[1] + sorted(all_p_edges)[2] + sum_weights
    all_sum_weights.append(sum_weights)
    #print(sum_weights)

print('The best 1-Tree lower bound :', sorted(all_sum_weights)[t_n-1])



# In[128]:


figure(num=None, figsize=(10, 10), dpi=80, facecolor='w', edgecolor='k')
# nx.draw(G,with_labels=True,pos=nx.circular_layout(G))
nx.draw(min_G,with_labels=True)
fig= plt.figure(figsize=(60,30))
plt.show()


# In[ ]:





# In[ ]:




