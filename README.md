# 🚏 IoT-powered smart bus stop

**To improve the mobility of citizens in a city, enabling fast, easy and safe travel, and at the same time, lower management costs for the administrators.**

## 📝 Abstract  

This project has been made as the final project for the Master's Degree in CS IoT course. It focuses on improving public transportation, particularly through city buses. The aim is to create a smart bus stop, which allows easier access to the service and enables (through a network of such stations) an enhancement of the service.

In the project vision, each smart bus stop is going to be equipped with a digital kiosk/totem device and a button board. A solar panel could also be provided to the station to make it self-sufficient during sunny hours.

The totem would allow people to see the real-time location of public transportation, with any transit times through the various stations. It also makes it possible to purchase tickets on the spot, making it easy for people without a mobile device to reserve a seat and plan a trip.  
An NFC/RFID reader makes the auth possible both with the smartphone and with other physical devices (provided, for example, to the elderly who don't own modern mobile).

For people with disabilities, a button is provided to alert the driver to give help or attention.

Once the network of smart stops is established, it will be possible to perform statistical analysis and forecasting on the use of a certain line, allowing better allocation of resources (add/delete a bus, "dynamic" lines, etc). An ideal solution uses an AI-powered camera to count people waiting at the stops and a server that checks if the maximum capacity of the upcoming bus would be exceeded, so calling an additional bus.

The project has been developed on Arduino and Esp32 dev-board. Every part works smoothly but some parts have been simplified since more realistic solutions would have been too time-expensive.

**Authors**: Giacomo Salici @jacksalici and Francesco Marucci @MRTCc, University of Modena and Reggio Emilia

## 🏗 Actors and Architecture  

The main actors of the project are the *bus stop*, the *bus stop help button*, *the bus itself* and the *main server*.

```mermaid

graph LR;
broker[Mqtt Broker]

server[Server]-.-|http|stop[Bus Stop]
server-.-|mqtt|button[Bus Stop Button]
server-.-|mqtt|bus[Bus Client]


stop-->c(Web Client)
stop-->n(NFC Authentication)
button-->h(Help Button)
bus-->t(GPS Tracker)
bus-->p(Passenger counter)

server-->d(Digital Twin)
server-->m(Resources Manager)
server -->a(AI Forecasting)


```

### Main server 🧠

The main server manages a Flask server that offers frontends to the stops. It is subscribed to all    MQTT topics and it couples the information of each bus and its next stop. All the details, along with the seat bookings are stored in an SQLite database that represents a digital twin of public transport.

The server receives via MQTT the location of each bus and fetches using Open Route Service the ETA to its next station and sends all the data to it. It receives also the number of seats busy.

From each station, moreover, the server receives the number of people awaiting there and if someone requests help using the specific button. The request is forwarded via MQTT to the upcoming bus.

The count of the people in the crowd is presented to the system administrators with a specific page. Bus lines that can't manage all the people are highlighted.

For the developers, the server has an API endpoint that let to fetch real-time data from the stops such as the number of people there.

Lastly, we develop with Prophet a forecasting model to predict the number of busy seats in a future moment based on the past recorded data. Since it is just a demo project the recorded data was generated using a script, so the model is not accurate.

### Bus Stop 🚏

Each bus stop has a kiosk loaded on the server offered front-end. Users can use a real-time-updated map to see the location of the bus, along with the actual number of busy seats on that bus.

Users can book a seat by logging in using an NFC reader. An Arduino board sends to the serial port the UID of the NFC tag (or smartphone). It is read via front-end using the experimental web serial port API. Since the project is just a demo we used the UID as the authentication key ignoring that it would be a severe vulnerability in an actual realization.

### Bus Stop Help Button 🕹

Each stop is provided with an ESP32 board that let people toggle a button to call for help. The board is separated from the Arduino NFC reader for the sake of modularity and the decoupling principle.

The same ESP32 board read the value of a potentiometer that simulates the presence of an AI-powered camera that counts people.

### Bus Client 🚍  

Each bus is tracked with a GPS sensor. For the demo we created a smartphone app that sends the location and that allows the user to set the number of busy seats and the next stop.
