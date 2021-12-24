# "fastAPI_IOT_version1"

This repo contains the work on IOT backend webserver using fastAPI,
several communication protocols have been implemented like RestAPI, WebSocket and MQTT

* Note:
    -  docker used is ubuntu arm based as the pi processor is arm64


## command to run the server
* cd iot_server_v1
> python3 main.py

### notes on iot_server_v1
* this is version 1 of the iot_server
* This works on RestAPI, hitting the API to get the device status and other information
* capabilities to create/delete user, create/update/delete device
* managing the important configuration like creation, deletion of user and deletion of device only by admin.
* first creation of user is always admin
* database backend is sqlite


## dependencies 
* ubuntu packages:
    - apt-get install -y fish python3-pip curl
    - apt install net-tools
    <!-- - apt-get install sqlitebrowser 
    (sqlitebrowser is https://sqlitebrowser.org/) -->


### for using localtunnel ( a proxy for webserver ) [reference](https://localtunnel.github.io/www/)
* linux command
    - curl -sL https://deb.nodesource.com/setup_14.x | bash - 
    - apt-get install -y nodejs
    - npm install -g localtunnel
    - lt --port 8000

### python packages:
- pip install --upgrade pip
- pip install -r requirements.txt

-----

## Mosquitto Installation

### Installing MQTT server (mosquitto)
- apt install software-properties-common
- apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
- apt-get update
- apt-get install mosquitto

### Starting mosquitto broker
- service mosquitto start
- service mosquitto status # checking the status

> Mosquitto authentication: [reference](https://www.youtube.com/watch?v=AsDHEDbyLfg)
* Note : when changes are done and password is created run the following command
    - service mosquitto restart

* Current authorization : is
    - Username : iot_test_v1
    - Password :yashveer

* command used to create the user name and password: 
mosquitto_passwd -c /etc/mosquitto/passwd_file iot_test_v1

---
## Working with Docker
### Saving the docker container methods
- docker commit <container_id> <new_image_name>:version<number>
- docker save -o <output_filename>.tar <new_image_name>:version<number>

### Running on Docker:

* for rasbian docker issue: [error_reference](https://askubuntu.com/questions/1263284/apt-update-throws-signature-error-in-ubuntu-20-04-container-on-arm)

- docker run -it -v /home:/home -p 8000:8000 --network "host" --name ubuntu_port_testing_1 --security-opt seccomp:unconfined ubuntu:latest


## TODO
[x] made more secure backend (fastAPI)
* add video streaming platform [reference](https://stackoverflow.com/questions/65971081/stream-video-to-web-browser-with-fastapi)

## Reference 
* https://pythonrepo.com/repo/sabuhish-fastapi-mqtt-python-fastapi-utilities
* https://github.com/sabuhish/fastapi-mqtt/blob/master/docs/getting-started.md
* https://fastapi.tiangolo.com/tutorial/
* Home automation Info videos :  https://www.youtube.com/channel/UC75HTMhqVZs0sPOMTMQqI9g
## Additional details:
    https://docs.google.com/document/d/1t5qNqFk1zkpqU8hp0CfM5sPngBX_D-aD8vrElaOjCCc/edit