import sys

sys.path.append('../database')

from db_connection import PostgresConnection
from connection_params import CONNECTION_PARAMS, TASKS_TABLE


def main():
    PostgresConnection(CONNECTION_PARAMS).run_cmd(
        'DROP TABLE %s;' % (TASKS_TABLE)
    )

if __name__ == '__main__':
    main()
