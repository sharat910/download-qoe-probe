import os
import logging 
import random
from datetime import datetime


def create_logger(name,tag):
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger("%s-%d" % (name,random.randint(0,100)))
    logger.setLevel(logging.INFO)
 
    # create the logging file handler
    os.makedirs("logs/%s"%tag,exist_ok=True)

    fh = logging.FileHandler("logs/%s/%s-%s.log" % (tag,name, str(datetime.now())))
 
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    # create the logging stderr handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)
 
    # add handler to logger object
    logger.addHandler(fh)
    return logger