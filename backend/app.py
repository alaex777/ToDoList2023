import sys
from uuid import uuid4

from fastapi import FastAPI

sys.path.append('../database')

from models import Record
from services import postgres_error_wrapper

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

@postgres_error_wrapper
@app.get('/get/tasks', status_code=200)
async def tasks_list():
    res = PostgresConnection(CONNECTION_PARAMS).run_cmd('SELECT * FROM %s;' % (TASKS_TABLE))
    if len(res) == 0:
        res = ''
    return {'message': res}

@postgres_error_wrapper
@app.post('/create/task', status_code=200)
async def create_task(record: Record):
    conn = PostgresConnection(CONNECTION_PARAMS)
    ids = conn.run_cmd('SELECT task_id FROM %s;' % (TASKS_TABLE))
    uid = uuid4()
    while uid in ids:
        uid = uuid4()
    conn.run_cmd(
        'INSERT INTO %s VALUES (\'%s\', \'%s\');' % 
        (TASKS_TABLE, str(uid), record.content)
    )
    return {'message': 'ok'}

@postgres_error_wrapper
@app.delete('/delete/task/{id}', status_code=200)
async def delete_task(id: str):
    PostgresConnection(CONNECTION_PARAMS).run_cmd(
        'DELETE FROM %s WHERE task_id = \'%s\';' % (TASKS_TABLE, id)
    )
    return {'message': 'ok'}

@postgres_error_wrapper
@app.put('/update/task/{id}', status_code=200)
async def update_task(id: str, record: Record):
    PostgresConnection(CONNECTION_PARAMS).run_cmd(
        'UPDATE %s SET content = \'%s\' WHERE task_id = \'%s\';' % 
        (TASKS_TABLE, record.content, id)
    )
    return {'message': 'ok'}
