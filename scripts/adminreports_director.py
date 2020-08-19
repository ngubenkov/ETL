import os
import logging
import re
import sys
import threading
import time


DATA_DATE = 'DATA_DATE'
TOKEN = 'TOKEN'
PASSWORD = 'PASSWORD'
BILLING_DIRECTOR_FREQID_TO_RUN = 'BILLING_DIRECTOR_FREQID_TO_RUN'

LOGGER = logging.getLogger()


def main():
    os.environ[DATA_DATE] = '15-AUG-20'
    """
    Get all possible freqs or get user given freq 
    """
    freqQuery = ''' 
    SELECT a.CODE, a.USERNAME, a.ENC_PASSWORD, df.ID, df.NAME,
    df.DEFS, df.SAFETIME, df.SAFEDAY, r.NAME, r.GENERATESCRIPTCLI

    FROM ADMINREPORTS.DATASOURCEFREQ df
    JOIN ADMINREPORTS.REPORTS r on df.REPORTID = r.ID
    JOIN ADMINREPORTS.ADMINS a on a.ID = df.ADMINID
    where (df.ISACTIVE = 1 and
          r.ISACTIVE = 1 and
           :1 is null) or
          (df.id = :2)
        order by df.id;
        '''

    try:
        freqIdToRun = os.environ.get(BILLING_DIRECTOR_FREQID_TO_RUN)


    finally:
        """ 
        wait for all threads to finish. When all subprocess have finished
        """
        LOGGER.info("Now joining each launched thread so that the main thread"
                    "waits on all of them.")


if __name__ == '__main__':
    main()
