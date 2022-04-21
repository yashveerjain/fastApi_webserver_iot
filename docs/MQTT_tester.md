# To test the MQTT broker 

## Start the broker
> service mosquitto start

## Sub to all topic
>mosquitto_sub -t "#" -v -u home_automation_v1 --pw yashveer

## Pub to one topic
>mosquitto_pub -t "room1/device1000" -u home_automation_v1 --pw yashveer -m "on"
