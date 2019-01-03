#!/bin/bash

cd ~
cd /media/pi/D220-8D3B1/SIOT
git pull origin master
git status
git add data-storage/usb/data_log_combined.csv
git commit -m "Routine data upload"
git push origin master
git status
