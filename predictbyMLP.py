#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 20:55:02 2022

@author: wll
"""


import pandas as pd
import pickle

df = pd.read_csv("spec_features.csv")
X = df.iloc[:,1:181]
with open('MLPonMainsample.pickle', 'rb') as f:
    classifier = pickle.load(f)
y_pred = classifier.predict(X)
y_pred = y_pred.tolist()
df['MLPclass']=y_pred
print(df)
df.to_csv('result_MLP.csv',index=None)