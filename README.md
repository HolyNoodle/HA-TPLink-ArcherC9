# HA-TPLink-ArcherC9
Custom component for device tracking platform in Home assistant. Works on Archer C9 v5

# Installation
1. Put the `tplink_archer_c9.py` into the `config/custom_components/device_tracker/` folder

2. `configuration.yaml`:

        device_tracker:
        - platform: bluetooth_tracker
        - platform: tplink_archer_c9
          host: HOST IP # 192.168.0.1
          password: "md5 encrypted password" 
 
3. Restart !

# Getting your md5 encrypted password

Information extracted from [https://www.home-assistant.io/components/device_tracker.tplink/](https://www.home-assistant.io/components/device_tracker.tplink/)

For Archer C9 models running firmware version 150811 or later please use the encrypted password you can retrieve like this:

1. Go to the login page of your router. (default: 192.168.0.1)
2. Type in the password you use to login into the password field.
3. Click somewhere else on the page so that the password field is not selected anymore.
4. Open the JavaScript console of your browser (usually by pressing F12 and then clicking on “Console”).
5. Type document.getElementById("login-password").value; or document.getElementById("pcPassword").value;, depending on your firmware version.
6. Copy the returned value to your Home Assistant configuration as password.

#  Works on
Harware: Raspberry Pi 3 B+
Python: 3.6.6
Hassio: 0.79.2
Archer C9 v5 : 1.2.2 Build 20180423 rel.85787(4555)

(Hassio connected through RJ45 to the router)

# Usage
This code has been written by me and tested on my own router. 
I can not assure you it will work. I can not be blamed for any problem with this code.
I guess you should not have any major issues with it.
