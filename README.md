# RaspyControlLab
Main software repository for the Open-Hardware project (RaspyControl Lab). Follow the instructions to build the software of RaspyControlLab.


# Prerequisites
1. Download a 32-bit Raspberry Pi Os with recommended software from the webpage: https://downloads.raspberrypi.org/raspios_full_armhf/images/raspios_full_armhf-2022-04-07/2022-04-04-raspios-bullseye-armhf-full.img.xz
2. Use the software Raspberry Pi Imager to write this image in a micro sd card. 
3. Take into accpunt that in RaspyControl Lab, we used a Raspberry Pi 4 with RAM of 4GB. Also a model with 2GB is enough for the software requirements.

# Software Installation Instructions
1. Install Janus WebRTC server. This server allows the real-time video for the laboratory.
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
