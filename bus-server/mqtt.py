

import paho.mqtt.client as paho
from paho import mqtt
import json, sqlite3




def toggleHButton (stopID, counter, mqttclient):
    print("Toggled h button for the stop " + stopID + ": "+ str(counter))
    connection = sqlite3.connect('database.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute('update stops set hButton = ? where id = ?', (counter, stopID))
    connection.commit()
    bus = cursor.execute('select id from buses where stop_id = ?', (stopID,)).fetchone()
    connection.commit()
    connection.close()
    if bus is not None:
        print(bus[0])
        #mqtt publish to the bus topic
        id_fermata = stopID
        id_corsa = "id_corsa"
        mqttclient.publish(f'devices/fermate/{id_fermata}/corse/{id_corsa}', json.dumps({"fragile": counter}))
    
    
    

def peopleCounter(stopID, counter):
    print("People Counter " + stopID + ": "+ str(counter))
    connection = sqlite3.connect('database.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute('update stops set people = ? where id = ?', (counter, stopID))
    
    connection.commit()
    connection.close()
    
    

def updateBus(busDict):
    print(busDict)
    connection = sqlite3.connect('database.db', check_same_thread=False)
    cursor = connection.cursor()
    """cursor.execute('insert or replace into buses values(?,?,?,?)',
                   (busDict["id_bus"],
                    str([
                        busDict["latitude"],
                        busDict["longitude"]]),
                    busDict["fermata"],
                    busDict["seats_count"],
                    ))
    """
    cursor.execute('insert or replace into buses values(?,?,?,?)',
                   (busDict["id_bus"],
                    str([
                        busDict["latitude"],
                        busDict["longitude"]]),
                    busDict["fermata"],
                    busDict["seats_count"],
                    ))
    
    connection.commit()
    connection.close()

    

    


class MqttClient:
    
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    # setting callbacks for different events to see if it works, print the message etc.
    def on_connect(self,client, userdata, flags, rc, properties=None):
        print("Connected with code: %s." % rc)

    # with this callback you can see if your publish was successful
    def on_publish(self, client, userdata, mid, properties=None):
        print("Published " + str(mid))

    # print which topic was subscribed to
    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        pass

    # print message, useful for checking if it was successful
    def on_message(self,client, userdata, msg):
        print("Message arrived from " + msg.topic + " - " + str(msg.payload.decode("utf-8")))
        
        topicArray = str(msg.topic).split("/")
        #devices/hButtons/from/01 - 0
        if len(topicArray)>3:
            if topicArray[1] == "hButtons":
                toggleHButton(topicArray[3], int(msg.payload.decode("utf-8")), self.client)

        #devices/fermate/01/contapersone/ - 14
        if len(topicArray)>3:
            if topicArray[3] == "contapersone":
                peopleCounter(topicArray[2], msg.payload.decode("utf-8"))
        
        #devices/buses/id_bus - {"id_bus":"id_bus","latitude":44.8909336,"longitude":11.0672094,"seats_count":2,"fermata":""}
        if len(topicArray)>2:
            if topicArray[1] == "buses":
                updateBus(json.loads(str(msg.payload.decode("utf-8"))))
        

    def __init__(self) -> None:
        
        self.client.on_connect = self.on_connect
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.username_pw_set("fran_student", "Franhive1")
        self.client.connect("d1690858e84545978808a4cc1505ee04.s2.eu.hivemq.cloud", 8883)
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.subscribe("#")
        

