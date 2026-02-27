import logging
import os

class Logger:
    def __init__(self):
        self.log_dir = "./Logs"
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)
        self.setup_logs()

    def setup_logs(self):
        log_file_path = os.path.join(self.log_dir,"log.log")
        logging.basicConfig(
                    filename = log_file_path,
                    filemode="a",
                    level = logging.INFO,
                    format = "%(asctime)s:%(name)s:%(levelname)s:%(message)s", 
                    datefmt = "%d/%m/%Y %I:%M:%S %p")
        return logging.getLogger("RetailApp")