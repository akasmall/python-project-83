# from functools import wraps
import psycopg2
from psycopg2.extras import NamedTupleCursor


def connect_db(app):
    return psycopg2.connect(app.config['DATABASE_URL'])


def close(conn):
    conn.close()


# def perform_in_db(with_commit: bool = False):  # noqa: C901
#     def decorator(func: callable):

#         @wraps(func)
#         def inner(*args, **kwargs):
#             conn = args[0]
#             if not isinstance(conn, psycopg2.extensions.connection):
#                 raise ValueError('First argument must be psycopg2 connection')
#             try:
#                 with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
#                     result = func(cursor=cursor, *args, **kwargs)
#                     if with_commit:
#                         conn.commit()
#                     return result
#             except Exception as err:
#                 if conn:
#                     conn.rollback()
#                 raise err

#         return inner

#     return decorator


# @perform_in_db(with_commit=True)
# def insert_url(conn, url, cursor=None):  # pylint: disable=W0613
#     cursor.execute(
#         'INSERT INTO urls (name) VALUES (%s) RETURNING id;',
#         (url,)
#     )
#     result = cursor.fetchone().id
#     return result


# @perform_in_db()
# def get_url(conn, url_id, cursor=None):  # pylint: disable=W0613
#     cursor.execute('SELECT * FROM urls WHERE id = (%s);', (url_id,))
#     result = cursor.fetchone()
#     return result


# @perform_in_db()
# def check_url_exists(conn, url, cursor=None):  # pylint: disable=W0613
#     cursor.execute(
#         'SELECT * FROM urls WHERE name = (%s);', (url,))
#     result = cursor.fetchone()
#     return result


# @perform_in_db(with_commit=True)
# def insert_check(conn, url_id, url_info, cursor=None):
# # pylint: disable=W0613
#     cursor.execute(
#         'INSERT INTO url_checks (url_id, status_code, h1, title, description)'
#         'VALUES (%s, %s, %s, %s, %s);',
#         (url_id, url_info['status_code'], url_info['h1'],
#          url_info['title'], url_info['description']))


# @perform_in_db()
# def get_url_checks(conn, url_id, cursor=None):  # pylint: disable=W0613
#     cursor.execute(
#         'SELECT * FROM url_checks WHERE url_id = (%s) ORDER BY id DESC;',
#         (url_id,)
#     )
#     result = cursor.fetchall()
#     return result


# @perform_in_db()
# def get_urls_with_latest_check(conn, cursor=None):
#     # pylint: disable=W0613
#     cursor.execute(
#         'SELECT DISTINCT ON (urls.id) '
#         'urls.id AS id, '
#         'urls.name AS name, '
#         'url_checks.created_at AS created_at, '
#         'url_checks.status_code AS status_code, '
#         'url_checks.url_id AS url_id '
#         'FROM urls '
#         'LEFT JOIN url_checks ON urls.id=url_checks.url_id '
#         'ORDER BY urls.id DESC, url_checks.url_id DESC;')
#     result = cursor.fetchall()
#     return result


def execute_query(app, query, params=None, fetch_one=False, fetch_all=False):
    conn = connect_db(app)
    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)
        cursor.execute(query, params or ())

        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            result = None
        if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
            conn.commit()

        return result
    except Exception as err:
        # В случае ошибки откатываем
        conn.rollback()
        raise err
    finally:
        if cursor:
            cursor.close()
        close(conn)


def insert_url(app, url):
    query = 'INSERT INTO urls (name) VALUES (%s) RETURNING id;'
    result = execute_query(app, query, (url,), fetch_one=True)
    return result.id


def get_url(app, url_id):
    query = 'SELECT * FROM urls WHERE id = (%s);'
    result = execute_query(app, query, (url_id,), fetch_one=True)
    return result


def check_url_exists(app, url):
    query = 'SELECT * FROM urls WHERE name = (%s);'
    result = execute_query(app, query, (url,), fetch_one=True)
    return result


def get_url_checks(app, url_id,):
    query = 'SELECT * FROM url_checks WHERE url_id = (%s) ORDER BY id DESC;'
    result = execute_query(app, query, (url_id,), fetch_all=True)
    return result


def insert_check(app, url_id, url_info):
    query = (
        'INSERT INTO url_checks (url_id, status_code, h1, title, description)'
        'VALUES (%s, %s, %s, %s, %s);'
    )
    url_info_data = (
        url_id,
        url_info['status_code'],
        url_info['h1'],
        url_info['title'],
        url_info['description']
    )
    execute_query(app, query, url_info_data)
    # execute_query(app, query, url_info_data, fetch_all=True)


def get_urls_with_latest_check(app):
    query = (
        'SELECT DISTINCT ON(urls.id) '
        'urls.id AS id, '
        'urls.name AS name, '
        'url_checks.created_at AS created_at, '
        'url_checks.status_code AS status_code, '
        'url_checks.url_id AS url_id '
        'FROM urls '
        'LEFT JOIN url_checks ON urls.id = url_checks.url_id '
        'ORDER BY urls.id DESC, url_checks.url_id DESC;'
    )
    result = execute_query(app, query, fetch_all=True)
    return result
