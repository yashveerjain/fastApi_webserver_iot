# Compiling Code to protect the Code Base when distributing

* using [pyinstaller](https://pyinstaller.readthedocs.io/en/stable/usage.html) to convert the python code to binary file to be used by other platforms as well without sharing the actual code.

## steps 
* download PyInstaller
> pip install pyinstaller
* check whether the download was successful
> pyinstaller
* run the following command inside the app dir (iot_server_v3/)
> pyinstaller main.py --hidden-import passlib.handlers.bcrypt --hidden-import main  --specpath temp_dir2 --distpath temp_dir2/dist --workpath temp_dir2/build

    
## important note:
- in above command few things need to be present
    - `--hidden-import passlib.handlers.bcrypt` as the pyinstaller is unable to detect this module
    - `--hidden-import main` this is for the uvicorn, as unvicorn.run() needs the py filename(in our case its main.py) and the appname (in our case its `app`), eg: `uvicorn.run("main:app",host="0.0.0.0")`
    - in command there is `temp_dir2` in multiple arguments, this is the dirname where you can store the compiled script in one place, change the name according to you desire.
- in the app dir (eg: iot_server_v3) delete the __init__.py file if present.
    - eg : iot_server_v3/__init__.py if present remove it.
    - only remove this one file **do not remove** other __init__.py present in sub directories.





