from contextlib import contextmanager
import psycopg2
from psycopg2.extras import NamedTupleCursor


def connect_db(db_url):
    return psycopg2.connect(db_url)


def close(conn):
    conn.close()


@contextmanager
def get_connection(db_url):
    conn = None
    try:
        conn = connect_db(db_url)
        yield conn
        conn.commit()
    except Exception as err:
        conn.rollback()
        raise err
    finally:
        if conn:
            conn.close()


def get_url(conn, url_id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        query = 'SELECT * FROM urls WHERE id = (%s);'
        cur.execute(query, (url_id,))
        result = cur.fetchone()
        return result


def insert_url(conn, url):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        query = 'INSERT INTO urls (name) VALUES (%s) RETURNING id;'
        cur.execute(query, (url,))
        result = cur.fetchone()
        return result.id


def check_url_exists(conn, url):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        query = 'SELECT * FROM urls WHERE name = (%s);'
        cur.execute(query, (url,))
        result = cur.fetchone()
        return result


def get_url_checks(conn, url_id,):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        query = 'SELECT * FROM url_checks WHERE url_id = (%s) ORDER BY id DESC;'
        cur.execute(query, (url_id,))
        result = cur.fetchall()
        return result


def insert_check(conn, url_id, url_info):
    url_info_data = (
        url_id,
        url_info['status_code'],
        url_info['h1'],
        url_info['title'],
        url_info['description']
    )
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        query = (
            '''INSERT INTO url_checks (
                url_id,
                status_code,
                h1,
                title,
                description
                )
            VALUES (%s, %s, %s, %s, %s);
            '''
        )
        cur.execute(query, url_info_data)


def get_urls_with_latest_check(conn):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
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
        cur.execute(query)
        result = cur.fetchall()
        return result
