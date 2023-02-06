import sys
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from psycopg2 import OperationalError

sys.path.append('../database')

from models import Record

from connection_params import CONNECTION_PARAMS, TASKS_TABLE
from db_connection import PostgresConnection

app = FastAPI()


@app.get('/')
async def list():
    return {
        '/get/tasks': 'Get all tasks',
        '/create/task': 'Create task with content',
        '/delete/task/{id}': 'Delete task with id',
        '/update/task/{id}': 'Update task with id'
    }

@app.get('/get/tasks', status_code=200)
async def tasks_list():
    conn = PostgresConnection(CONNECTION_PARAMS)
    try:
        res = conn.run_cmd('SELECT * FROM %s;' % (TASKS_TABLE))
        if len(res) == 0:
            res = ''
        return {'message': res}
    except OperationalError:
        return HTTPException(status_code=503, detail='Error connection to database')
    except:
        return HTTPException(status_code=500, detail='Unknown exception')

@app.post('/create/task', status_code=200)
async def create_task(record: Record):
    conn = PostgresConnection(CONNECTION_PARAMS)
    try:
        ids = conn.run_cmd('SELECT task_id FROM %s;' % (TASKS_TABLE))
        uid = uuid4()
        while uid in ids:
            uid = uuid4()
        conn.run_cmd(
            'INSERT INTO %s VALUES (\'%s\', \'%s\');' % 
            (TASKS_TABLE, str(uid), record.content)
        )
        return {'message': 'ok'}
    except OperationalError:
        return HTTPException(status_code=503, detail='Error connection to database')
    except:
        return HTTPException(status_code=500, detail='Unknown exception')

@app.delete('/delete/task/{id}', status_code=200)
async def delete_task(id: str):
    conn = PostgresConnection(CONNECTION_PARAMS)
    try:
        conn.run_cmd('DELETE FROM %s WHERE task_id = \'%s\';' % (TASKS_TABLE, id))
        return {'message': 'ok'}
    except OperationalError:
        return HTTPException(status_code=503, detail='Error connection to database')
    except:
        return HTTPException(status_code=500, detail='Unknown exception')

@app.put('/update/task/{id}', status_code=200)
async def update_task(id: str, record: Record):
    conn = PostgresConnection(CONNECTION_PARAMS)
    try:
        conn.run_cmd(
            'UPDATE %s SET content = \'%s\' WHERE task_id = \'%s\';' % 
            (TASKS_TABLE, record.content, id)
        )
        return {'message': 'ok'}
    except OperationalError:
        return HTTPException(status_code=503, detail='Error connection to database')
    except:
        return HTTPException(status_code=500, detail='Unknown exception')
