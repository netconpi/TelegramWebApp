
import sqlite3

import psycopg2
import psycopg2.extras
from random import randint

def postgree_fetch(requs_db: str):
    try:
        with psycopg2.connect(
                    host = 'localhost',
                    dbname = 'dbms_db',
                    user = 'dbms',
                    password = 'secretPassword',
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
                    dbname = 'dbms_db',
                    user = 'dbms',
                    password = 'secretPassword',
                    port = 5432) as conn:

            with conn.cursor() as cur:
                cur.execute(requs_db)
                conn.commit()
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


def check(telegram_id, typee='company'):
    if typee == 'company':
        registred = postgree_fetch(f'''SELECT telegram_id FROM "tgWebAppRender_company" WHERE telegram_id=''' + f"'{telegram_id}'")
    elif typee == 'user':
        registred = postgree_fetch(f'''SELECT telegram_id FROM "tgWebAppRender_userapp" WHERE telegram_id=''' + f"'{telegram_id}'")
    elif typee == 'share':
        own_id = postgree_fetch(f'''SELECT id FROM "tgWebAppRender_company" WHERE telegram_id=''' + f"'{telegram_id}'")[0][0]
        registred = postgree_fetch(f'''SELECT token FROM "tgWebAppRender_invationtoken" WHERE owner_id=''' + f"'{own_id}'")

    if not registred:
        return False
    else:
        return True


def get(telegram_id, typee='share'):
    if typee == 'share':
        own_id = postgree_fetch(f'''SELECT id FROM "tgWebAppRender_company" WHERE telegram_id=''' + f"'{telegram_id}'")[0][0]
        data = postgree_fetch(f'''SELECT token FROM "tgWebAppRender_invationtoken" WHERE owner_id=''' + f"'{own_id}'")

    if not data:
        return False
    else:
        return data[0][0]


def generate_token(telegram_id):
    token = randint(100000000000000, 9999999999999999999)
    own_id = postgree_fetch(f'''SELECT id FROM "tgWebAppRender_company" WHERE telegram_id=''' + f"'{telegram_id}'")[0][0]
    res = postgree_commit(
        f'''INSERT INTO "tgWebAppRender_invationtoken" (token, owner_id) VALUES ({token}, {own_id});'''
    )

    return token
