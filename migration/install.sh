#!/bin/bash
cwd=$(pwd)
sudo pip install numpy==1.11.2
sudo pip install scipy==0.18.1
sudo pip install sklearn==0.18
sudo pip install pandas==0.19.1
sudo pip install matplotlib==1.5.3
sudo pip install haversine==0.4.5
sudo pip install xlrd==1.0.0
sudo pip install statsmodels==0.6.1
sudo pip install networkx==1.11
# install the python module community separately
# this module is installed by python
mkdir ./downloads
cd ./downloads
python ./../code/RetrievePackages.py
cd ./python-louvain-0.3
python setup.py install
cd $cwd
read  -p "Installation done. Press enter to continue" dummy
