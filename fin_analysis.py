# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 19:26:45 2017

@author: admin
"""

import pandas as pd
from difflib import SequenceMatcher
import numpy as np

#Function that computes the similarity ratio between two strings using Gestalt Pattern Matching algorithm
def similar(a,b):
    return SequenceMatcher(None,a,b).ratio()

#Read in the dataframe.
df = pd.read_csv('C:/Users/admin/findata.csv')  
#Query the datframe to find the index of the inputted company.
a = df.set_index('Name').index.get_loc(raw_input('Enter the Company name: ') )

#Manipulate the data according to the required format.
training = df.iloc[:,2:11].fillna(value='0')
year = training[['Founding year']].astype(int).values
country = training['Company country']
training = training.drop(['Total funding','Number of employees','Founding year','Company country'],axis=1)

#Initialize column names list and similarity index np array
column_identifier = training.columns.tolist()
similarity_index =  np.zeros(shape = (df.shape[0] ,len(column_identifier)))

#Compute the base similarity index using only Tags, Company Description, Product Description and partners features
for i in range(len(column_identifier)):
    for j in range(df.shape[0]):
        if training.loc[j,column_identifier[i]] == '0':
            similarity_index[j,i] = 0
        else :
            similarity_index[j,i] = similar(training.loc[a,column_identifier[i]],training.loc[j,column_identifier[i]])
[similarity_index[:,i]/max(similarity_index[:,i]) for i in range(len(column_identifier))]  
similarity_index = np.array([sum(similarity_index[i,:]) for i in range(df.shape[0])])

#Compute the similarity when investor feature is checked
investor_index = []
for j in range(df.shape[0]):
    if training.loc[j,'Investors'] == '0':
        investor_index.append(0)
    else:
        investor_index.append(similar(training.loc[a,'Investors'],training.loc[j,'Investors']))
investor_index[j] = investor_index[j]/max(investor_index)
investor_index = np.array([similarity_index[i]+investor_index[i] for i in range(df.shape[0])])
buff2 = investor_index.argsort()[-4:][::-1]
buff2 = np.delete(buff2,0)
print 'Filtering by investor:\n%s\n'%(df.loc[buff2,'Name'])

#Compute the similarity when lifestage feature is checked
lifestage_index = []
for j in range(df.shape[0]):
    if abs(year[a]-year[j]) < 3:
        lifestage_index.append(1)
    else:
        lifestage_index.append(0)  
lifestage_index = np.array([similarity_index[i]+lifestage_index[i] for i in range(df.shape[0])]) 
buff3 = lifestage_index.argsort()[-4:][::-1]
buff3 = np.delete(buff3,0)
print 'Filtering by life stage:\n%s\n'%(df.loc[buff3,'Name'])

#Compute the similarity when country feature is checked
country_index = []
for i in range(df.shape[0]):
    if similar(country.loc[a],country.loc[i]) <= 0.5:
        country_index.append(0)
    else:
        country_index.append(1)
country_index = np.array([similarity_index[i]+country_index[i] for i in range(df.shape[0])])
buff4 = country_index.argsort()[-4:][::-1]
buff4 = np.delete(buff4,0)
print 'Filtering by country:\n%s'%(df.loc[buff4,'Name'])


