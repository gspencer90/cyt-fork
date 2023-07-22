#!/bin/bash

YELLOW='\033[33m'
GREEN='\033[32m'
NO_COLOR='\033[0m'

# TO-DO: BREAK ECHO STATEMENTS TO LOG FN
echo -e "${YELLOW}Initializing app...${NO_COLOR}"

# Update Linux
echo -e "${YELLOW}Updating OS...${NO_COLOR}"
sudo apt-get update
sudo apt-get upgrade
echo -e "${GREEN}OS updated successfully${NO_COLOR}"

# Install Kismet
echo -e "${YELLOW}Installing Kismet...${NO_COLOR}"
wget -O - https://www.kismetwireless.net/repos/kismet-release.gpg.key | sudo apt-key add -
echo "deb https://www.kismetwireless.net/repos/apt/release/$(lsb_release -cs) $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/kismet.list
sudo apt-get update
sudo apt-get install kismet
echo -e "${GREEN}Kismet installed successfully${NO_COLOR}"

# Add sources to Kismet config file
echo -e "${YELLOW}Adding source adapters to Kismet config file...${NO_COLOR}"
#TO-DO: ALLOW USER TO SPECIFY SOURCE
echo -e "source=wlan0\nsource=wlan1\nsource=hci0\n" | sudo tee -a /etc/kismet/kismet_site.conf
echo -e "${GREEN}Sources added successfully${NO_COLOR}"

# Create Kismet logging directory
echo -e "${YELLOW}Creating logs directory...${NO_COLOR}"
mkdir /home/$USER/kismet_logs
echo -e "${GREEN}Logs directory created successfully${NO_COLOR}"

# Add current user to the Kismet group
echo -e "${YELLOW}Adding user '$USER' to Kismet group...${NO_COLOR}"
sudo usermod -aG kismet $USER
su - $USER
echo -e "${GREEN}User '$USER' added successfully, rebooting...${NO_COLOR}"
sleep 5
sudo reboot