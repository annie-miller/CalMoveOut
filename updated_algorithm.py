#!/usr/bin/env python
# coding: utf-8

# In[6]:


#import libraries
import csv
import pandas as pd
from geopy.geocoders import Nominatim


# In[7]:


# read in data
data = pd.read_csv('addresses.csv')
data


# In[3]:


#clean data
data = data.rename(columns = {'Are you available for pickup on Friday, May 20th from 9am-12pm?':'20th am', 'Are you available for pickup on Friday, May 20th from 1-4pm?':'20th pm', 'Are you available for pickup on Saturday, May 21st from 9am-12pm?':'21st am', 'Are you available for pickup on Saturday, May 21st from 1-4pm?':'21st pm', 'Are you available for pickup on Friday, May 27th from 9am-12pm?':'27th am','Are you available for pickup on Friday, May 27th from 1-4pm?':'27th pm', 'Are you available for pickup on Saturday, May 28th from 9am-12pm?':'28th am', 'Are you available for pickup on Saturday, May 28th from 1-4pm?':'28th pm'}, inplace = True)
days = ['20th am', '20th pm', '21st am', '21st pm', '27th am', '27th pm', '28th am', '28th pm']
selected = ['Name', 'Address Line 1', 'Address Line 2', 'City', 'Zip', 'Number of Items']+ days

display(data)
#new_data = data[selected]


# In[20]:


#make full address and select number of pickups
num_pickups = 104
new_data['address'] = new_data['Address Line 1'] + ', '+ new_data['City']
#new_data = new_data.drop([20, 32, 50], axis = 0)
new_data = new_data.iloc[:num_pickups]
new_data


# In[21]:


#convert dates
for row in days:
    new_data[row] = [1 if x == 'yes' else 0 for x in new_data[row].values]
    

#create numeric indicator for availability
new_data['sum'] = new_data['20th am'] + new_data['20th pm'] + new_data['21st am'] + new_data['21st pm'] + new_data['27th am'] + new_data['27th pm'] + new_data['28th am'] + new_data['28th pm']
new_data


# In[9]:


geolocator = Nominatim(user_agent="example app")

addresses = new_data['address'].values


# In[23]:


coordinates = []

for i in range(0,num_pickups):
    location = geolocator.geocode(addresses[i])
    coordinates += [[location.point.latitude, location.point.longitude]]

#add coordinates column to dataframe

new_data['coordinates'] = coordinates


# In[24]:


#start groups + add people with only one time slot
one = new_data[new_data['sum'] == 1]
data_no_one = new_data.drop(one.index, axis = 0)


first_fri_am = one[one['20th am'] == 1]
first_fri_pm = one[one['20th pm'] == 1]
first_sat_am = one[one['21st am'] == 1]
first_sat_pm = one[one['21st pm'] == 1]
sec_fri_am = one[one['27th am'] == 1]
sec_fri_pm = one[one['27th pm'] == 1]
sec_sat_am = one[one['28th am'] == 1]
sec_sat_pm = one[one['28th pm'] == 1]

tables = [first_fri_am, first_fri_pm, first_sat_am, first_sat_pm, sec_fri_am, sec_fri_pm, sec_sat_am, sec_sat_pm]
tables

#data_no_one


# In[25]:



for i in data_no_one.index:
    availability = data_no_one.loc[i][days].values
    smallest = list()
    distances = list()
    item_coordinates = data_no_one.loc[i]['coordinates']
    for j in range(0,8):
        if availability[j] == 1:
            tbl_coordinates = tables[j]['coordinates'].values
            for k in range(0, len(tbl_coordinates)):
                coords = tbl_coordinates[k]
                x = (item_coordinates[0] - coords[0])**2
                y = (item_coordinates[1] - coords[1])**2
                distances += [((x + y)**0.5)]
            smallest += [min(distances)]
        else:
            smallest += [1000]
    minimum_index = smallest.index(min(smallest))
    tables[minimum_index] = tables[minimum_index].append(data_no_one.loc[i])


# In[26]:


tables[1]


# In[27]:


#reset index for each table

for i in range(0, 8):
    tables[i] = tables[i].sort_index()
    display(tables[i])


# In[4]:


for i in range(0,8):
    print(len(tables[i]))


# In[29]:


# check length of each table and add indexes that could have some added and ones that could have some removed
remove = []
add = []

for i in range(0,8):
    length = len(tables[i])
    if length > 13:
        remove += [i]
    elif length < 13:
        add += [i]
        
remove


# In[30]:


#rearrange lists
for item in remove:
    more_than_one = tables[item][tables[item]['sum'] > 1]
    more_than_one_index = more_than_one.index
    for index in reversed(more_than_one_index):
        smallest = list()
        distances = list()
        if len(tables[item]) <= 13:
            break;
        time_slots = more_than_one.loc[index][days]
        item_coordinates = more_than_one.loc[index]['coordinates']
        for j in range(0, 8):
            if time_slots[j] == 1 and add.count(j) > 0 and item != j:
                tbl_coordinates = tables[item]['coordinates'].values
                for k in range(0, len(tbl_coordinates)):
                    coords = tbl_coordinates[k]
                    x = (item_coordinates[0] - coords[0])**2
                    y = (item_coordinates[1] - coords[1])**2
                    distances += [((x + y)**0.5)]
                smallest += [min(distances)]
            else:
                smallest += [1000]
        minimum_index = smallest.index(min(smallest))
        #check if this has to be iloc instead of loc -- changed to iloc
        tables[minimum_index] = tables[minimum_index].append(more_than_one.iloc[index])
        tables[item] = tables[item].drop(index, axis = 0)
            


# In[14]:


#reset index for each table

for i in range(0, 8):
    tables[i] = tables[i].sort_index()
    print(len(tables[i]))
    display(tables[i])


# In[15]:


#validate table lengths
for i in range(0, 4):
    print(len(tables[i]))


# In[12]:


#putting in order of distance
#address off of interstate 80 as the starting point since that's where we were told trucks would start
#change this if starting point changes 
geolocator = Nominatim(user_agent="example app")
starting = geolocator.geocode('650 University Avenue, Berkeley')
coords_starting = [[starting.point.latitude, starting.point.longitude]]

for i in range(0, 8):
    working_tbl = tables[i]
    new_tbl = pd.DataFrame()
    distances = []
    #get starting point
    for item in working_tbl.index:
        item_coordinates = working_tbl.loc[item]['coordinates'].values
        x = (item_coordinates[0] - coords_starting[0])**2
        y = (item_coordinates[1] - coords_starting[1])**2
        distances += [((x + y)**0.5)]
    minimum_index = smallest.index(min(distances))
    new_tbl= new_tbl.append(working_tbl.iloc[minimum_index])
    
    #set new starting point to measure distance
    starting = working_tbl.iloc[minimum_index]['coordinates'].values
    
    working_tbl = working_tbl.drop(minimum_index, axis = 0)
    

    #order all other points
    while len(working_tbl) > 0:
        distances = []
        for item in working_tbl.index:
            item_coordinates = working_tbl.loc[item]['coordinates'].values
            x = (item_coordinates[0] - starting[0])**2
            y = (item_coordinates[1] - starting[1])**2
            distances += [((x + y)**0.5)]
        minimum_index = smallest.index(min(distances))
        new_tbl= new_tbl.append(working_tbl.iloc[minimum_index])
        
        #set new starting point to measure distance
        starting = working_tbl.iloc[minimum_index]['coordinates'].values
        
        working_tbl = working_tbl.drop(minimum_index, axis = 0)
        
        


# In[ ]:


for i in range(0, 8):
    display(tables[i])

