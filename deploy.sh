#!/usr/bin/env bash

cd /home/pi/playspace
echo 'Removing current dirs'
if [ -d rpi_cam-0.1-dev/ ]; then
	sudo rm -Rf rpi_cam-0.1-dev/
fi
if [ -f rpi_cam-0.1-dev.tar.gz ]; then
	#sudo rm -Rf rpi_cam-0.1-dev.tar.gz
	echo '!!!'
fi
echo 'Uninstalling pip rpi_cam'
#sudo pip uninstall rpi_cam &&
echo 'Extracting new build'
tar -xvf rpi_cam-0.1-dev.tar.gz &&
echo 'Installing new'
cd rpi_cam-0.1-dev/
sudo python setup.py install &&
echo 'Running app.py'
python rpi_cam/app.py

