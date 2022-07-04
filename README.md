# RaspyControlLab
Main software repository for the Open-Hardware project (RaspyControl Lab). This laboratory is an initiative to build open-hardware experiments in automatic control available for all. Follow the instructions to build the software of RaspyControlLab.

![IMG_20220610_205943304](https://user-images.githubusercontent.com/11606241/177064756-751f21b6-fdd3-4ecb-aab0-6fc227649cfa.jpg)
![IMG_20220610_205817676](https://user-images.githubusercontent.com/11606241/177064967-fb3548e2-48d3-4572-8fde-7342ec64ceed.jpg)


# Prerequisites
1. Download a 32-bit Raspberry Pi Os with recommended software from the webpage: https://downloads.raspberrypi.org/raspios_full_armhf/images/raspios_full_armhf-2022-04-07/2022-04-04-raspios-bullseye-armhf-full.img.xz
2. Use the software Raspberry Pi Imager to write this image in a micro sd card. 
3. Take into account that in RaspyControl Lab, we used a Raspberry Pi 4 with RAM of 4GB. Also a model with 2GB is enough for the software requirements.

# Instructions for software installation 
1. Install Janus WebRTC server. This server allows the real-time video for the laboratory. Runs these commands from a terminal in the Raspberry Pi.
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install libmicrohttpd-dev libjansson-dev     libnice-dev libssl-dev libsrtp-dev libsrtp2-dev libsofia-sip-ua-dev     libglib2.0-dev libopus-dev libogg-dev libini-config-dev     libcollection-dev pkg-config gengetopt libtool automake dh-autoreconf
cd ~
mkdir janus && cd janus
git clone https://github.com/meetecho/janus-gateway.git
cd janus-gateway
sudo apt-get install libconfig-dev
sh autogen.sh
./configure --disable-websockets --disable-data-channels \
--disable-rabbitmq --disable-docs --disable-mqtt --prefix=/opt/janus
make
sudo make install
sudo make configs
```

2. Install an Apache2 server in your Raspberry Pi
```
sudo apt install apache2 -y
sudo cp -r /home/pi/janus/janus-gateway/html /var/www/janus
```
  -Edit the file 000-default.conf of Apache2 in your Raspberry Pi with the content of the file 000-default.conf (https://github.com/Uniminutoarduino/RaspyControlLab/blob/main/Apache2/000-default.conf) in the folder (Apache2) of this respository

```
sudo nano /etc/apache2/sites-available/000-default.conf
```
  -Enable proxy mode in the Apache2 server
```
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo service apache2 restart
```




