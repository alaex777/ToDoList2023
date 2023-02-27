import logging

from fastapi import HTTPException
from psycopg2 import OperationalError


def postgres_error_wrapper(func):
    async def inner():
        try:
            return await func()
        except OperationalError:
            logging.error('error connection to database')
            return HTTPException(status_code=503, detail='Error connection to database')
        except Exception as exp:
            logging.error('some unknown service error %s' % (str(exp)))
            return HTTPException(status_code=500, detail='Unknown exception')
    return inner
