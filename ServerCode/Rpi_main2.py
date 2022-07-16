import paho.mqtt.client as mqtt
import time

#Setting up credentials
clientID = '90132f672b'
brokerURL = 'a2gciga1hgsz6v-ats.iot.ap-south-1.amazonaws.com'
brokerport = 8883
mqtt_client = mqtt.Client(clientID)
mqtt_client.tls_set(ca_certs="AmazonRootCA1.crt",certfile="certificate.pem",keyfile="private.pem")
recieved_message = "NULL"

#Setting up a variable for recieved message
def onMessageRecieved(client, userdata, msg):
    print("Received message in topic '{}': {}".format(msg.topic, msg.payload))
    message_string = msg.payload.decode('UTF-8')
    #if message_string == "Hello from server":
    global recieved_message
    recieved_message = message_string

#Connection Response
def onConnection(client, userdata, flags, rc):
    if rc == 0:
        print("Connected succesfully to " + brokerURL + "with result code " + str(rc))
    else:
        print("Connection unsuccessful")

#Connect function for prompted connection
def connectMQTT():
    mqtt_client.connect(host=brokerURL, port = brokerport)
    mqtt_client.on_connect = onConnection

#Subscribing function
def subscribeMQTT(subtopic):
    #print("Subcribing to topic: " + subtopic)
    mqtt_client.subscribe(topic=subtopic)

#Setting up function to publish a message
def publishMesage(pubtopic, message):
    mqtt_client.publish(topic=pubtopic,payload=message,qos=1)

#Setting up Pinout

#Connecting to AWS IoT Core, then sleeping so callback is processed neatly.
connectMQTT()
time.sleep(1)

#Setting up function callbacks
mqtt_client.on_message = onMessageRecieved

while True:
    #Getting a loop to keep callbacks active
    mqtt_client.loop_start()

    #Subscribing to a topic
    client_topic = 'testsub'
    subscribeMQTT(subtopic=client_topic)
    mqtt_client.on_message = onMessageRecieved
    #Publishing message
    #print("Publishing message to topic 'testsub'")
    #publishMesage(pubtopic='testsub',message="Hello")
    timeStamp = time.time()
    timeStamp = str(timeStamp)
    if recieved_message == "Hello from server":
        hellomsg = '{"id":"'+ clientID + timeStamp +'",'+'"message":"Hello from Raspberry Pi"}'
        publishMesage(pubtopic=client_topic,message=hellomsg)
        recieved_message = "NULL"
    if recieved_message == "NULL":
        recieved_message = recieved_message
    time.sleep(3)
    mqtt_client.loop_stop()