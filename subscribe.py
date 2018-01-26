import paho.mqtt.client as mqtt
from collections import namedtuple


TEMPERATURE='temperature'
HUMIDITY='humidity'



Property = namedtuple('Property', ['topic', 'type'])

devices =[
    {
        "id": "d55c4200",
        "iota_id": "xxx",
        "properties":[
            Property("temperature/degrees", type=TEMPERATURE),
            Property("humidity/percentage", type=HUMIDITY)
        ]        
    },
    {
        "id": "30aea4379688",
        "iota_id": "xxx",
        "properties":[
            Property("temperature/degrees", type=TEMPERATURE),
            Property("humidity/percentage", type=HUMIDITY)
        ]
    },
]



def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    for device in devices:
        for prop in device["properties"]:
            client.subscribe("homie/{}/{}".format(device["id"], prop.topic))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    device = [device for device in devices if device["id"]==msg.topic.split("/")[1]][0]
    if device:
        prop = [prop for prop in device["properties"] if prop.topic == "/".join(msg.topic.split("/")[2:])][0]
        
        print "SEND TO IOTA, DEVICE:{}, TYPE:{}, VALUE:{}".format(device["id"], prop.type, msg.payload)
        

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.178.37", 1883, 60)

client.loop_forever()