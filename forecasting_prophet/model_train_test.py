import numpy as np
import pandas as pd
from fbprophet import Prophet
from prophet.serialize import model_to_json, model_from_json

import time
import sys
import error_functions


def help_command_syntax():
    print("HELP:\n\t model_train_test.py train_data_file.csv test_data_file.csv")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("ERRORE, numero incorretto di parametri di invocazione!!!")
        help_command_syntax()
        sys.exit(-1)
    
    train_data_file, test_data_file = sys.argv[1:]

    print("Loading training data...")
    df = pd.read_csv(train_data_file, index_col=[0], parse_dates=[0])

    print("Training...")
    df_train = df.reset_index().rename(columns={'datetime': 'ds', 'count': 'y'})
    model = Prophet()

    start_time = time.time()

    model.fit(df_train)

    end_time = time.time()
    delta_sec = end_time - start_time
    print('\ttime needed (sec) to train: ', delta_sec / 60)

    print("Loading test data...")
    df_test = pd.read_csv(test_data_file, index_col=[0], parse_dates=[0])
    df_test_prophet = df_test.reset_index().rename(columns={'datetime': 'ds', 'count': 'y'})

    print("Performing forecasting on test data...")
    test_fcst = model.predict(df_test_prophet)
    test_fcst = test_fcst[(6 <= test_fcst['ds'].dt.hour) & (test_fcst['ds'].dt.hour <= 21)]

    print("Performance evaluation...")
    pass

    print("Saving model in 'serialized_model.json'...")
    with open('serialized_model.json', 'w') as fout:
        fout.write(model_to_json(model))

    print("Done!")
