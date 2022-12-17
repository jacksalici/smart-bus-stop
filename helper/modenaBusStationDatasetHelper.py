# TO GET THE LIST OF THE BUS STATION PRESENT IN MODENA

import json, requests, csv, io

CSV_URL = "http://www.datiopen.it/SpodCkanApi/api/1/rest/dataset/mappa_fermate_autobus_in_italia.csv"

with requests.get(CSV_URL, stream=True) as r:
     buff = io.StringIO(r.text)
     obj = csv.DictReader(buff,delimiter=";")
     newobj = []
     for station in obj:
          if station["Comune"].upper()=="MODENA":
               newobj.append({
                    "name": station["Nome"].title(),
                    "lon": station["Longitudine"],
                    "lat": station["Latitudine"]
               })
     
     with open("modenaBusStationDataset.json", "w") as fd:
         json.dump(newobj, fd, indent=4) 

     print(len(newobj))