import numpy as np
import pandas as pd
from fbprophet import Prophet
from prophet.serialize import model_to_json, model_from_json

import time
import sys


def help_command_syntax():
    print("HELP:\n\t model_train_test.py model_file.json data_file.csv")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("ERRORE, numero incorretto di parametri di invocazione!!!")
        help_command_syntax()
        sys.exit(-1)

    model_file, data_file = sys.argv[1:]

    print("Loading model...")
    with open(model_file, 'r') as fin:
        model = model_from_json(fin.read())

    print("Loading data...")
    df = pd.read_csv(data_file, index_col=[0], parse_dates=[0])
    df = df.reset_index().rename(columns={'datetime': 'ds', 'count': 'y'})

    print("Performing forecasting...")
    start_time = time.time()

    df_fcst = model.predict(df)
    df_fcst = df_fcst[(6 <= df_fcst['ds'].dt.hour) & (df_fcst['ds'].dt.hour <= 21)]

    df_fcst = df_fcst[df_fcst['yhat'] > 0]
    df_fcst['yhat'] = np.round(df_fcst['yhat'])

    end_time = time.time()
    delta_sec = end_time - start_time
    print('\ttime needed (sec) to forecast: ', delta_sec / 60)

    print("Performance evaluation...")
    pass

    print("Saving forecasted data...")
    df_fcst.to_csv('fcst_data', index=False)

    print("Done!")

