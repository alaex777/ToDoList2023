import pytest
import requests
import sys

sys.path.append('../database')

from connection_params import TASKS_TABLE


HOST = 'http://localhost:8000'

def test_api_positive(pg_connection):
    conn = pg_connection

    req = requests.get(HOST + '/get/tasks')
    assert req.status_code == 200
    assert req.json() == {'message': ''}

    req = requests.post(HOST + '/create/task', json={'content': 'test1'})
    assert req.status_code == 200

    res = conn.run_cmd('SELECT content FROM %s' % (TASKS_TABLE))
    assert len(res) == 1
    assert res[0][0] == 'test1'

    res = conn.run_cmd('SELECT task_id FROM %s' % (TASKS_TABLE))
    task_id = res[0][0]
    print(task_id)

    req = requests.get(HOST + '/get/tasks')
    assert req.status_code == 200
    assert req.json() == {'message': [[task_id, 'test1']]}

    req = requests.put(HOST + f'/update/task/{task_id}', json={'content': 'test2'})
    assert req.status_code == 200

    res = conn.run_cmd('SELECT content FROM %s' % (TASKS_TABLE))
    assert len(res) == 1
    assert res[0][0] == 'test2'

    req = requests.delete(HOST + f'/delete/task/{task_id}')
    assert req.status_code == 200

    res = conn.run_cmd('SELECT content FROM %s' % (TASKS_TABLE))
    assert len(res) == 0
