# Details

## Getting started:
* for getting started visit [this](docs/Getting_Started.md)

## TODO :
* [TODO List](docs/TODO.md)

## for other details
* visit [docs](docs/) it contains all the extra information from installation to compilation and internal configurations.

## > examples 
* this directory contains starting point for fastapi and mqtt
---

## > iot_server_v1

This dir contains the work on IOT backend webserver using fastAPI,
several communication protocols have been implemented like RestAPI.

* Note:
    -  docker used is ubuntu arm based as the pi processor is arm64


### - command to run the server
* cd iot_server_v1
> service mosquitto start
> python3 main.py

### - notes on iot_server_v1
* this is version 1 of the iot_server
* This works on RestAPI, hitting the API to get the device status and other information
* capabilities to create/delete user, create/update/delete device
* managing the important configuration like creation, deletion of user and deletion of device only by admin.
* first creation of user is always admin
* database backend is sqlite
---

## > iot_server_v2
This is the updated version of iot_server_v1, and contains:
* minor bug fixes, and more clean up code for authentication and data handling,
* it includes video streaming

### - command to run the server
* cd iot_server_v2
> service mosquitto start
> python3 main.py

## > iot_server_v3
This is the updated version of iot_server_v2, and contains:

* it includes MQTT for communicating with devices
* It includes websocket for updating device status to and from the frontent and send and receive from mqtt.
* few additional improvements to make the code cleaner

### - command to run the server
* cd iot_server_v3
> service mosquitto start
> python3 main.py

## > iot_server_v4
This is the updated version of iot_server_v4, and contains: (work in progress)

* Fetching the device status using api polling instead of websocket
* Working of SQLAlchemy integration

### - command to run the server
* cd iot_server_v4
> service mosquitto start
> python3 main.py
