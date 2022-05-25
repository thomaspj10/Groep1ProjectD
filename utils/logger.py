from datetime import datetime
from utils.singleton import Singleton

class Logger(metaclass=Singleton):
    def Write(self, event:str):
        with open("../.log", "a") as f:
            current_datetime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            f.write(f"{current_datetime}\t{event}\n")