# Chasing Your Tail Remix

## Requirements
- Python 3.9+
- Kismet

## Quickstart
1. Install Kismet and Python if not already installed - `sudo apt-get`
2. Run `cyt-fork/scripts/setup.sh` - `./scripts/setup.sh`
3. Activate a virtual environment - `python3 -m venv .venv && souce .venv/bin/activate`
4. Open two terminals. In one run Kismet, ensuring that it outputs logs to `cyt-fork/logs`. In the second terminal, run the CYT app - `python app/main.py`

## Device Types to Monitor (possibly)
- Probing Devices (AutogroupProbe)
- SSIDs (WiFi Wireless Access Points)
- BlueTooth
- IoT (OBD, wearables, headphones, etc.)