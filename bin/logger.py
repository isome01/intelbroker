import os
from tools import format_time_stamp


class Logger:
    """This class is used simply
    to log to files."""

    def __init__(self, **kwds):
        self.id = kwds.get('id', os.getpid())
        self.logger_name = f'{kwds.get("logger_name", "Logger")}-{self.id}'
        self.log_path = kwds.get('log_path', os.getcwd())
        self.returning_log = True
        self.time_format = '%m/%d/%Y %H:%M:%S'
        self.log_file = None
        try:
            if not os.path.exists(self.log_path):
                os.mkdir(self.log_path)
                self.returning_log = False

            self.log_file = open(
                f'{self.log_path}/{self.logger_name}.log',
                'a' if self.returning_log else 'w'
            )
        except Exception as e:
            print(f'Error: {e}\n')

    def __call__(self, *args):
        self._log(args[0])

    def __del__(self):
        if self.log_file:
            self.log_file.close()

    def _log(self, text=''):
        if self.log_file is None:
            pass
        elif not self.log_file.closed:
            if len(text) < 1:
                text = '(default): logging successful'

            # configure date and time
            self.log_file.write(f'{format_time_stamp()} - {text}\n')
        else:
            print(f'Error from {self.logger_name}: log file is closed.')

