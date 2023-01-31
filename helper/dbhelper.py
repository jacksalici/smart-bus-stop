import json
import sqlite3

connection = sqlite3.connect('../bus-server/database.db')
cursor = connection.cursor()

dataset = json.load(open('busStopDataset.json'))

for key, value in dataset.items():
    cursor.execute('insert into stops values(?,?,?)',(key,str(value["coord"]),value["name"]))
    

connection.commit()
connection.close()