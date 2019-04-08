#!/bin/bash

par=$1
parName=Trig_Lat

scan_Type=$2

Yarr_DIR=/home/yamagaya/Desktop/Yarr-sw/LatestYarr2/src/
tool_DIR=/home/yamagaya/Desktop/diff_plot/

python src/edit_json.py $parName $par $scan_Type

cd $Yarr_DIR
./doScan.sh -m KEK101 -s ${scan_Type} -j

echo $before_par
cd $tool_DIR
#python src/edit_json.py $parName $before_par $scan_Type
