from fastapi import HTTPException
from psycopg2 import OperationalError


def postgres_error_wrapper(func):
    async def inner():
        try:
            return await func()
        except OperationalError:
            return HTTPException(status_code=503, detail='Error connection to database')
        except:
            return HTTPException(status_code=500, detail='Unknown exception')
    return inner
