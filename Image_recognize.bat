#!/bin/bash
#  
echo '---------make photo file path-------------'
picdir = '/home/pi/original_pic/'
#time
datecode=`date '+%Y_%m_%d_%H_%M_%S'`
headercode="log_"
endcode=".png"
picname=$headercode$datecode$endcode
#echo $datecode'.png'
picname=$picname$picname
echo $'picture path is ...'$picname
echo '-------------taking picture--------------------'
libcamera-still -e png --width 960 --height 720 -0 $picname
echo 'Recognizing set-point temperture'
/usr/bin/python3 /home/pi/detect.py
/home/pi/ --save-txt --save-conf --project
/home/pi/result
echo 'Date transimission & Delete raw picture'
# Data tranmissition by MQTT protocol
/usr/bin/python3 /home/pi/publish_camera.py
# Delete raw picture 
/usr/bin/python3 /home/pi/delete.py
