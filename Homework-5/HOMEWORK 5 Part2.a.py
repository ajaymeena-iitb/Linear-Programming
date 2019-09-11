#!/usr/bin/env python
# coding: utf-8

# In[36]:


import docplex.mp.model as cpx
import networkx as nx
import pandas as pd 
import matplotlib.pyplot as plt
from math import sqrt
import networkx as nx


# In[88]:


location = 'C:/Users/dell pc/Desktop/Sem 8/INDR460-OPERATIONS RESEARCH APPLICATIONS/assignments/assignment 5/TSPdata.xlsx'
df_r =pd.read_excel(location,sheetname='Sheet3',header=None,skiprows=2)
lat = df_r[1].tolist()
long = df_r[2].tolist()
# df_r
df_r[0].tolist()
len(df_r[0].tolist())


# In[89]:


class MyClass(object):
    def __init__(self,n_id, lat,long):
        self.n_id = n_id
        self.lat = lat
        self.long = long  

my_objects = [] 


# In[90]:


for i in range(len(df_r[0].tolist())):
    my_objects.append(MyClass(df_r[0].tolist()[i],df_r[1].tolist()[i],df_r[2].tolist()[i]))

#my_objects[14].long
t_n = len(df_r[0].tolist())


# In[91]:


cij = [[0 for i in range(t_n)] for j in range(t_n)]
for i in range(t_n):
     for j in range(t_n):
         cij[i][j] = abs(sqrt((my_objects[i].lat-my_objects[j].lat)**2 + (my_objects[i].long-my_objects[j].long)**2))  


# In[92]:


opt_model = cpx.Model(name="MIP Model")
xij = opt_model.binary_var_matrix(t_n, t_n)

for i in range(t_n):
    opt_model.add_constraint(xij[i,i] == 0)
for i in range(t_n):
#     print(obj.number)
    opt_model.add_constraint(opt_model.sum(xij[i,j] for j in range(t_n)) == 1)
    
for i in range(t_n):
#     print(obj.number)
    opt_model.add_constraint(opt_model.sum(xij[j,i] for j in range(t_n)) == 1)


# In[93]:


opt_model.minimize(opt_model.sum(xij[i,j]*cij[i][j] for i in range(t_n) for j in range(t_n)))
url = 'https://api-oaas.docloud.ibmcloud.com/job_manager/rest/v1/'
key = 'api_555476e8-b9e9-4d02-a523-cd50d8bbd4d5'
k_n = 0


# In[94]:


for it in  range(20):
    s = opt_model.solve(url=url,key=key)
    G = nx.DiGraph()
    G.add_nodes_from(range(t_n))
    for i in range(t_n):
        for j in range(t_n):
            if xij[i,j].solution_value == 1:
                #print(i,j)
                G.add_edge(i,j)


      
    a_list = list(nx.simple_cycles(G))
    if len(a_list) == 1:
        break
    for a_it in range(len(a_list)-1):
        k = a_list[a_it]
        print(k)
        k_n = k_n +1
        a_n = list(range(t_n))
        for i in k:
            a_n.remove(i)
        opt_model.add_constraint(opt_model.sum(xij[k[i],j] for i in range(len(k)) for j in a_n) == 1)
            
####################################################################################################################
   


# In[95]:


from matplotlib.pyplot import figure
figure(num=None, figsize=(10, 10), dpi=80, facecolor='w', edgecolor='k')
# nx.draw(G,with_labels=True,pos=nx.circular_layout(G))
nx.draw(G,with_labels=True)
fig= plt.figure(figsize=(60,30))
plt.show()


# In[107]:


print("The minimum distance tour is objective")
print("The number of cut", k_n)
opt_model.print_solution()


# In[ ]:





# In[ ]:




