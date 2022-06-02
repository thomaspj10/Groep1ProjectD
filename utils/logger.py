import time
import logging

logging.basicConfig(filename=".log", filemode="a", format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")

def __execute(logging_method: callable):
    def logger(activity:str, information:str):
        current_unix = time.time()
        logging_method(
            "{time}\t{activity}\t{info}".format(
                time=current_unix,
                activity=activity,
                info=information
            )
        )
    
    return logger
        
def info(activity:str, information:str):
    __execute(logging.info)(activity, information)
    
def warning(activity:str, information:str):
    __execute(logging.warning)(activity, information)
    
def error(activity:str, information:str):
    __execute(logging.error)(activity, information)
    
def critical(activity:str, information:str):
    __execute(logging.critical)(activity, information)

def debug(activity:str, information:str):
    __execute(logging.debug)(activity, information)
    