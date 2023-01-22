import numpy as np
import pandas as pd

import sys
import getopt


def data_generation(start_date, end_date, is_train=True):
    dates = pd.date_range(start=pd.Timestamp(start_date), end=pd.Timestamp(end_date), freq='30min')
    shape = len(dates)

    mu, sigma = 4, 1
    values = np.random.default_rng().normal(mu, sigma, shape)
    rints = np.round(values)
    rints[rints < 0] = 0

    df = pd.DataFrame({
        "datetime": dates,
        "count": rints,
    })

    df['hour'] = df['datetime'].dt.hour
    df = df[(6 <= df['hour']) & (df['hour'] <= 21)]

    df['count'] = np.where(df['hour'] == 12, df['count'] + 3, df['count'] - 1)
    df['count'] = np.where(df['hour'] == 13, df['count'] + 3, df['count'] - 1)
    df['count'] = np.where(df['hour'] == 18, df['count'] + 3, df['count'] - 1)
    df['count'] = np.where(df['hour'] == 19, df['count'] + 3, df['count'] - 1)
    df['count'] = np.where(df['count'] < 0, 0, df['count'])

    df.drop('hour', axis=1, inplace=True)

    # print(df.info())

    if is_train:
        df.to_csv('train_data.csv', index=False)
    else:
        df.to_csv('test_data.csv', index=False)


if __name__ == "__main__":
    print("Acquisizione intervalli temporali di training e testing...")
    print("Inserire i datetime richiesti nel formato: 'YYYY-MM-DD hh:mm:ss'")

    try:
        train_start = input("Data di inizio training:")
        train_end = input("Data di fine training:")
        test_start = input("Data di inizio testing:")
        test_end = input("Data di fine testing:")
    except:
        print("ERRORE: qualcosa non ha funzionato nell'acquisizione degli interavalli temporali!!!")
        sys.exit(-1)

    print("Generazione dati di training...")
    data_generation(train_start, train_end)

    print("Generazione dati di testing...")
    data_generation(test_start, test_end, is_train=False)

    print("Fatto!")
