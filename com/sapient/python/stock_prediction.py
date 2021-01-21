import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import math
df = pd.read_csv('train.csv', nrows = 11856)
from statsmodels.tsa.api import ExponentialSmoothing
#Creating train and test set
#Index 10392 marks the end of October 2013
train=df[0:10392]
test=df[10392:]

#Aggregating the dataset at daily level
df['Timestamp'] = pd.to_datetime(df.Datetime,format='%d-%m-%Y %H:%M')
df.index = df.Timestamp
df = df.resample('D').mean()


train['Timestamp'] = pd.to_datetime(train.Datetime,format='%d-%m-%Y %H:%M')
train.index = train.Timestamp
train = train.resample('D').mean()
test['Timestamp'] = pd.to_datetime(test.Datetime,format='%d-%m-%Y %H:%M')
test.index = test.Timestamp
test = test.resample('D').mean()
train.Count.plot(figsize=(15,8), title= 'Report date', fontsize=14)
test.Count.plot(figsize=(15,8), title= 'Report date', fontsize=14)

y_hat_avg = test.copy()

fit1 = ExponentialSmoothing(np.asarray(train['Count']) ,seasonal_periods=7 ,trend='add', seasonal='add',).fit()

y_hat_avg['Prediction_Count'] = fit1.forecast(len(test))


plt.figure(figsize=(12,5))
plt.plot(train['Count'], label='Train')
plt.plot(test['Count'], label='Test')
plt.plot(y_hat_avg['Prediction_Count'], label='Prediction_Count')

plt.legend(loc='best')
plt.show()

#print(test.Count)
rms = math.sqrt(mean_squared_error(test.Count, y_hat_avg.Prediction_Count))
print(rms)

newdf = pd.concat([y_hat_avg])
newdf.to_csv("prediction_report.csv")

