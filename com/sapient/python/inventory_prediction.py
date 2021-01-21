import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.api import ExponentialSmoothing
import math

df = pd.read_csv('calculated_measures.csv', nrows=10001).sort_values(['report_date'])
df = df[df['facility_name'].str.contains("Camrose")]
print(len(df))
# Creating train and test set
# Index 10392 marks the end of October 2013
train = df[0:160]
test = df[160:]

# Aggregating the dataset at daily level
df['report_date'] = pd.to_datetime(df.report_date, format='%Y-%m-%d %H:%M:%S')
df.index = df.report_date
df = df.resample('M').mean()

test['report_date'] = pd.to_datetime(test.report_date, format='%Y-%m-%d %H:%M:%S')
test.index = test.report_date
test = test.resample('M').mean()

train['report_date'] = pd.to_datetime(train.report_date, format='%Y-%m-%d %H:%M:%S')
train.index = train.report_date
train = train.resample('M').mean()
y_hat_avg = test.copy()

fit1 = ExponentialSmoothing(np.asarray(train['physical_inventory_quantity_mt']), seasonal_periods=2, trend='add',
                            seasonal='add', ).fit()
y_hat_avg['Prediction_Count'] = fit1.forecast(len(test))

plt.figure(figsize=(12, 5))
plt.plot(train['physical_inventory_quantity_mt'], label='Train')
plt.plot(test['physical_inventory_quantity_mt'], label='Test')
plt.plot(y_hat_avg['Prediction_Count'], label='Prediction_Count')

plt.legend(loc='best')
plt.show()
# print(test.Count)
rms = math.sqrt(mean_squared_error(test.physical_inventory_quantity_mt, y_hat_avg.Prediction_Count))
print(rms)

newdf = pd.concat([y_hat_avg])
newdf.to_csv("prediction_report.csv")
