#This file is if you want to build it yourself. This script MUST be run with sudo. This will also install this app with your permission
echo Installing Packages
sudo apt install python3
sudo apt install python3-pip
#Installing required outer packages
pip3 install pyinstaller
pip3 install psutil
#Installing pyinstaller compiler and psutil library
echo Compiling...
pyinstaller --onefile dgraph.py
pyinstaller --onefile mgraph.py
pyinstaller --onefile pmgraph.py
#Compiling code
cp ./dist/dgraph .
cp ./dist/mgraph .
cp ./dist/pmgraph .
#Copying binary out
rm -rf build
rm -rf dist
#Cleaning up
read -p "Do you want to install? (yes/no) " yn
#Ask for permission
case $yn in 
	yes ) echo ok, we will proceed;;
	no ) echo exiting...;
		exit;;
	* ) echo invalid response;
		exit 1;;
esac
echo Installing...
sudo cp ./dgraph /usr/bin
sudo cp ./mgraph /usr/bin
sudo cp ./pmgraph /usr/bin
