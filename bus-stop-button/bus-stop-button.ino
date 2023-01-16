
#include <WiFiManager.h>

#include "credential.h"
#include <WiFi.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>

WiFiClientSecure espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;

int currentstateFSM_Led = 0;

#define MSG_BUFFER_SIZE (50)
char msg[MSG_BUFFER_SIZE];

#define BUTTON_PIN 16 // ESP32 pin GIOP16, which connected to button
#define LED_PIN 18    // ESP32 pin GIOP18, which connected to led


const char *topic_out = "button/01";
const char *topic_in = "info";

static const char *root_ca PROGMEM = R"EOF(
-----BEGIN CERTIFICATE-----
MIIFazCCA1OgAwIBAgIRAIIQz7DSQONZRGPgu2OCiwAwDQYJKoZIhvcNAQELBQAw
TzELMAkGA1UEBhMCVVMxKTAnBgNVBAoTIEludGVybmV0IFNlY3VyaXR5IFJlc2Vh
cmNoIEdyb3VwMRUwEwYDVQQDEwxJU1JHIFJvb3QgWDEwHhcNMTUwNjA0MTEwNDM4
WhcNMzUwNjA0MTEwNDM4WjBPMQswCQYDVQQGEwJVUzEpMCcGA1UEChMgSW50ZXJu
ZXQgU2VjdXJpdHkgUmVzZWFyY2ggR3JvdXAxFTATBgNVBAMTDElTUkcgUm9vdCBY
MTCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBAK3oJHP0FDfzm54rVygc
h77ct984kIxuPOZXoHj3dcKi/vVqbvYATyjb3miGbESTtrFj/RQSa78f0uoxmyF+
0TM8ukj13Xnfs7j/EvEhmkvBioZxaUpmZmyPfjxwv60pIgbz5MDmgK7iS4+3mX6U
A5/TR5d8mUgjU+g4rk8Kb4Mu0UlXjIB0ttov0DiNewNwIRt18jA8+o+u3dpjq+sW
T8KOEUt+zwvo/7V3LvSye0rgTBIlDHCNAymg4VMk7BPZ7hm/ELNKjD+Jo2FR3qyH
B5T0Y3HsLuJvW5iB4YlcNHlsdu87kGJ55tukmi8mxdAQ4Q7e2RCOFvu396j3x+UC
B5iPNgiV5+I3lg02dZ77DnKxHZu8A/lJBdiB3QW0KtZB6awBdpUKD9jf1b0SHzUv
KBds0pjBqAlkd25HN7rOrFleaJ1/ctaJxQZBKT5ZPt0m9STJEadao0xAH0ahmbWn
OlFuhjuefXKnEgV4We0+UXgVCwOPjdAvBbI+e0ocS3MFEvzG6uBQE3xDk3SzynTn
jh8BCNAw1FtxNrQHusEwMFxIt4I7mKZ9YIqioymCzLq9gwQbooMDQaHWBfEbwrbw
qHyGO0aoSCqI3Haadr8faqU9GY/rOPNk3sgrDQoo//fb4hVC1CLQJ13hef4Y53CI
rU7m2Ys6xt0nUW7/vGT1M0NPAgMBAAGjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNV
HRMBAf8EBTADAQH/MB0GA1UdDgQWBBR5tFnme7bl5AFzgAiIyBpY9umbbjANBgkq
hkiG9w0BAQsFAAOCAgEAVR9YqbyyqFDQDLHYGmkgJykIrGF1XIpu+ILlaS/V9lZL
ubhzEFnTIZd+50xx+7LSYK05qAvqFyFWhfFQDlnrzuBZ6brJFe+GnY+EgPbk6ZGQ
3BebYhtF8GaV0nxvwuo77x/Py9auJ/GpsMiu/X1+mvoiBOv/2X/qkSsisRcOj/KK
NFtY2PwByVS5uCbMiogziUwthDyC3+6WVwW6LLv3xLfHTjuCvjHIInNzktHCgKQ5
ORAzI4JMPJ+GslWYHb4phowim57iaztXOoJwTdwJx4nLCgdNbOhdjsnvzqvHu7Ur
TkXWStAmzOVyyghqpZXjFaH3pO3JLF+l+/+sKAIuvtd7u+Nxe5AW0wdeRlN8NwdC
jNPElpzVmbUq4JUagEiuTDkHzsxHpFKVK7q4+63SM1N95R1NbdWhscdCb+ZAJzVc
oyi3B43njTOQ5yOf+1CceWxG1bQVs5ZufpsMljq4Ui0/1lvh+wjChP4kqKOJ2qxq
4RgqsahDYVvTH9w7jXbyLeiNdd8XM2w9U/t7y0Ff/9yi0GE44Za4rF2LN9d11TPA
mRGunUHBcnWEvgJBQl9nJEiU0Zsnvgc/ubhPgXRR4Xq37Z0j4r7g1SgEEzwxA57d
emyPxgcYxn/eR44/KJ4EBs+lVDR3veyJm+kXQ99b21/+jh5Xos1AnX5iItreGCc=
-----END CERTIFICATE-----
)EOF";

void setup()
{

    Serial.begin(115200);
    Serial.print("Connecting to ");
    Serial.println(ssid);

    // WiFiManagerParameter stopbusidparameter("StopID", "Topic", topic_out, 20);
    WiFiManager wifiManager;

    /// wifiManager.addParameter(&stopbusidparameter);

    wifiManager.autoConnect("esp32");

    // topic_String = String(topic_out_new);

    randomSeed(micros());
    Serial.print("WiFi connected at IP address: ");
    Serial.println(WiFi.localIP());

    espClient.setCACert(root_ca);
    client.setServer(mqtt_server, mqtt_port);
    client.setCallback(callback);

    pinMode(BUTTON_PIN, INPUT_PULLUP); // set ESP32 pin to input pull-up mode
    pinMode(LED_PIN, OUTPUT);          // set ESP32 pin to output mode

}

void loop()
{

    if (!client.connected())
        reconnect();
    client.loop();
    
    // 1.0 input read
    int buttonState;
    buttonState = digitalRead(BUTTON_PIN);

    // input to enum

    // 2.0 future state
    int futurestateFSM_Led;

    // default future state = current state
    futurestateFSM_Led = currentstateFSM_Led;
    if (currentstateFSM_Led == 0 && buttonState == HIGH)
        futurestateFSM_Led = 1;
    if (currentstateFSM_Led == 1 && buttonState == LOW)
        futurestateFSM_Led = 2;
    if (currentstateFSM_Led == 2 && buttonState == HIGH)
        futurestateFSM_Led = 3;
    if (currentstateFSM_Led == 3 && buttonState == LOW)
        futurestateFSM_Led = 0;

    // 3.0  on entry and on exit actions
    if (futurestateFSM_Led != currentstateFSM_Led)
    {
        if (futurestateFSM_Led == 1)
            {digitalWrite(LED_PIN, LOW);
            publishMessage(String(LOW), true);}
        if (futurestateFSM_Led == 3)
            {digitalWrite(LED_PIN, HIGH);
            publishMessage(String(HIGH), true);}
    }

    // 4.0 transition
    currentstateFSM_Led = futurestateFSM_Led;
}

void reconnect()
{
    // Loop until we’re reconnected
    while (!client.connected())
    {
        Serial.print("Attempting MQTT connection. ");
        String clientId = "ESP8266Client-"; // Create a random client ID
        clientId += String(random(0xffff), HEX);
        // Attempt to connect
        if (client.connect(clientId.c_str(), mqtt_username, mqtt_password))
        {
            Serial.println("Connected");
            client.subscribe(topic_in); // subscribe the topics here
                                        // client.subscribe(command2_topic);   // subscribe the topics here
        }
        else
        {
            Serial.print("Failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds"); // Wait 5 seconds before retrying
            delay(5000);
        }
    }
}

void callback(char *topic, byte *payload, unsigned int length)
{
    String incommingMessage = "";
    for (int i = 0; i < length; i++)
        incommingMessage += (char)payload[i];
    Serial.println("Message arrived from " + String(topic) + ": " + incommingMessage);
}

void publishMessage(String payload, boolean retained)
{
    if (client.publish(topic_out, payload.c_str(), true))
        Serial.println("Message published on " + String(topic_out) + ": " + payload);
}