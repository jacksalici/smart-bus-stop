

import paho.mqtt.client as paho
from paho import mqtt


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
        print(msg.topic + " - " + str(msg.payload.decode("utf-8")))

    def __init__(self) -> None:
        
        self.client.on_connect = self.on_connect
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.username_pw_set("fran_student", "Franhive1")
        self.client.connect("d1690858e84545978808a4cc1505ee04.s2.eu.hivemq.cloud", 8883)
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.subscribe("#")
