import requests
import sys

sys.path.append('../database')

from connection_params import TEST_TABLE

# export RUN_MODE=test
HOST = 'http://localhost:8000'

def test_api_positive(pg_connection):
    conn = pg_connection

    req = requests.get(HOST + '/get/tasks')
    assert req.status_code == 200
    assert req.json() == {'message': ''}

    req = requests.post(HOST + '/create/task', json={
        'content': 'test1',
        'due_date': '12/02/2002',
        'type': 'work'})
    assert req.status_code == 200

    res = conn.run_cmd('SELECT content, due_date, type FROM %s' % (TEST_TABLE))
    assert len(res) == 1
    assert res[0] == ('test1', '12/02/2002', 'work')

    res = conn.run_cmd('SELECT task_id FROM %s' % (TEST_TABLE))
    task_id = res[0][0]

    req = requests.get(HOST + '/get/tasks')
    assert req.status_code == 200
    assert req.json() == {'message': [[task_id, 'test1', '12/02/2002', 'work']]}

    req = requests.put(HOST + f'/update/task/{task_id}', json={
        'content': 'test2',
        'due_date': '12/02/2002',
        'type': 'work'
    })
    assert req.status_code == 200

    res = conn.run_cmd('SELECT content, due_date, type FROM %s' % (TEST_TABLE))
    assert len(res) == 1
    assert res[0] == ('test2', '12/02/2002', 'work')

    req = requests.delete(HOST + f'/delete/task/{task_id}')
    assert req.status_code == 200

    res = conn.run_cmd('SELECT content FROM %s' % (TEST_TABLE))
    assert len(res) == 0
