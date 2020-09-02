import logging
import re
from itertools import groupby


def createLogger(name, lvl=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(lvl)
    ch = logging.StreamHandler()
    ch.setLevel(lvl)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
