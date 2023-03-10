# -*- coding: utf-8 -*-
"""lstm_stock.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ksQU2flKJzdh_kOFEvkIxYM0hOx8c6rF
"""

import numpy as np
import pandas as pd

import os
import matplotlib.pyplot as plt
import pandas_datareader as web
import datetime as dt

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
data_df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Datasets/stock.csv')
data_df

data_df['open'].plot()
plt.xlabel('Date')
plt.ylabel('Price')

from sklearn.preprocessing import MinMaxScaler
data_rehsape = data_df['open'].values.reshape(-1,1).astype('float32')

"""Scale the data"""

sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(data_rehsape)

look_back = 3
test_size = 250
train, test = training_set_scaled[:-test_size], training_set_scaled[-test_size-look_back:]

# how many days to be the base of predictions
prediction_days = 10

x_train=[]
y_train=[]

for i in range(prediction_days, len(train)):
    x_train.append(train[i-prediction_days:i,0])
    y_train.append(train[i,0])
    if i<=prediction_days:
        print(x_train)
        print(y_train)
        print()

#convert the x_train and y_train to numpy arrays
x_train, y_train = np.array(x_train), np.array(y_train)

#Reshape the data into 3 dimensional
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
print(x_train.shape)

len_train = np.linspace(0, train.shape[0],train.shape[0]+1)
plt.plot(len_train[1:],sc.inverse_transform(train.reshape(-1,1)))
#plt.plot(len_test[1:],sc.inverse_transform(y_hat))
plt.xlabel('Date') # set a xlabel
plt.ylabel('Price')

print('Train shape:', train.shape)

len_test = np.linspace(train.shape[0], test.shape[0]+train.shape[0],test.shape[0]+1)
plt.plot(len_test[1:],sc.inverse_transform(test.reshape(-1,1)))
#plt.plot(len_test[1:],sc.inverse_transform(y_hat))
plt.xlabel('Date') # set a xlabel
plt.ylabel('Price')

print('Test shape:', test.shape)

def LSTM_model():
    
    model = Sequential()
    
    model.add(LSTM(units = 50, return_sequences = True, input_shape = (x_train.shape[1],1)))
    model.add(Dropout(0.2))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(units=1))
    
    return model

model = LSTM_model()
model.summary()
model.compile(optimizer='adam', 
              loss='mean_squared_error')

history_ltsm = model.fit(x_train, y_train, epochs=30, batch_size=60, validation_split=0.2)

loss = history_ltsm.history['loss']
val_loss = history_ltsm.history['val_loss']
epochs = range(len(loss))
plt.plot(epochs, loss, color='orange', label='train loss')
plt.plot(epochs, val_loss, color='blue', label='val loss')
plt.title('Train and val loss')
plt.legend()
plt.savefig('loss.png')
plt.show()

"""Create test dataset"""

x_test = []
y_test = dataset[training_data_len:,:]
for i in range(60, len(test_data)):
    x_test.append(test_data[i-60:i,0])

# how many days to be the base of predictions
prediction_days = 10

x_test=[]
y_test=[]

for i in range(prediction_days, len(test)):
    x_test.append(test[i-prediction_days:i,0])
    y_test.append(test[i,0])
    if i<=prediction_days:
        print(x_test)
        print(y_test)
        print()

#convert into numpy arrays
x_test, y_test = np.array(x_test), np.array(y_test)

#Reshape the data into 3 dimensional
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
print(x_test.shape)

y_test = np.reshape(y_test, (y_test.shape[0], 1))
y_test = sc.inverse_transform(y_test)

y_pred = model.predict(x_test)
y_pred = sc.inverse_transform(y_pred)

print(y_test)

plt.plot(y_test, color='black', label="Actual")
plt.plot(y_pred, color= 'green', label="predicted")
plt.title("Test dataset")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.savefig('Test dataset')
plt.show()