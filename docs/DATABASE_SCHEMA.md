# How Database is structure

- there are 2 separate databases
    - Users 
    - Devices
- the DB is sqlite
- using ORM sqlalchemy for working with Database throuugh python.

## User
* it stores all the informatin of the user in each row
* It has 5 columns-
    - `id` -> (type : int) Unique for each row
    - `username` -> (type : string) as name suggest its stores name of the user.
    - `email` -> (type : string) must be unique for each user
    - `hashed_password` -> (type : string) password encrypted by passlib for extra security.
    - `isadmin` -> (type : bool) store True or False, if True the user get root privileges, and so he can delete or create users and devices.

## Device
* it stores information of the device in each row
* It has 6 columns:
    - `id` -> (type : int) Unique for each row
    - `name` -> (type : string) Device name
    - `topic_name` -> (type : string) Must be unique 
    - `status` -> (type : float) switch status of the device either True or False (where True == On and False == Off)
    - `gpio_pin` -> (type : int) gpio pin assigned to the device
    - `extra_details` -> (type : float) store the extra information like temperature value or speed of fan etc.