#!/usr/bin/env python
# coding: utf-8

# In[33]:


get_ipython().run_line_magic('reset', '')
from docplex.mp.model import Model
import networkx as nx
import pandas as pd 
import matplotlib.pyplot as plt


# In[34]:


location = 'C:/Users/dell pc/Desktop/Sem 8/INDR460-OPERATIONS RESEARCH APPLICATIONS/assignments/assignment 3/CaliforniaData_for_code.xlsx'
df_c = pd.read_excel(location,sheetname='Sheet1',header=None)
df_r =pd.read_excel(location,sheetname='CaliforniaData',header=None,skiprows=2)
df_r_n =pd.read_excel(location,sheetname='Sheet4',header=None,skiprows=2)
df_r_p =pd.read_excel(location,sheetname='Sheet5',header=None,skiprows=2)


# In[35]:


class O_D(object):
    def __init__(self,number, origin,destination,distance,flow):
        self.number = number
        self.origin = origin
        self.destination = destination
        self.distance = distance
        self.flow = flow
    def find_sp(self,sp):
        self.sp = sp
    def find_sd(self,sd):
        self.sd = sd
    def vector_p(cls):
        v_p = [0]*339
        for i in cls.sp:
            v_p[i] = 1
        cls.v_p = v_p  

class A_T(object):
    def __init__(self,number, arc_h,arc_t,length):
        self.number = number
        self.arc_h = arc_h
        self.arc_t = arc_t
        self.length = length

class Population(object):
    def __init__(self,number,city,population):
        self.number = number
        self.city = city
        self.population = population       
       
OD_infor = []
AT_infor = []
Population_infor = []


for i in range(len(df_r[0])):
    OD_infor.append(O_D(df_r[0].tolist()[i],df_r[1].tolist()[i],df_r[2].tolist()[i],df_r[3].tolist()[i],df_r[4].tolist()[i]))

for i in range(len(df_r_n[0])):
    AT_infor.append(A_T(df_r_n[0].tolist()[i],df_r_n[1].tolist()[i],df_r_n[2].tolist()[i],df_r_n[3].tolist()[i]))

for i in range(len(df_r_p[0])):
    Population_infor.append(Population(df_r_p[0].tolist()[i],df_r_p[1].tolist()[i],df_r_p[2].tolist()[i]))
    
print(len(OD_infor))
print(len(AT_infor))
print(Population_infor[50].city)


# In[36]:


X = nx.Graph()
for obj in AT_infor:
    X.add_node(obj.arc_h)
    X.add_node(obj.arc_t)
    X.add_edge(obj.arc_h, obj.arc_t, length=obj.length)
    
for obj in Population_infor:
    nx.set_node_attributes(X,{obj.city:{'population':obj.population}})


# In[37]:


for obj in OD_infor:
    obj.find_sp(nx.dijkstra_path(X,obj.origin,obj.destination,weight='length'))
    obj.find_sd(nx.dijkstra_path_length(X,obj.origin,obj.destination,weight='length'))
    obj.vector_p();


# In[38]:


cost_value = [1]*339
for i in range(len(Population_infor)):
    if Population_infor[i].population > 100000:
        cost_value[Population_infor[i].city] = 3
    else:
        cost_value[Population_infor[i].city] = 2


# In[39]:


import docplex.mp.model as cpx
opt_model = cpx.Model(name="MIP Model")
b_v_x = opt_model.binary_var_list(339, name='x')
b_v_y = opt_model.binary_var_list(len(OD_infor)+1, name='y')

for obj in OD_infor:
    opt_model.add_constraint(opt_model.sum(opt_model.scal_prod(b_v_x,obj.v_p)) >= b_v_y[obj.number])
    
for i in range(1,len(OD_infor)+1):
    opt_model.add_constraint(b_v_y[i] == 1)
    
opt_model.minimize(opt_model.sum(b_v_x))


# In[40]:


url = 'https://api-oaas.docloud.ibmcloud.com/job_manager/rest/v1/'
key = 'api_555476e8-b9e9-4d02-a523-cd50d8bbd4d5'
s = opt_model.solve(url=url,key=key)


# In[41]:


total_trip = 0;
for elements in b_v_y:
    if elements.solution_value != 0:
        total_trip = total_trip+1
print('total trip = ', total_trip)
print('objective_value = ',opt_model.objective_value)
        


# In[44]:


print('decesion variables corresponding to fast charge locations are:')
for elements in b_v_x:
    if elements.solution_value != 0:
        print(elements)


# In[ ]:




