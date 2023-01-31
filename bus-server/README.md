# Main server 🧠

```bash
# To run the server
pip install -r requirements.txt
cd bus-server
python app.py
```

The main server manages a Flask server that offers frontends to the stops. They are designed using simple Bootstrap classes.  

The main page presents all the stops, while at `http://127.0.0.1:5000/stops/<stopid>`.

The information regarding stops and lines is taken from the `opendata.comune.bologna.it` website, where developers can fetch the data of the TPER bus service using API. The script that we used to do that is [here](../helper/). We choose to simulate all the stops of Casalecchio town, near Bologna. This is because the town is still served by the same service as Bologna and shares the same optimal APIs, but it has far fewer stops.  

The server is subscribed to all MQTT topics and it couples the information of each bus and its next stop. MQTT is managed by `paho.mqtt.client` library. All the details, along with the seat bookings are stored in an SQLite database that represents a digital twin of public transport.  

People can use the front-end stop page to book a seat on the next bus. They have to log in using the Arduino NFC reader. The UID is sent to the front-end that is read using the [Serial Port API (mdn docs)](https://developer.mozilla.org/en-US/docs/Web/API/SerialPort/readable).

The server receives via MQTT the location of each bus and fetches using Open Route Service the ETA to its next station and sends all the data to it. It receives also the number of seats busy. ORS needs an API call to work properly.

The location of the bus along with the location of the stop itself is presented to the user using Leaflet JS Library for displaying maps.

From each station, moreover, the server receives the number of people awaiting there and if someone requests help using the specific button. The request is forwarded via MQTT to the upcoming bus. The next stop of each bus is currently obtained from the bus itself whose driver set it using the specific app. In a real solution, the database would integrate also the lines and all the paths of the buses.

The count of the people in the crowd is presented to the system administrators with a specific page (`/bus-admin`). Bus lines that can't manage all the people are highlighted.

For the developers, the server has an API endpoint (`/api`) that let to fetch real-time data from the stops such as the number of people there using `POST` method. Swagger is used for creating the documentation. 

## Useful Links:

- [https://developer.chrome.com/en/articles/serial/](https://developer.chrome.com/en/articles/serial/)
- [TPER OpenData Bologna](https://opendata.comune.bologna.it/explore/dataset/tper-vigente-mattina/guida/?disjunctive.route_id&disjunctive.stop_name&disjunctive.direction_id&disjunctive.giorno&disjunctive.orario&sort=-stop_id&location=14,44.48646,11.27438&basemap=jawg.streets)
