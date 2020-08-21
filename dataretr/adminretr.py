import os
import sys
import logging
from utillib.util import *

LOGGER = logging.getLogger()


if __name__ == '__main__':

    LOGGER.debug("Received sys.argv : %s", sys.argv)

    """ Get arguments from adminreports_director saved in os"""
    FREQID =  os.environ['FREQID']
    DSR_ID = os.environ['DSR_ID']
    PHASE = os.environ['PHASE']

    DATARETR_RETRIEVED_PATH = get_conf_dict()['DATARETR_RETRIEVED_PATH']

    LOGGER.info('Received DATARETR_RETRIEVED_PATH: %s', DATARETR_RETRIEVED_PATH)
    LOGGER.info('Received PHASE: %s', PHASE)

    RETRIEVE_PATH = os.environ['RETRIEVE_PATH']
    LOGGER.info('Receieved RETRIEVE_PATH: %s', RETRIEVE_PATH)

    open_file = open
    mode = 'r'
    encoding = None
    errors = 'ignore'



