#This file is if you want to build it yourself. This script MUST be run with sudo
sudo apt install python3
sudo apt install python3-pip
#Installing required outer packages
pip3 install pyinstaller
#Installing pyinstaller compiler
pyinstaller --onefile dgraph.py
#Compiling code
cp ./dist/dgraph .
#Copying binary out
rm -rf build
rm -rf dist
#Cleaning up
