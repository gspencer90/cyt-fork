#!/bin/bash
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # no color
numprocesses=$(ps aux | grep -i 'kismet' | wc -l)
if [[ $numprocesses > 2 ]] ; then 
		echo -e "${GREEN}Kismet up${NC}"
	else
		echo -e "${RED}Kismet down${NC}"
fi

string=$(iwconfig wlan1mon)
if [[ $string == *"Mode:Monitor"* ]]; then
	echo -e "${GREEN}Monitor Mode Detected${NC}"
else
	echo -e "${RED}Monitor Mode Not Detected${NC}"
fi 
echo
sleep 10;
