# Details

## Getting started:
* for getting started visit [this](docs/Getting_Started.md)

## TODO :
* [TODO List](docs/TODO.md)

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
This is the updated version of iot_server_v2, and contains:
* minor bug fixes, and more clean up code for authentication and data handling,
* it includes video streaming

### - command to run the server
* cd iot_server_v1
> python3 main.py
