import database_common
from psycopg2 import sql


def normalize_output_single_row(normalize_me):  # Creates a simple dictionary
    dump_dictionary = {}
    for row in normalize_me:
        for key, value in row.items():
            dump_dictionary[key] = value
    return dump_dictionary


def normalize_output_multiple_rows(normalize_me):  # Creates dictionaries in a list
    normalized_output = []
    for row in normalize_me:
        dump_dictionary = {}
        for key, value in row.items():
            dump_dictionary[key] = value
        normalized_output.append(dump_dictionary)
    return normalized_output


@database_common.connection_handler
def add_user(cursor, user_data):
    username = user_data['username']
    password = user_data['password']
    cursor.execute(sql.SQL("""
                            INSERT INTO users (username, password)
                            VALUES ('{username}', '{password}')
                            """).format(username=sql.SQL(username), password=sql.SQL(password)))


@database_common.connection_handler
def get_usernames(cursor):
    cursor.execute("""
                    SELECT username FROM users
                    """)
    return [dict_['username'] for dict_ in normalize_output_multiple_rows(cursor.fetchall())]


@database_common.connection_handler
def get_a_pass(cursor, username):
    cursor.execute(sql.SQL("""
                            SELECT password FROM users
                            WHERE username = '{username}'
                            """).format(username=sql.SQL(username)))
    return normalize_output_single_row(cursor.fetchall())['password']


@database_common.connection_handler
def get_user_id(cursor, username):
    cursor.execute("""
                    SELECT id FROM users
                    WHERE username = '{username}'
                    """).format(username=username)

