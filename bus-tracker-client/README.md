# Bus Client 🚍  

Each bus is tracked with a GPS sensor. For the demo we created a smartphone app that sends the location and that allows the user to set the number of busy seats and the next stop. We used MIT App Inventor, a tool for creating apps without coding, we were curious about its capabilities. We have to say that, for developers like us, a classic Java Android Application would have been much easier to build, however for the simplest application (not like this one), MIT AI is a nice tool, also considering that can generate multi-platform apps.

The bus sends via MQTT the requested data, and it is notified on the same topic when someone asks for help at his next stop.

| Topic | Payload - Examples|
|-|-|
|`devices/buses/id_bus` | {"id_bus":01,"latitude":44.8909336,"longitude":11.0672094,"seats_count":2,"fermata":"61035"}`|
|`devices/buses/id_bus`|{"fragile": True}
