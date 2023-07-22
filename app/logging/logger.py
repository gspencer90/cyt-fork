import time

class Logger:
   def __init__(self, base_path: str) -> None:
      self.logs = []
      self.base_path = base_path
      self.timestamp = self.get_timestamp()

   def log(self, log_statement: str) -> None:
      timestamp = self.get_timestamp(full_timestamp=False)
      self.logs.append(f'{timestamp}: {log_statement}')

   def write_logs(self) -> None:
      log_file_name = f'cyt_log_{self.timestamp}'
      log_path = f'{self.base_path}/logs/{log_file_name}'
      with open(log_path, 'w') as log_file:
         for log in self.logs:
            log_file.write(f'{log}\n')

   def get_timestamp(self, full_timestamp = True) -> str:
      return time.strftime('%d%m%YT%H:%M') if full_timestamp is True else time.strftime('%H:%M')
