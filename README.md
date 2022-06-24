# Platform for UAV Controlling

This project aims to develop an MQTT platform for UAV control applying the detection of attacks on the wireless network. Thus, two programs are built: one for the controller and the other for the Raspberry Pi, which is responsible for communicating with the UAV. The connection between the Raspberry Pi and the UAV is through the wireless network, so a machine learning model is generated in order to detect attacks, such as Wi-Fi deauthentication and cracking.

The group for this project is composed of the following members:

- Henrique Bonini de Britto Menezes: henrique.menezes@usp.br;
- Leandro Marcos da Silva: leandro.marcos@usp.br;
- Matheus dos Santos Luccas: matheus.luccas@usp.br.

## Technologies and Tools Used
The technologies and tools in the sequence have been used for the development of this project so far. However, other tools can be added in future modifications, for example, the addition of some Graphical User Interface (GUI).

- **DJI Tello** Consists of an extremely light UAV with only 80 g counting the propellers and battery, low cost and portable, in addition to being designed for beginners in the area. The UAV can fly up to 13 minutes at a speed of 28.8 km/h within a radius of up to 100 meters away;
- **Python:** Simple, versatile programming language and has a huge amount of libraries, such as paho-mqtt and djitellopy;
- **Raspberry Pi Zero W:** Single-board computer with low cost and accessible to students in general. The Zero W model is an evolution of the Zero model, with 802.11n wireless connection and bluetooth 4.0;
- **Eclipse Mosquitto:** Broker server that is easy to install and configure. Also, it's open source and has an image on Docker Hub;
- **Eclipse Paho:** Library to implement the MQTT client, that is, to send and receive messages. The Mosquitto Python Client project was donated to Eclipse Paho in June 2013, and allows integration with several programming languages as well, such as C or Java;
- **OpenSSL:** Allows the generation of X.509 certificates, in the X.509 Public Key Infrastructure (PKI) standard and encrypted with SHA-256.

-----

## Configuration and Execution

To run the programs, it is necessary to have [Python 3.6+](https://www.python.org/) and install the following libraries:

````
pip install paho-mqtt
pip install djitellopy
````

Also, it is possible to install the libraries through ```requirements.txt```:

```
pip install -r requirements.txt
```

__Note 1:__ It is possible to create a virtual environment too. However, don't forget to activate it when installing the libraries and running the code.

__Note 2:__ The ```djitellopy``` library is only used in the _uav.py_ script, so no need to install on the controller. And for the library to work correctly, it is necessary to install OpenCV and libatlas on the OS through the commands:

```
sudo apt-get install python3-opencv
sudo apt-get install libatlas-base-dev
```

In addition, it is possible to configure your MQTT broker address and SSL/TLS certificates in the codes. As the platform supports DJI Tello, it is necessary to configure your network on the Raspberry Pi or any other device that will connect with the UAV. On Linux systems, it can be done by editing the file ```/etc/wpa_supplicant/wpa_supplicant.conf``` and creating an entry:

````
network={
    ssid="TELLO SSID"
    psk="TELLO PASSWORD"
}
````

To initialize receiving commands and publishing UAV state, run the command ```python3 uav.py```. The _-t_ or _--tello_ parameter is to inform that DJI Tello is available to receive commands. Then, check if Tello is connected to the network before informing this parameter. Also, the drone state is published every two seconds, being sent pitch, yaw, roll, speed on three axes (x, y, z), average temperature, battery level, and height.

If it gets the error "Python [Errno 98] Address already in use" when rerunning with DJI Tello, it will need to terminate the process:

```
ps -fA | grep python
kill -9 process_id
```

Commands are sent by the controller through the command ```python3 controller.uav```, addition to receiving the UAV state. There are two ways to enter commands: single command and flight plan. The single command is informed in the _-a_ or _--action_ parameter, and its respective value in the _-v_ or _--value_ parameter. For example, the command ```python3 controller.py -a left -v 10``` makes the UAV fly left for 10 cm. The second way is to use the .txt file with the flight plan defined, as defined in the example _flight_plan.txt_. To enter a text file, the _-f_ or _--flight_plan_ parameter is required. Below are the possible actions implemented in this project:

- **takeoff:** take off the UAV;
- **land:** land the UAV;
- **up _value_:** ascend to _value_ cm;
- **down _value_:** descend to _value_ cm;
- **forward _value_:** fly forward for _value_ cm;
- **backward _value_:** fly backward for _value_ cm;
- **left _value_:** fly left for _value_ cm;
- **right _value_:** fly right for _value_ cm;
- **rotate_clockwise _value_:** rotate _value_ degrees clockwise;
- **rotate_counterclockwise _value_:** rotate _value_ degrees counterclockwise.

__Note 3:__ The _-o_ or _--only_publish_ parameter is used only publish commands, not subscribe.

__Note 4:__ For the DJI Tello to work with the application, its firmware needs to be updated to the latest version. In addition, some bugs may occur, so it is recommended to connect the drone to the smartphone and fly, and then connect to the platform.

-----

## Next Steps

The next steps for this project are:

- Fix issue with SSL/TLS certificate present in recent versions of Python;
- Build the model to detect wireless network attacks.

__Note:__ The dataset to train the model against wireless attacks was provided from the _[ECU-IoFT](https://github.com/iMohi/ECU-IoFT)_ repository.
