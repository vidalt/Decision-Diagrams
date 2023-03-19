import logging

class DashLoggerHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)
        self.queue = []

    def emit(self, record):
        msg = f'{record.pathname.split("/")[-1]}[{record.lineno}] {record.msg}'
        self.queue.append(msg)