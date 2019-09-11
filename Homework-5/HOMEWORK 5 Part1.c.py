#!/usr/bin/env python
# coding: utf-8
# In[11]:
import docplex.mp.model as cpx
import networkx as nx
import pandas as pd 
import matplotlib.pyplot as plt
from math import sqrt
import networkx as nx
# In[12]:
t_n = 5
cij = [[0,55,105,80,60],[60,0,75,60,75],[110,90,0,195,135],[80,60,175,0,85],[60,75,120,80,0]]
cij
# In[13]:
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

# In[14]:
opt_model.minimize(opt_model.sum(xij[i,j]*cij[i][j] for i in range(t_n) for j in range(t_n)))
url = 'https://api-oaas.docloud.ibmcloud.com/job_manager/rest/v1/'
key = 'api_555476e8-b9e9-4d02-a523-cd50d8bbd4d5'
# In[15]:
for it in  range(20):
    s = opt_model.solve(url=url,key=key)
    G = nx.DiGraph()
    G.add_nodes_from(range(t_n))
    for i in range(t_n):
        for j in range(t_n):
            if xij[i,j].solution_value == 1:
                #print(i,j)
                G.add_edge(i,j)


        #if it >= 1:
    #a = nx.find_cycle(G)
    a_list = list(nx.simple_cycles(G))
    if len(a_list) == 1:
        break
    for a_it in range(len(a_list)-1):
        k = a_list[a_it]
        print(k)
        # nx.find_cycle(G)
        #k = [a[i][0] for i in range(len(a))]
        a_n = list(range(t_n))
        for i in k:
            a_n.remove(i)
        opt_model.add_constraint(opt_model.sum(xij[k[i],j] for i in range(len(k)) for j in a_n) == 1)
            
####################################################################################################################

# In[19]:
from matplotlib.pyplot import figure
figure(num=None, figsize=(10, 10), dpi=80, facecolor='w', edgecolor='k')
# nx.draw(G,with_labels=True,pos=nx.circular_layout(G))
nx.draw(G,with_labels=True)
fig= plt.figure(figsize=(60,30))
plt.show()

# In[17]:
opt_model.print_solution()
print('Min path would be the objective')

# In[ ]:




