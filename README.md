# piMatrix
Ascii code to make a raspberry pi and camera an ascii webcam

## Overview
This was a hackday project for a raspberry pi and the camera module. You will need 3 things;

* RaspberryPi running Raspbian Jessie, camera pi module and an internet connection. Also some python libraries
* A Web Server running apache and jquery. Also some pythion libraries

### Client
Run Raspbian Jessie pi and ensure the camera is enabled using this guide - [link](https://thepihut.com/blogs/raspberry-pi-tutorials/16021420-how-to-install-use-the-raspberry-pi-camera)

Then get and run the setup.sh script in the client folder like below;

```
wget -q https://raw.githubusercontent.com/iaingblack/piMatrix/master/client/setup.sh -O setup.sh
chmod +x setup.sh
sudo setup.sh
```

### Server/Web
Create an Ubuntu 14.04 x64 server (I tested on Digital Ocean)

Then get and run the setup.sh script in the server folder like below;

```
wget -q https://raw.githubusercontent.com/iaingblack/piMatrix/master/server/setup.sh -O setup.sh
chmod +x setup.sh
sudo setup.sh
```