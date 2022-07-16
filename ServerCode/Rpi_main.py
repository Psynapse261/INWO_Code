from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder

#Setting up a variable for recieved message
def OnMessageRecieved(topic, payload, dup, qos, retain):
    print("Received message from topic '{}': {}".format(topic, payload))
    recieved_message = payload
    return recieved_message

#Connecting to AWS IoT Core
def connectMQTT(connection):
    print("Connecting to endpoint with client ID" + connection.client_id)
    #Waiting till a connection is made
    connect_future = connection.connect()
    connect_future.result()
    print('Connected!')

#Subscribing function
def subscribeMQTT(topic, connection):
    print("Subcribing to topic: " + topic)
    connection.subscribe(topic=topic, qos=mqtt.QoS.AT_LEAST_ONCE, callback=OnMessageRecieved())

#Setting up function to publish a message
def publishMesage(topic, message, connection):
    connection.publish(
                topic=topic,
                payload=message,
                qos=mqtt.QoS.AT_LEAST_ONCE)

#Setting up Pinout


while True:
    #Setting up mqtt credentials
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

    mqtt_connection = mqtt_connection_builder(
        endpoint='a2gciga1hgsz6v-ats.iot.us-west-2.amazonaws.com',
        port=8883,
        cert_filepath='certificate.pem.crt',
        pri_key_filepath='private.pem.key',
        client_bootstrap=client_bootstrap,
        ca_filepath='AmazonRoot-CA1.pem',
        on_message_received= OnMessageRecieved, 
        client_id='90132f672b',
        clean_session=False,
        keep_alive_secs=6)

    #Subscribing to a topic
    subscribeMQTT(topic='testsub',connection=mqtt_connection)
    #Publishing message
    publishMesage(topic='testsub',message='Hello',connection=mqtt_connection)




