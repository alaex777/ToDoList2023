import os
import json

from db_connection import DBConnectionParameters


config_file = open(os.path.join(
    os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 
    '.config', 
    'db_params.json'))

config = json.load(config_file)

CONNECTION_PARAMS = DBConnectionParameters(
    dbname=config['db_connection']['db_name'],
    user=config['db_connection']['user'],
    password=config['db_connection']['password'],
    host=config['db_connection']['host'],
    port=config['db_connection']['port']
)

TASKS_TABLE = config['tasks_table']

config_file.close()
