import pytest 
import sys

sys.path.append('../database')

from db_utils.create_tables import main as create
from db_utils.delete_tables import main as delete
from connection_params import CONNECTION_PARAMS, TEST_TABLE
from db_connection import PostgresConnection


@pytest.fixture
def pg_connection():
    try:
        delete(TEST_TABLE)
    except:
        pass
    create(TEST_TABLE)
    return PostgresConnection(CONNECTION_PARAMS)
