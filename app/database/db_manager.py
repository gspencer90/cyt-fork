import os
import sqlite3
import json
import glob
import time
from datetime import datetime, timedelta
from logging.logger import Logger

class DBManager:
   def __init__(self, logger: Logger, base_path: str, poll_period: float) -> None:
      self.logger = logger
      self.config_path = f'{base_path}/config.json'
      self.db_base_path = f'{base_path}/logs'
      self.poll_period = poll_period
      self.probe_ignore_list = self.get_ignore_list()
      self.db_file = self.get_db_file()
      log = f'Reading from {self.db_file}'
      self.logger.log(log)

   def get_database_connection(self) -> sqlite3.Cursor:
      latest_file = self.db_file
      connection = sqlite3.connect(latest_file)
      return connection.cursor()

   def query(self):
      time_delta = datetime.now() + timedelta(minutes=-self.poll_period)
      unix_time = time.mktime(time_delta.timetuple())
      query = f'SELECT devmac, type, device FROM devices WHERE last_time >= {unix_time}'

      cursor = self.get_database_connection()
      cursor.execute(query)
      rows = cursor.fetchall()

      wifi_events = []
      probe_events = []
      
      for row in rows:
         raw_device_json = json.loads(str(row[2], errors='ignore'))
         if 'dot11.probedssid.ssid' in str(row):
            ssid_probed_for = raw_device_json['dot11.device']['dot11.device.last_probed_ssid_record']['dot11.probedssid.ssid']
            if ssid_probed_for == '' or self.probe_ignore_list.get(ssid_probed_for) is not None:
               if self.probe_ignore_list.get(ssid_probed_for) is not None:
                  self.logger.log(f'{ssid_probed_for} in ignore list, skipping...')
            else:
               probe_events.append((str(row[0]), ssid_probed_for))
         else:
            wifi_events.append((row[0], row[1]))
      self.logger.log(f'Found {len(wifi_events)} WiFi events and {len(probe_events)} probe events')
      return {
         'wifi_events': wifi_events,
         'probe_events': probe_events
      }

   def get_ignore_list(self) -> dict:
      probe_ignore_list = {}
      with open(self.config_path, 'r', encoding='utf-8') as config_file:
         config_contents = config_file.read()

      config = json.loads(config_contents)
      for ssid in config['ssidIgnoreList']:
         probe_ignore_list[ssid] = True

      return probe_ignore_list

   def get_db_file(self) -> str:
      db_path = f'{self.db_base_path}/*.kismet'
      list_of_files = glob.glob(db_path)
      latest_file = max(list_of_files, key=os.path.getctime)
      return latest_file
