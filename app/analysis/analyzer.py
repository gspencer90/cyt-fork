import time
import database.db_manager as d
from logging.logger import Logger

class Analyzer:
    def __init__(self, logger: Logger, event_threshold: int) -> None:
        self.logger = logger
        self.event_threshold = event_threshold
        self.logger.log('Getting ignore list...')
        self.wifi_probes = {}
        self.wifi_broadcasts = {}
        self.alerts = []

    def process_events(self, wifi_events: list, probe_events: list) -> None:
        self.process_wifi_events(wifi_events=wifi_events)
        self.process_probe_events(probe_events=probe_events)
        self.alert()

    def process_wifi_events(self, wifi_events: list) -> None:
        self.logger.log('----WiFi Events----')
        for mac, device_type in wifi_events:
            match = self.wifi_broadcasts.get(mac)
            if match == None:
                self.wifi_broadcasts[mac] = {
                    'events': [],
                    'device_type': device_type
                }
            events = self.wifi_broadcasts[mac]['events']
            timestamp = self.get_timestamp()
            events.append(timestamp)
            log = f'{device_type} {mac} detected'
            self.logger.log(log)
            if len(events) > self.event_threshold:
                self.logger.log(f'{log} {len(events)} times - alerting...')
                self.alerts.append((mac, device_type))

    def process_probe_events(self, probe_events: list) -> None:
        self.logger.log('----Probe Events----')
        for mac, ssid in probe_events:
            match = self.wifi_probes.get(mac)
            if match is None:
                self.wifi_probes[mac] = {
                    'events': [],
                    'ssid_probe': ssid
                }
            events = self.wifi_probes[mac]['events']
            timestamp = self.get_timestamp()
            events.append(timestamp)
            log = f'{mac} probed for SSID {ssid}'
            self.logger.log(log)
            if len(events) > self.event_threshold:
                self.logger.log(f'{log} {len(events)} time - alerting...')
                self.alerts.append((mac, ssid))

    def alert(self) -> None:
        for mac, type in self.alerts:
            alert = f'ALERT: {mac}/{type}'
            self.logger.log(alert)
            print(alert)

    def get_timestamp(self):
        return time.strftime('%d%m%YT%H:%M')
