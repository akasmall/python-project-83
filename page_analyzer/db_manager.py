import psycopg2
from psycopg2.extras import NamedTupleCursor


def connect_db(db_url):
    return psycopg2.connect(db_url)


def close(conn):
    conn.close()


def insert_url(db_url, url):
    conn = connect_db(db_url)
    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)
        query = 'INSERT INTO urls (name) VALUES (%s) RETURNING id;'
        cursor.execute(query, (url,))
        result = cursor.fetchone()
    except Exception as err:
        conn.rollback()
        raise err
    finally:
        if cursor:
            cursor.close()
        conn.commit()
        close(conn)
    return result.id


def get_url(db_url, url_id):

    conn = connect_db(db_url)
    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)
        query = 'SELECT * FROM urls WHERE id = (%s);'
        cursor.execute(query, (url_id,))
        result = cursor.fetchone()
    except Exception as err:
        conn.rollback()
        raise err
    finally:
        if cursor:
            cursor.close()
        conn.commit()
        close(conn)
    return result


def check_url_exists(db_url, url):

    conn = connect_db(db_url)
    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)
        query = 'SELECT * FROM urls WHERE name = (%s);'
        cursor.execute(query, (url,))
        result = cursor.fetchone()
    except Exception as err:
        conn.rollback()
        raise err
    finally:
        if cursor:
            cursor.close()
        conn.commit()
        close(conn)
    return result


def get_url_checks(db_url, url_id,):

    conn = connect_db(db_url)
    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)
        query = 'SELECT * FROM url_checks WHERE url_id = (%s) ORDER BY id DESC;'
        cursor.execute(query, (url_id,))
        result = cursor.fetchall()
    except Exception as err:
        conn.rollback()
        raise err
    finally:
        if cursor:
            cursor.close()
        conn.commit()
        close(conn)
    return result


def insert_check(db_url, url_id, url_info):
    url_info_data = (
        url_id,
        url_info['status_code'],
        url_info['h1'],
        url_info['title'],
        url_info['description']
    )

    conn = connect_db(db_url)
    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)
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
        cursor.execute(query, url_info_data)
    except Exception as err:
        conn.rollback()
        raise err
    finally:
        if cursor:
            cursor.close()
        conn.commit()
        close(conn)


def get_urls_with_latest_check(db_url):

    conn = connect_db(db_url)
    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)
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
        cursor.execute(query)
        result = cursor.fetchall()
    except Exception as err:
        conn.rollback()
        raise err
    finally:
        if cursor:
            cursor.close()
        conn.commit()
        close(conn)
    return result
