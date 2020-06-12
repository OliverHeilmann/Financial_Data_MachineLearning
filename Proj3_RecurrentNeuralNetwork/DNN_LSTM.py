#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 19:46:35 2020

@author: OliverHeilmann
"""

import pandas as pd
from collections import deque
import time, random, os, pdb
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, CuDNNLSTM, BatchNormalization
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.callbacks import ModelCheckpoint, ModelCheckpoint
from sklearn import preprocessing

'''
Use:
    tensorboard --logdir=logs   # in terminal
    http://127.0.0.1:6006/      # in browser
    
Plotting:
    %matplotlib qt        --> as po-pup
    %matplotlib inline    --> in shell
'''

SEQ_LEN = 60  # how long of a preceeding sequence to collect for RNN
FUTURE_PERIOD_PREDICT = 3  # how far into the future are we trying to predict?
RATIO_TO_PREDICT = "GFS.L"
EPOCHS = 3  # how many passes through our data
BATCH_SIZE = 64  # how many batches? Try smaller batch if you're getting OOM (out of memory) errors.
NAME = f"{RATIO_TO_PREDICT}-{SEQ_LEN}-SEQ-{FUTURE_PERIOD_PREDICT}-PRED-{int(time.time())}"
RATIOS = ["GFS.L", "BAB.L", "JDW.L", "IAG.L"]  # the 4 ratios we want to consider


def classify(current, future):
    if float(future) > float(current):
        return 1
    else:
        return 0

main_df = pd.DataFrame() # begin empty
ratios = ["GFS.L", "BAB.L", "JDW.L", "IAG.L"]  # the 4 ratios we want to consider
for ratio in RATIOS:  # begin iteration
    print(ratio)
    dataset = f'stock_dfs/{ratio}.csv'  # get the full path to the file.
    df = pd.read_csv(dataset)  # read in specific file

    pdb.set_trace()

    # rename volume and close to include the ticker so we can still which close/volume is which:
    df.rename(columns={"Adj Close": f"{ratio}_close", "Volume": f"{ratio}_volume"}, inplace=True)

    df.set_index("Date", inplace=True)  # set time as index so we can join them on this shared time
    df = df[[f"{ratio}_close", f"{ratio}_volume"]]  # ignore the other columns besides price and volume

    if len(main_df)==0:  # if the dataframe is empty
        main_df = df  # then it's just the current df
    else:  # otherwise, join this data to the main one
        main_df = main_df.join(df)

main_df.fillna(method="ffill", inplace=True)  # if there are gaps in data, use previously known values
main_df.dropna(inplace=True)
print(main_df.head())  # how did we do??

main_df['future'] = main_df[f'{RATIO_TO_PREDICT}_close'].shift(-FUTURE_PERIOD_PREDICT)
main_df['target'] = list(map(classify, main_df[f'{RATIO_TO_PREDICT}_close'], main_df['future']))
print(main_df.head())

times = sorted(main_df.index.values)  # get the times
last_5pct = sorted(main_df.index.values)[-int(0.05*len(times))]  # get the last 5% of the times



