import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.api import ExponentialSmoothing
import math


# .sort_values(['report_date'])
# df = df[df['facility_name'].str.contains("Camrose")]

class inventory_prediction:
    # def __init__(self, name):
    #     self.name = name

    def predict(self):
        print("Prediction started")
        df = pd.read_csv('C:/Users/gopasali/PycharmProjects/PyExcersice/prediction/inventory/daily_inventory.csv')
        x = int((len(df) / 100) * 90)  # 4717
        train = df[0:x]
        test = df[x:]

        # Aggregating the dataset at daily level
        test['report_date'] = pd.to_datetime(test.report_date, format='%Y-%m-%d %H:%M:%S')
        test.index = test.report_date
        test = test.resample('D').mean()

        train['report_date'] = pd.to_datetime(train.report_date, format='%Y-%m-%d %H:%M:%S')
        train.index = train.report_date
        train = train.resample('D').mean()
        y_hat_avg = test.copy()
        # 2,6
        # with pd.option_context('display.max_rows', None, 'display.max_columns',
        #                        None):  # more options can be specified also
        #     print(train)

        fit1 = ExponentialSmoothing(np.asarray(train['physical_inventory_quantity_mt']), seasonal_periods=7,
                                    trend='add',
                                    seasonal='add').fit()

        y_hat_avg['Prediction_Count'] = fit1.forecast(len(test))

        plt.figure(figsize=(12, 5))
        plt.plot(train['physical_inventory_quantity_mt'], label='History')
        plt.plot(test['physical_inventory_quantity_mt'], label='Actual')
        plt.plot(y_hat_avg['Prediction_Count'], label='Prediction_Count')

        plt.legend(loc='best')
        plt.savefig("C:/Users/gopasali/PycharmProjects/PyExcersice/prediction/web/static/prediction_plot.jpeg")
        rms = math.sqrt(mean_squared_error(test.physical_inventory_quantity_mt, y_hat_avg.Prediction_Count))
        print(rms)

        prediction_results = pd.concat([y_hat_avg])
        prediction_results.to_csv(
            "C:/Users/gopasali/PycharmProjects/PyExcersice/prediction/prediction_output/prediction_report.csv")
        print("Prediction ended")

