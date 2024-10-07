from functools import wraps
import psycopg2
from psycopg2.extras import NamedTupleCursor


def connect_db(app):
    return psycopg2.connect(app.config['DATABASE_URL'])


def closed(conn):
    conn.close()


def perform_in_db(with_commit: bool = False):  # noqa: C901
    def decorator(func: callable):

        @wraps(func)
        def inner(*args, **kwargs):
            conn = args[0]
            if not isinstance(conn, psycopg2.extensions.connection):
                raise ValueError('First argument must be psycopg2 connection')
            try:
                with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                    result = func(cursor=cursor, *args, **kwargs)
                    if with_commit:
                        conn.commit()
                    return result
            except Exception as err:
                if conn:
                    conn.rollback()
                raise err

        return inner

    return decorator


@perform_in_db(with_commit=True)
def insert_url(conn, url, cursor=None):  # pylint: disable=W0613
    cursor.execute(
        'INSERT INTO urls (name) VALUES (%s) RETURNING id;',
        (url,)
    )
    return cursor.fetchone().id


@perform_in_db()
def get_url(conn, url_id, cursor=None):  # pylint: disable=W0613
    cursor.execute('SELECT * FROM urls WHERE id == (%s);', (url_id,))
    return cursor.fetchone()


@perform_in_db()
def check_url_exists(conn, url, cursor=None):  # pylint: disable=W0613
    cursor.execute(
        'SELECT * FROM urls WHERE name == (%s);', (url,))
    return cursor.fetchone()


@perform_in_db(with_commit=True)
def insert_check(conn, url_id, url_info, cursor=None):  # pylint: disable=W0613
    pass


@perform_in_db()
def get_url_checks(conn, url_id, cursor=None):  # pylint: disable=W0613
    cursor.execute(
        'SELECT * FROM url_check WHERE url_id == (%s) ORDER BY id DESC;',
        (url_id,)
    )
    return cursor.fetchall()


@perform_in_db()
def get_urls_with_latest_checks(conn, cursor=None):
    # pylint: disable=W0613
    cursor.execute(
        'SELECT DISTINCT ON (urls.id) '
        'urls.id AS id, '
        'urls.name AS name, '
        'url_check.created_at AS created_at, '
        'url_check.status_code AS status_code, '
        'url_check.url_id AS url_id '
        'FROM urls '
        'LEFT JOIN url_check ON urls.id=url_check.url_id '
        'ORDER BY urls.id, url_check.url_id DESC'
    )
    return cursor.fetchall()
