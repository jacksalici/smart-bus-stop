# People count Forecasting ✨

We developed with Prophet a **forecasting model** to predict the number of people waiting at the stops in a future moment based on the past recorded data. In the system, there will be a Prophet-object for each stop. Since it is just a demo project the recorded data was generated using a script, so the model is not accurate.

Our workflow was:
1. fake data generation -> `data_generation.py`
2. model training -> `model_train_test.py`
3. model prediction -> `model_predict.py`

`model_plot.py` is the same of `model_train_test.py`, but it shows some plots about Prophet's predictions.



### 1. Fake data generation
`data_generation.py` generates time series (day / number of peoples that have booked the stop) needed to train and test the Prophet model.
Data are generated using a composition of a gaussian distribution and an ad-hoc distribution in order to resemble the real-world peak hours of traffic (we assume at 12:00 and 19:00).
Data are saved in a `.csv` file using the format `timestamp, number of people`:
- training data are saved in the file `train_data.csv`
- test data are saved in the file `test_data.csv`

The script expects the initial and final dates of data in the format `YYYY-MM-DD hh:mm:ss`.
A running example:
```bash
python data_generation.py

Acquisizione intervalli temporali di training e testing...
Inserire i datetime richiesti nel formato: 'YYYY-MM-DD hh:mm:ss'
Data di inizio training:2022-01-01 06:00:00
Data di fine training:2022-12-31 21:30:00
Data di inizio testing:2023-01-01 06:00:00
Data di fine testing:2023-01-31 21:30:00
Generazione dati di training...
Generazione dati di testing...
Fatto!
```



### 2. Model training
`model_train_test.py` trains the model and tests it.
This script expects training and testing data in `.csv` format.:
```bash
python model_train_test.py train_data.csv test_data.csv
```

The trained model is saved in the file `serialized_model.json`.

Some example charts (if you run `model_plot.py`):
![count](https://user-images.githubusercontent.com/51177049/220537601-fc88cb68-8ec5-478d-a6ee-ecc257b6b63f.png)

![test](https://user-images.githubusercontent.com/51177049/220537661-64943d43-e540-4957-894f-a7a890c53536.png)

![graphs](https://user-images.githubusercontent.com/51177049/220537682-29ba20d3-bcf4-4364-b6d2-7964ca7640b1.png)



### 3. Model prediction
`model_predict.py` makes predictions.
The script expects a train model file (json-serialized) and an output file in csv format (`timestamp, number of people`):
```bash
python model_predict.py model_file.json data_file.csv
```



# Acknowledgements
- Official Prophet page -> https://facebook.github.io/prophet/
- Official Github Prophet page -> https://github.com/facebook/prophet
- Useful quickstart guide to Prophet -> https://www.youtube.com/watch?v=j0eioK5edqg
