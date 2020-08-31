from psycopg2 import connect, OperationalError
from yaml import load, Loader

from setup import POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER


class SpotifyDB:
    def __init__(self, db_conf_file):
        with open(db_conf_file, 'r') as cfg_file:
            cfg_data = load(cfg_file, Loader=Loader)

        self.tables_cfg = cfg_data['db']['tables']

        self.connection = connect(
            dbname = cfg_data['db']['name'],
            user = cfg_data['db']['user'],
            host = cfg_data['db']['host'],
            password = cfg_data['db']['pass']
        )
        self.cursor = self.connection.cursor()
        self._set_up_db()
        self.sql_query = SQLQuery()

    def __del__(self):
        self.connection.close()
        self.cursor.close()

    def _set_up_db(self):
        for t in self.tables_cfg:
            fields = ', '.join([f"{x['name']} {x['type']}"  for x in self.tables_cfg[t]])
            self.cursor.execute(
                f'CREATE TABLE {t} ({fields});'
            )

    def is_connected(self):
        print(self.connection.status)
        return True if self.connection.closed > 0 else False

    def insert(self, table, data):
        assert isinstance(data, dict)
        self.cursor.execute(
            f"INSERT INTO {table} ({', '.join(list(data.keys()))}) VALUES ({', '.join(list(data.values()))})"
        )

    # def get(self, table, data):
    #     assert isinstance(data, dict)
    #     self.cursor.execute(
    #         f"SELECT "
    #     )


# f = SQLQuery()
# print(f.insert('album', name='All the days', artist='Sain Ti').commit())
# print(f.select('*', 'movies').where('imdb_rating > 0').commit())

sb = SpotifyDB('config.yml')
# sb.
# sb.insert('user', {'id': '11111', 'secret': 'FFFFF'})


# # declare a cursor object from the connection
# cursor = conn.cursor()

# # execute an SQL statement using the psycopg2 cursor object
# cursor.execute(f"SELECT * FROM {table_name};")

# # enumerate() over the PostgreSQL records
# for i, record in enumerate(sb.db_cursor):
#     print ("\n", type(record))
#     print ( record )

# # close the cursor object to avoid memory leaks
# cursor.close()

# # close the connection as well
# conn.close()