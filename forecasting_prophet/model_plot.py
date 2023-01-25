import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from fbprophet import Prophet
from prophet.serialize import model_to_json, model_from_json

import time

import warnings
warnings.filterwarnings("ignore")

plt.style.use('ggplot')
plt.style.use('fivethirtyeight')

print("Loading training data...")
df = pd.read_csv('data.csv', index_col=[0], parse_dates=[0])
# print(df.info())

print("Plotting training data...")
# plotting per debug
color_pal = sns.color_palette()
df.plot(style='.', figsize=(10, 5), ms=1, color=color_pal[0], title='FERMATE')
plt.show()

print("Training...")
df_train = df.reset_index().rename(columns={'datetime': 'ds', 'count': 'y'})
# print(df_train.info())
model = Prophet()

start_time = time.time()

model.fit(df_train)

end_time = time.time()
delta_sec = end_time - start_time
print('\ttime needed (sec) to train: ', delta_sec/60)

print("Loading test data...")
df_test = pd.read_csv('test_data.csv', index_col=[0], parse_dates=[0])
df_test_prophet = df_test.reset_index().rename(columns={'datetime': 'ds', 'count': 'y'})

print("Performing forecasting...")
test_fcst = model.predict(df_test_prophet)
test_fcst = test_fcst[(6 <= test_fcst['ds'].dt.hour) & (test_fcst['ds'].dt.hour <= 21)]
test_fcst.head()

test_fcst.info()
test_fcst = test_fcst[test_fcst['yhat']>0]
test_fcst['yhat'] = np.round(test_fcst['yhat'])

fig, ax = plt.subplots(figsize=(10, 5))
fig = model.plot(test_fcst, ax=ax)
ax.set_title('Prophet Forecast')
plt.show()

fig = model.plot_components(test_fcst)
plt.show()

print("Saving model in 'serialized_model.json'...")
with open('serialized_model.json', 'w') as fout:
    fout.write(model_to_json(model))  # Save model
print("Done!")


