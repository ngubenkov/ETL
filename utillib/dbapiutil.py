import logging
import datetime
import uuid
import contextlib

logger = logging.getLogger(__name__)


class Connection:
    def __init__(self, dbapi_conn, startup_queries=None):
        self.dbapi_conn = dbapi_conn
        if startup_queries:
            for query in startup_queries:
                self.execute(query)


    def execute(self, sql, param = []):
        curson = self.dbapi_conn.cursor()
        requestId = uuid.uuid4().hex
        logger.debug("Starting execution of query (requestid: %s): %s , with parameters %s", requestId, sql, param)
        curson.execute(sql, param)
        logger.debug('Done query (requestid: %s) .', requestId)

        return curson

    def commit(self):
        return self.dbapi_conn.commit()

    def close(self):
        return self.dbapi_conn.close()

    def rollback(self):
        return self.dbapi_conn.rollback()

    def cursor(self):
        return self.dbapi_conn.cursor()


@contextlib.contextmanager
def connect(dbapi_conn_construct_callable, startup_queries):
    conn = None

    try:
        conn = Connection(dbapi_conn_construct_callable(),startup_queries)
        yield conn

    except Exception as e:
        if conn is not None:
            conn.rollback()
        raise e
    else:
        conn.commit()

    finally:
        if conn is not None:
            conn.close()