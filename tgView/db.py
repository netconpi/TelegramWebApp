
import sqlite3

import psycopg2
import psycopg2.extras

def postgree_fetch(requs_db: str):
    try:
        with psycopg2.connect(
                    host = 'localhost',
                    dbname = 'singup_db',
                    user = 'sing_main',
                    password = 'sing_mainPassword2022',
                    port = 5432) as conn:

            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(requs_db)
                result = cur.fetchall()
                return result
    except Exception as error:
        print(error)


def postgree_commit(requs_db: str):
    try:
        with psycopg2.connect(
                    host = 'localhost',
                    dbname = 'singup_db',
                    user = 'sing_main',
                    password = 'sing_mainPassword2022',
                    port = 5432) as conn:

            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(requs_db)
                cur.commit()
    except Exception as error:
        print(error)


def connect():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    return connection, cursor


def fetch(req):
    connection, cursor = connect()
    try:
        cursor.execute(req)
        res = cursor.fetchall()
        return res if res else 0
    except sqlite3.OperationalError:
        return 0


def commit(req):
    connection, cursor = connect()
    try:
        cursor.execute(req)
        connection.commit()
        return 1
    except sqlite3.OperationalError:
        return 0