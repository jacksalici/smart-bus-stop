# TO GET THE LIST OF THE BUS STATION PRESENT IN MODENA

import json, requests, csv, io

CSV_URL = "http://www.datiopen.it/SpodCkanApi/api/1/rest/dataset/mappa_fermate_autobus_in_italia.csv"

with requests.get(CSV_URL, stream=True) as r:
     buff = io.StringIO(r.text)
     obj = csv.DictReader(buff,delimiter=";")
     newobj = []
     for index, station in enumerate(obj):
          if station["Comune"].upper()=="MODENA" and station["Nome"]!="" :
               newobj[index] = {
                    'name': station["Nome"].title(),
                    'coord': [float(station["Latitudine"]), float(station["Longitudine"])],
               }
     
     with open("modenaBusStationDataset.json", "w") as fd:
         json.dump(newobj, fd, indent=4) 

     print(len(newobj))