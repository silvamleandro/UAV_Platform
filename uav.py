# UAV program
'''
    Imports and argument
'''
from datetime import datetime
from djitellopy import Tello
from time import sleep
import argparse
import json
import os
import paho.mqtt.client as paho
import ssl


# Argument received when run
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--tello', action='store_true', help='Tello is available')
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


# Function to update the 'state' topic JSON message topic
def json_update_state(pry, speed, temperature, battery, height):
    # JSON message
    message = {
        "time": str(datetime.now()).split('.')[0] + ':' + str(datetime.now()).split('.')[1],
        "pry": pry,
        "speed": speed,
        "temperature": temperature,
        "battery": battery,
        "height": height
    }
    return json.dumps(message) # JSON updated


# Function to update the 'processed' topic JSON message topic
def json_update_processed(action):
    # JSON message
    message = {
        "time": str(datetime.now()).split('.')[0] + ':' + str(datetime.now()).split('.')[1],
        "action": action
    }
    return json.dumps(message) # # JSON updated


# ON connect function
def on_connect(client, userdata, flags, rc):
    # First log
    log("on_connect({}, {}, {}, {})".format(client, userdata, flags, rc))
    # Subscribe to the UAV commands topic, with qos = 1
    client.subscribe(commands, qos=1)


# ON message funcion
def on_message(client, userdata, msg):
    # Decode the received message
    message = msg.payload.decode("utf-8")
    # Message log
    log("{}: {}".format(msg.topic, message))

    # Check which topic is the message
    if msg.topic == commands:
        try:
            # Parsing the message to JSON...
            parse = json.loads(message)

           # Execute the action
            if execute(parse): 
                # Confirm the execution of the action
                confirmation(parse)

        except ValueError:
            # If there is an error in the JSON
            log('Error in command received')


# ON log function
def on_log(client, userdata, level, buf):
    print("log: ", buf)   


# ON disconnect funcion
def on_disconnect(client, userdata, rc):
    if rc != 0:
        log('Unexpected disconnection. Reconnecting...')


# Function to perform the UAV action
def execute(dictionary):
    # The ranges for validating the value were defined based on the djitellopy lib

    if dictionary['action'] == 'takeoff':
        log('Taking off...')
        # Send command to Tello
        tello.takeoff() if args.tello else None

    elif dictionary['action'] == 'land':
        log('Landing...')
        # Send command to Tello
        tello.land() if args.tello else None

    elif dictionary['action'] == 'up':
        log('Ascending to ' + str(dictionary['value']) + ' cm')
        # Send command to Tello (with value validation)
        if args.tello and (20 <= dictionary['value'] <= 500):
            tello.move_up(dictionary['value'])

    elif dictionary['action'] == 'down':
        log('Descending to ' + str(dictionary['value']) + ' cm')
        # Send command to Tello (with value validation)
        if args.tello and (20 <= dictionary['value'] <= 500):
            tello.move_up(dictionary['value'])

    elif dictionary['action'] == 'forward':
        log('Flying forward for ' + str(dictionary['value']) + ' cm')
        # Send command to Tello (with value validation)
        if args.tello and (20 <= dictionary['value'] <= 500):
            tello.move_forward(dictionary['value'])

    elif dictionary['action'] == 'backward':
        log('Flying backward for ' + str(dictionary['value']) + ' cm')
        # Send command to Tello (with value validation)
        if args.tello and (20 <= dictionary['value'] <= 500):
            tello.move_back(dictionary['value']) 

    elif dictionary['action'] == 'left':
        log('Flying left for ' + str(dictionary['value']) + ' cm')
        # Send command to Tello (with value validation)
        if args.tello and (20 <= dictionary['value'] <= 500):
            tello.move_left(dictionary['value']) 

    elif dictionary['action'] == 'right':
        log('Flying right for ' + str(dictionary['value']) + ' cm')
        # Send command to Tello (with value validation)
        if args.tello and (20 <= dictionary['value'] <= 500):
            tello.move_right(dictionary['value'])

    elif dictionary['action'] == 'rotate_clockwise':
        log('Rotating ' + str(dictionary['value']) + ' degrees clockwise')
        # Send command to Tello (with value validation)
        if args.tello and (1 <= dictionary['value'] <= 360):
            tello.rotate_clockwise(dictionary['value'])

    elif dictionary['action'] == 'rotate_counterclockwise':
        log('Rotating ' + str(dictionary['value']) + ' degrees counterclockwise')
        # Send command to Tello (with value validation)
        if args.tello and (1 <= dictionary['value'] <= 360):
            tello.rotate_counter_clockwise(dictionary['value'])

    else:
        log('No action is valid')
        return False # Action was not executed

    return True # Action was executed


# Function to confirm the execution of an action
def confirmation(parse):
    log('Confirming action execution: ' + parse['action'])
    # Confirming command execution
    client.publish(processed, json_update_processed(parse['action']), qos=1)


# Class applied in Expection
class MQTTClientDisconnected(Exception):
    pass


# Main function
def main():
    #clear_screen() # Cleaning the screen...
    client.loop_start() # Start client loop
    
    try:
        while True:
            log("Sending UAV state data")
            # Publishing UAV state data
            if args.tello: # Tello is available            
                client.publish(state, json_update_state(f'{tello.get_pitch()} {tello.get_roll()} {tello.get_yaw()}',
                                                        f'{tello.get_speed_x()} {tello.get_speed_y()} {tello.get_speed_z()}',
                                                        f'{tello.get_temperature()}',
                                                        f'{tello.get_battery()}',
                                                        f'{tello.get_height()}'))
            else: # Simulated data
                client.publish(state, json_update_state('000 000 000', '000 000 000', '000', '000', '000'))
            
            sleep(5) # Wait 5 seconds
    except MQTTClientDisconnected: # MQTT client disconnected
        log("Client disconnected. Reconnecting...")
    except BaseException as msg: # Base expection
        log("Error in main() loop. Stopping Threads... {}".format(msg))
        client.loop_stop() # End client loop



'''
    Main
'''
if __name__ == '__main__':
    # Certificate paths
    cert_path = 'certs'
    ca_cert = os.path.join(cert_path, "ca.crt")
    client_cert = os.path.join(cert_path, "device001.crt")
    client_key = os.path.join(cert_path, "device001.key")

    # Tello is available
    if args.tello:
        tello = Tello() # Create Tello object
        tello.connect() # Enter SDK mode

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

    client.on_connect = on_connect
    client.on_message = on_message
    #client.on_log = on_log
    client.on_disconnect = on_disconnect

    # Execute main function
    main()
