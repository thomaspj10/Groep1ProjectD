from utils.singleton import Singleton
class Logger(metaclass=Singleton):
    def log(self, event:str):
        print(event)