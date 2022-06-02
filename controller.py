# Controller program
'''
    Imports and argument
'''
from datetime import datetime
import argparse
import json
import os
import paho.mqtt.client as paho
import pathlib
import ssl


# Arguments received when run
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--action', type=str, help='Action performed on the UAV')
parser.add_argument('-v', '--value', type=int, help='Value associated with the action')
parser.add_argument('-f', '--flight_plan', type=pathlib.Path, help='Specify a file.txt with the flight plan')
parser.add_argument('-o', '--only_publish', action='store_true', help='Only publish commands, not subscribe')
args = parser.parse_args()



'''
    Functions
'''
# Function to clear the screen
def clear_screen():
    # It is for MacOS and Linux
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # It is for Windows platfrom
        _ = os.system('cls')


# Function to show the log
def log(string):
    string = '[' + str(datetime.now()).split('.')[0] + ':' + str(datetime.now()).split('.')[1]  + '] ' + string
    print(string)


# Function to update the 'commands' topic JSON message topic
def json_update_commands(action, value=0):
    if value is None: value = 0 # Check if value is None

    # JSON message
    message = {
        "time": str(datetime.now()).split('.')[0] + ':' + str(datetime.now()).split('.')[1],
        "action": action,
        "value": value
    }
    return json.dumps(message) # JSON updated


# ON connect function
def on_connect(client, userdata, flags, rc):
    # First log
    log("on_connect({}, {}, {}, {})".format(client, userdata, flags, rc))
    # Subscribe to the UAV state topic, with qos = 1
    client.subscribe(state, qos=1)
    # Subscribe to the command confirmation topic
    client.subscribe(processed, qos=1)


# ON message function
def on_message(client, userdata, msg):
    # Decode the received message
    message = msg.payload.decode("utf-8")
    # Message log
    log("{}: {}".format(msg.topic, message))


# ON log function
def on_log(client, userdata, level, buf):
    print("log: ", buf)   


# ON disconnect funcion
def on_disconnect(client, userdata, rc):
    if rc != 0:
        log('Unexpected disconnection. Reconnecting...')


# Main function
def main():
    #clear_screen() # Cleaning the screen...
    
    while True: # While it's true
        client.loop() # Client loop...



'''
    Main
'''
if __name__ == '__main__':
    # Certificate paths
    cert_path = 'certs'
    ca_cert = os.path.join(cert_path, "ca.crt")
    client_cert = os.path.join(cert_path, "device002.crt")
    client_key = os.path.join(cert_path, "device002.key")

    # Create client object
    client = paho.Client(protocol=paho.MQTTv311)

    # Configuring the TLS certificate
    client.tls_set(ca_certs=ca_cert,
    certfile=client_cert,
    keyfile=client_key,
    tls_version=ssl.PROTOCOL_TLSv1_2)

    # Server hostname verification in server certificate
    # In this case, it is True for non-verification (fix soon)
    client.tls_insecure_set(True)

    # Username and password to connect to the broker
    client.username_pw_set("admin", password="admin")
    # Connecting to the broker
    client.connect('200.144.244.229', port=8083)

    # UAV identification (ID)
    uav_id = 'uav01'
    # Main topic with UAV identification
    main_topic = "iod/" + str(uav_id) + '/'
    # Topic where UAV state is sent
    state = str(main_topic)+'state'
    # Topic where the confirmation of commands is sent
    processed = str(main_topic)+'processed'
    # Topic where the command for the UAV is received
    commands = str(main_topic)+'commands'

    # Check if actions have been provided
    if args.flight_plan != None: # Flight plan provided
        with args.flight_plan.open('r') as file: # File for reading
            for row in file: # Going through the .txt file
                try:
                    client.publish(commands, json_update_commands(row.split()[0], row.split()[1]))
                except IndexError: # Value not informed
                    client.publish(commands, json_update_commands(row.split()[0], 0))
    elif(args.action != None): # An action was informed by parameter
        client.publish(commands, json_update_commands(args.action, args.value))

    client.on_connect = on_connect
    client.on_message = on_message
    #client.on_log = on_log
    client.on_disconnect = on_disconnect

    if args.only_publish: # Only publish
        exit() # Finish the execution

    # Execute main function
    main()
