#!/bin/bash

echo '---------make photo file path-------------'
picdir='/home/pi/original_pic/'

#time
datecode=`date '+%Y_%m_%d_%H_%M_%S'`
headercode="log_"
endcode=".jpg"  # raspistill 
picname=$headercode$datecode$endcode
picname=$picdir$picname
echo $'picture path is ...'$picname

echo '-------------taking picture--------------------'
raspistill -w 960 -h 720 -o $picname

echo 'Recognizing set-point temperature and send data to mqtt server'
/usr/bin/python3 /home/pi/IR.py

echo 'Delete raw picture'
# Delete raw picture 
/usr/bin/python3 /home/pi/delete.py
