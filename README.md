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

## > iot_server_v4
This is the updated version of iot_server_v3, and contains

* minor bug fixes, and more clean up code for authentication and data handling,
* it includes MQTT for communicating with devices
* It includes websocket for updating device status to and from the frontent and send and receive from mqtt.
* few additional improvements to make the code cleaner

* Fetching the device status using api polling instead of websocket
* Working of SQLAlchemy integration

### - command to run the server
* cd iot_server_v4
> service mosquitto start
> python3 main.py
