import sys

sys.path.append('../database')

from db_connection import PostgresConnection
from connection_params import CONNECTION_PARAMS, TASKS_TABLE


def main(table_name=TASKS_TABLE):
    PostgresConnection(CONNECTION_PARAMS).run_cmd(
        'DROP TABLE %s;' % (table_name)
    )

if __name__ == '__main__':
    main()
