# RaspyControlLab
Main software repository for the Open-Hardware project (RaspyControl Lab). This laboratory is an initiative to build **open-hardware experiments** in automatic control available for everyone. Follow the instructions to build the software of RaspyControlLab.

![IMG_20220610_205943304](https://user-images.githubusercontent.com/11606241/177064756-751f21b6-fdd3-4ecb-aab0-6fc227649cfa.jpg)
![IMG_20220610_205817676](https://user-images.githubusercontent.com/11606241/177064967-fb3548e2-48d3-4572-8fde-7342ec64ceed.jpg)

## Video

Please, click on the following videos to see some testing examples of the Remote Laboratory **RaspyControlLab**.

<a href="http://www.youtube.com/watch?feature=player_embedded&v=mceNmW32gA0
" target="_blank"><img src="http://img.youtube.com/vi/mceNmW32gA0/0.jpg" 
alt="PI controller example (RaspyControlLab)" width="400" height="300" border="2" /></a>
<a href="http://www.youtube.com/watch?feature=player_embedded&v=nNIj8CU-z-w
" target="_blank"><img src="http://img.youtube.com/vi/nNIj8CU-z-w/0.jpg" 
alt="Access to (RaspyControlLab)" width="400" height="300" border="2" /></a>

# Prerequisites
1. Download a 32-bit Raspberry Pi Os with recommended software from the webpage: https://downloads.raspberrypi.org/raspios_full_armhf/images/raspios_full_armhf-2022-04-07/2022-04-04-raspios-bullseye-armhf-full.img.xz
2. Use the software Raspberry Pi Imager to write this image in a micro sd card. 
3. Take into account that in RaspyControl Lab, we used a Raspberry Pi 4 with RAM of 4GB. Also a model with 2GB is enough for the software requirements.
4. Enable the following interfaces: Camera, VNC, SSH, I2C,SPI of your Raspberry Pi. Use the command sudo raspi-config from a terminal or enter to the Raspberry Pi configuration in your Raspberry Pi OS.

# Instructions for software installation 
1. **Install Janus WebRTC server.** This server allows the real-time video for the laboratory. Runs these commands from a terminal in the Raspberry Pi.
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

-Edit the file janus.plugin.streaming.jcfg with the contents available in the folder Janus in this repository. Use the following command for that:
  ```
  sudo nano opt/janus/etc/janus/janus.plugin.streaming.jcfg
  ```

2. **Install an Apache2 server in your Raspberry Pi and copy the janus html files**
```
sudo apt install apache2 -y
sudo cp -r /home/pi/janus/janus-gateway/html /var/www/janus
```
  -Edit the file 000-default.conf of Apache2 in your Raspberry Pi with the content of the file 000-default.conf (https://github.com/Uniminutoarduino/RaspyControlLab/blob/main/Apache2/000-default.conf) in the folder (Apache2) of this respository

```
sudo nano /etc/apache2/sites-available/000-default.conf
```
  -Enable the proxy mode in the Apache2 server
```
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo service apache2 restart
```

3. **Change the permissions of the folder /var/www to write files in it.**

```
sudo chown -R pi:www-data /var/www
sudo chmod u+rxw,g+rx-w,o-rwx /var/www

```
  -Edit the sudoers file
  
```
sudo nano /etc/sudoers 
(search for these lines and modify them as follows:)
%sudo   ALL=(ALL:ALL) ALL
www-data ALL= NOPASSWD: ALL
```

  -Restart Apache2 service
```
  sudo service apache2 restart
```

4. **Copy the RaspycontrolLab Apache 2 configuration file called "FlaskApp.conf" available in the folder Apache 2 in this repository to the location /etc/apache2/sites-available**
```
sudo cp FlaskApp.conf /etc/apache2/sites-available
```

5. **Copy all contents of the folder FlaskApp available in the folder Apache 2 in this repository inside the location /var/wwww**. Because the file permissions are enabled to write files in the folder /var/www, you can use a simple copy and paste, or use the following commands. 
```
sudo cp -R FlaskApp /var/www
```
6. **Install and enable the WSGI mode. RaspyControl Lab uses this mode to interact with Python language.**

```
sudo apt-get install python3-pip apache2 libapache2-mod-wsgi-py3
sudo a2enmod wsgi
sudo a2enmod headers
sudo a2enmod rewrite
sudo service apache2 restart
```

7. Enable the site "FlaskApp" in Apache
```
sudo aen2site FlaskApp
sudo service apache2 restart
```


8. **Start the Janus WebRTC server. Send a video stream using the tool ffmpeg**. Take in mind that the video port in this case is the 5004, and the video rate is 200Kb/sec.

```
/opt/janus/bin/janus -F /opt/janus/etc/janus/
sudo raspivid -t 0 -w 680 -h 480 -fps 20 -g 75 -b 200000 -n -rot 90 -o - | ffmpeg  -i - -c:v copy -r 20 -bsf dump_extra -maxrate 100K -bufsize 80K -tune zerolatency -f rtp rtp://127.0.0.1:5004?pkt_size=1300

```

9. **Open a browser (Google Chrome or Mozilla Firefox) and type the IP of the Raspberry Pi.** You should see the real-time video of the experiment and the web interface for it.

10. **Copy the folder HardwareX and paste it in your Desktop folder.** Go to the file rc.local and edit it with the contents of the file ("rc.local") provided in this repository.

```
sudo nano /etc/rc.local
```

In this folder, you will find the bash scripts to start the video streaming, the Janus WebRTC server, and the node.js to the real-time plotter. 

- If you want to change the video rate, go to the file "startbashffmpeg.sh". 
- If you want the start process of Janus go to the file startbashjanus.sh. 
- Finally, if you want to change the access to the plotter employing node.js and redis, go to the files "startbashnode.sh" and "servidorwsHX.js".

11. **Reboot your Raspberry Pi.**

```
reboot
```
12. **Install the Python library to manage the 16-bit ADC (ADS1115).** This ADC will read the values of the level from the ultrasonic sensor (US-016).
```
sudo apt-get install build-essential python-dev python-smbus
sudo pip3 install adafruit-circuitpython-ads1x15
sudo pip install adafruit-circuitpython-ads1x15
```

13. **To plot data in real-time from the experiment, we need to install node.js and a redis database.** For that, the steps are:

- Check the system architecture version of your Raspberry Pi
```
uname -m
```
- Get the node.js version for your system architecture. 
```
wget https://nodejs.org/dist/v16.15.1/node-v16.15.1-linux-armv7l.tar.xz
```
- Install node.js
```
tar -xzf node-v16.15.1-linux-armv7l.tar.xz
cd /home/pi/node-v16.15.1-linux-armv7l
sudo cp -R * /usr/local 
```
- If the installation is ready, check the versions of node and npm
```
node -v
npm -v
```
- Install de node.js packages needed to plot data
```
sudo npm install ws
sudo npm install redis  
sudo npm install fs

```

- Install the redis database server
```
sudo apt install redis-server
redis-server –version
redis-cli
```
--  Edit the redis server configuration
```
sudo nano /etc/redis/redis.conf
```
-- Search and put these lines in the redis.conf file
```
#bind 127.0.0.1::1
Bind 0.0.0.0
```
-- Install the Python redis client
```
sudo pip3 install redis
```
The files to start the node.js server and for the plotter are available at the HardwareX folder and in the location /var/www/FlaskApp/templates/plot.html. Please, see these files.

14. **To plot data, we created a small library with redis support known as plotter.** This library is inside the folder /var/www/FlaskApp
- Import the library
```
import plotter as plot #Library to plot data
```
- You can use any of the following functions as you desire. Take into account that data must be in form of string. Therefore, we employed the method str to transform numeric data in string.
```
plot.1m(str(sensor)) #Plot a sample of one sensor, controller, etc.
plot.2m(str(sensor),str(sensor2)) #Plot two samples of sensors, controller, etc.
#Plot three samples of sensors, controller, etc.
plot.3m(str(sensor),str(sensor2),str(sensor3)) 
```

15. **Open a browser (Google Chrome or Mozilla Firefox) and type the IP of the Raspberry Pi.** You should see the real-time video of the experiment and the web interface for it. Test the experiment and the plotter. See the following videos if you have any doubt.

- PI Controller: https://youtu.be/mceNmW32gA0
- Pi Controller with plotter: https://youtu.be/ifcukqjerqE
