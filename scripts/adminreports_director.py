import os
import logging
import re
import sys
import threading
import time
import datetime
from utillib.connections import get_etl_conn
from utillib.genlib import *

DATA_DATE = 'DATA_DATE'
TOKEN = 'TOKEN'
PASSWORD = 'PASSWORD'
BILLING_DIRECTOR_FREQID_TO_RUN = 'BILLING_DIRECTOR_FREQID_TO_RUN'

LOGGER = logging.getLogger()

def lockFreqid(conn, freqid):
    """
        This will lock freqid with FOR UPDATE NOWAIT so no more than
        two same freqid will be run at same time
    """
    sql = '''
            SELECT * FROM ADMINREPORTS.DATASOURCEFREQ
            WHERE ID = :1 FOR UPDATE
            '''
    conn.execute(sql, [freqid])
    LOGGER.info("Successfully locked DATASOURCEFREQ record with id: %s",freqid)



def main():
    os.environ[DATA_DATE] = '15-AUG-20'
    """
    Get all possible freqs or get user given freq 
    """

    currentDateTime = datetime.datetime.now()
    logicalHours = currentDateTime.hour
    logicalMinutes = currentDateTime.min

    LOGGER.info('currentDateTime: %s', currentDateTime)
    LOGGER.info('logicalHours: %s', logicalHours)
    LOGGER.info('logicalMinutes: %s', logicalMinutes)

    logical
    processesLaunched = 0

    freqQuery = ''' 
    SELECT a.CODE, a.USERNAME, a.ENC_PASSWORD, df.ID, df.FREQ, df.NAME,
    df.DEFS, df.SAFETIME, df.SAFEDAY, r.NAME, r.GENERATESCRIPTCLI, r.FILESUFFIX, r.MAXTRIES

    FROM ADMINREPORTS.DATASOURCEFREQ df
    JOIN ADMINREPORTS.REPORTS r on df.REPORTID = r.ID
    JOIN ADMINREPORTS.ADMINS a on a.ID = df.ADMINID
    where (df.ISACTIVE = 1 and
          r.ISACTIVE = 1 and
           1 is null) or
          (df.id = 1)
        order by df.id;
        '''

    try:
        freqIdToRun = os.environ.get(BILLING_DIRECTOR_FREQID_TO_RUN)
        LOGGER.info("Received BILLING_DIRECTOR_FREQID_TO_RUN: %s", freqIdToRun)

        with get_etl_conn() as adminreports_conn:
            reader = adminreports_conn.execute(freqQuery, [freqIdToRun], [freqIdToRun])

            for reader_row in reader:
                try:
                    """ 
                    Get info about freq
                    """

                    LOGGER.info('Now handling reader_row: %s', reader_row)
                    freqid = reader_row[3]
                    freq = reader_row[4]
                    dsname = reader_row[1]
                    soCode = reader_row[9]
                    soUsername = reader_row[1]
                    soEncPassword = reader_row[2]
                    safeTime = reader_row[7]
                    safeDay = reader_row[8]
                    fileSuffix = reader_row[11]
                    frname = reader_row[5]
                    maxTries = reader_row[12]
                    generateScriptCLI = reader_row[10]
                    sourceOut = reader_row[9]

                    # Lock freq
                    frequnid_sql = '''SELECT MAX(ID)+1 FROM ADMINREPORTS.DATASOURCERUNS'''

                    freqRunID = adminreports_conn.execute(frequnid_sql).fetchone()[0]

                    LOGGER.info('freq: %s', freq)
                    LOGGER.info('freqRunId: %s', freqRunID)
                    LOGGER.info('Handling freqid: %s, soCode: %s', freqid, soCode)

                    lockFreqid(adminreports_conn, freqid)

                    LOGGER.info('Director is processing freqid: %s', freqid)
                    prog_date = datetime.date.today()


                    if freq == 'D':
                        dataDate = trunc(datetime.datetime.now())

                    elif freq == 'M':
                        if datetime.datetime.now().month == 12: # if current month is JAN, so run for DEC prev year
                            dataDate = datetime.date(datetime.datetime.now().year - 1 ,
                                                     datetime.datetime.month - 1 or 12,
                                                     1)

                        else:
                            dataDate = datetime.date(datetime.datetime.now().year,
                                                     datetime.datetime.month - 1 or 12,
                                                     1)
                    else:
                        raise Exception("Unsupported freq: %s",freqid)

                LOGGER.info('Processed dataDate: %', dataDate)

    



    finally:
        """ 
        wait for all threads to finish. When all subprocess have finished
        """
        LOGGER.info("Now joining each launched thread so that the main thread"
                    "waits on all of them.")


if __name__ == '__main__':
    main()
