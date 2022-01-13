# CRUD Operations on database

## Device DB
* GET request:
    - `/devices` - return the list of all the devices
        - return type :  **Json** - List of all devices
    - `/device/{device_id}` - return the specific device based on the device id.
        - return type :  **Json** - device
* POST request:
    - `/device` - create new device, post parameters are specified in `DATABASE_SCHEMA.md` in device section.
        - return type :  **Json** - device
* PUT request:
    - `/device` - updating the status and other parameter of the device.
        - take inputs :
            - `id` - device id, `status` - switch status
        - return type :  **Json** - device

* Delete request:
    - Note : requires admin privileges to perform this operations.
    - `/device/{device_id}` - delete the particular device from DB
        - return type:  **Json** - device
    - `/devices` - delete all the devices from the DB
        - return type : **Json** - list of all devices

## USER DB
* Note: all operation require admin priveleges, hence first user by default is admin.
* GET request:
    - `/user/{user_id}` - return the specific user based on the device id.
        - return type :  **Json** - User
* POST request:
    - `/user` - create new user, post parameters are specified in `DATABASE_SCHEMA.md` in User section.
        - return type :  **Json** - User

* Delete request:
    - `/user/{user_id}` - delete the particular user from DB
        - return type:  **Json** - user
    
