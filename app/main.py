import subprocess
import os
import json
import time
from pathlib import Path
from analysis.analyzer import Analyzer
from database.db_manager import DBManager
from logging.logger import Logger

base_path = Path(__name__).parent.absolute()
output_file = 'results.json'
# TO-DO: Refactor this to config along with ignore list
timeout = 2
event_threshold = 3

def main() -> None:
      print('Initializing...')
      logger = Logger(base_path=base_path)
      print('Starting Chasing Your Tail...')
      db = DBManager(logger=logger, base_path=base_path, poll_period=timeout)
      analyzer = Analyzer(logger=logger, event_threshold=event_threshold)
      try:
            while True:
                  logger.log('Starting scan...')
                  events = db.query()
                  
                  wifi_events = events['wifi_events']
                  probe_events = events['probe_events']

                  analyzer.process_events(wifi_events=wifi_events, probe_events=probe_events)
                  time.sleep(timeout * 60)
      except KeyboardInterrupt:
            pass
      finally:
            logger.log('Application quitting...')
            print('Finalizing...')
            with open(output_file, 'w') as file:
                  data = {
                  'ssidProbes': analyzer.wifi_probes,
                  'wifiClients': analyzer.wifi_broadcasts
                  }
                  file.write(json.dumps(data, indent=4))
            logger.write_logs()

def verify_monitor_mode() -> None:
      dir_path = os.path.dirname(os.path.realpath(__file__))
      path = f'{dir_path}/config/monitor.sh'
      output = subprocess.call([path])
      print(output)

def initialize() -> None:
   verify_monitor_mode()

if __name__ == '__main__':
    main()
