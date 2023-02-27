import sys
import os
import logging
from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.append('../database')

from models import Record
from services import postgres_error_wrapper

from connection_params import CONNECTION_PARAMS, TASKS_TABLE, TEST_TABLE
from db_connection import PostgresConnection

app = FastAPI()

TEST_MODE = os.getenv('RUN_MODE', default='work')
if TEST_MODE == 'work':
    WORK_TABLE = TASKS_TABLE
else:
    WORK_TABLE = TEST_TABLE

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s %(levelname)s %(message)s',
    filename='logs/logs.log',
    filemode='w'
)

@app.get('/')
async def list():
    logging.info('base path called')
    return {
        '/get/tasks': 'Get all tasks',
        '/create/task': 'Create task with content',
        '/delete/task/{id}': 'Delete task with id',
        '/update/task/{id}': 'Update task with id'
    }

@postgres_error_wrapper
@app.get('/get/tasks', status_code=200)
async def tasks_list():
    logging.info('get tasks path called')
    res = PostgresConnection(CONNECTION_PARAMS).run_cmd(
        'SELECT * FROM %s;' % (WORK_TABLE)
    )
    if len(res) == 0:
        res = []
    logging.info('get tasks worked fine')
    return {'message': res}

@postgres_error_wrapper
@app.post('/create/task', status_code=200)
async def create_task(record: Record):
    print(record)
    logging.info('create task path called')
    PostgresConnection(CONNECTION_PARAMS).run_cmd(
        'INSERT INTO %s VALUES (\'%s\', \'%s\', \'%s\', \'%s\');' % 
        (WORK_TABLE, str(uuid4()), record.content, record.due_date, record.type.value)
    )
    logging.info('create task worked fine')
    return {'message': 'ok'}

@postgres_error_wrapper
@app.delete('/delete/task/{id}', status_code=200)
async def delete_task(id: str):
    logging.info('delete task path called')
    PostgresConnection(CONNECTION_PARAMS).run_cmd(
        'DELETE FROM %s WHERE task_id = \'%s\';' % (WORK_TABLE, id)
    )
    logging.info('delete task worked fine')
    return {'message': 'ok'}

@postgres_error_wrapper
@app.put('/update/task/{id}', status_code=200)
async def update_task(id: str, record: Record):
    logging.info('update task path called')
    PostgresConnection(CONNECTION_PARAMS).run_cmd(
        'UPDATE %s SET content = \'%s\' WHERE task_id = \'%s\';' % 
        (WORK_TABLE, record.content, id)
    )
    logging.info('update task worked fine')
    return {'message': 'ok'}
