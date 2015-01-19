# FIPV - FakeInternetPointViewer

##Requirements:

  - Raspberry Pi (connected to internet)
  - OS: Rapsbian Weezy http://downloads.raspberrypi.org/raspbian_latest (did not try with any other OS)
  - Breadboard, jumperwires, LCD-Display (HD44780 - Controller)

##Connecting the Hardware
After setting up the raspberry pi itself, the cables need to be connected in the following way:

|  LCD contact | to GPIO-Pin |
|:------------:|:-----------:|
|    1 (GND)   |   6 (GND)   |
|    2 (+5V)   |   2 (+5V)   |
| 3 (Kontrast) |   6 (GND)   |
|    4 (RS)    |  26 (GPIO7) |
|    5 (R/W)   |   6 (GND)   |
|     6 (E)    |  24 (GPIO8) |
| 11 (Daten 4) | 22 (GPIO25) |
| 12 (Daten 5) | 18 (GPIO24) |
| 13 (Daten 6) | 16 (GPIO23) |
| 14 (Daten 7) | 12 (GPIO18) |
| 15 (LED +5V) |   2 (+5V)   |
| 16 (LED GND) |   6 (GND)   |

The circuit layout I used can be found here at http://schnatterente.net :

> http://www.schnatterente.net/img/articles/raspberrypi-display/raspberry-pi-display-aufbau.png

I know that is not the same display used in my imgur-post (http://imgur.com/gallery/az8Am) but the layout on my display contacts was the same, just split in two rows. 


## Installation


###Requirements for installing the imgur-API

```sh
$ sudo apt-get update && sudo apt-get upgrade && sudo apt-get dist-upgrade
$ sudo apt-get install python-pip
```
###Installing the imgur-API
```sh
$ pip install imgurpython
```

###Registering your client at imgur
Visit
> https://api.imgur.com/oauth2/addclient

to obtain your *client-id* and *client-secret* for the script (see lines 21 & 22 in fipv_piversion.py)
###Installing FIPV on your Raspberry PI

```sh
$ git clone https://github.com/sbasht/fipv
$ cd fipv
$ nano fipv_piversion.py
```
Go to following lines in the beginning of the script and change client_id, client_secret and the username to the data you obtaint from registering your application / you know your username (by the way works with every other username) :
```
#########################################
#HERE COMES THE PART WHERE YOU NEED TO CHANGE SOMETHING
#
#To get your client_id and client_secret you need to register
# at https://api.imgur.com/oauth2/addclient
##########################################
#
#
client_id = 'YOUR CLIENT ID'
client_secret = 'YOUR CLIENT SECRET'
username="YOUR USERNAME"
DISPLAY_WIDTH = 24 #How many chars fit into one line of the display
#
#
#########################################
```

##Running FIPV

To use this program (and talk to the GPIOs) currently the only option working for me is running the script with root-privileges. Therefore:


```sh
$ sudo python fipv_piversion.py
```

##Version
0.1
##Known Bugs
- If the last submission was an album, it will crash. (Fix is currently being tested)
- If imgur is over capacity, it will crash. (try/except will be included)


