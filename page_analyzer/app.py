import requests
from dotenv import load_dotenv
from flask import (
    Flask, flash, redirect, render_template,
    abort, request, url_for
)
from page_analyzer import db_manager as db
from page_analyzer.utils import normalize_url, validate_url
from page_analyzer.page_checker import extract_page_data
from page_analyzer.config import config


load_dotenv()
app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['DATABASE_URL'] = config.DATABASE_URL


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def show_urls_page():
    conn = db.connect_db(app)
    urls_check = db.get_urls_with_latest_check(conn)
    db.close(conn)
    return render_template('urls/list.html', urls_check=urls_check)


@app.get('/urls/<url_id>')
def show_url_page(url_id):
    conn = db.connect_db(app)
    url = db.get_url(conn, url_id)
    if not url:
        abort(404)
    checks = db.get_url_checks(conn, url_id)
    db.close(conn)
    return render_template('urls/detail.html', url=url, checks=checks)


@app.post('/urls')
def add_url():
    url = request.form.get('url')
    normal_url = normalize_url(url)
    is_valid, error_message = validate_url(normal_url)
    if not is_valid:
        flash(error_message, 'danger')
        return render_template('index.html', url=normal_url), 422
    conn = db.connect_db(app)
    url_info = db.check_url_exists(conn, normal_url)
    if url_info:
        flash('Страница уже существует', 'info')
        url_id = url_info.id
    else:
        flash('Страница успешно добавлена', 'success')
        url_id = db.insert_url(conn, normal_url)
    db.close(conn)

    return redirect(url_for('show_url_page', url_id=url_id))


@app.post('/urls/<url_id>/check')
def check_url_page(url_id):
    conn = db.connect_db(app)
    url = db.get_url(conn, url_id)
    try:
        response = requests.get(url.name, timeout=50)
        response.raise_for_status()
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        conn.close()
        return redirect(url_for('show_url_page', url_id=url_id))

    url_info = extract_page_data(response.text, response.status_code)
    flash('Страница успешно проверена', 'success')
    db.insert_check(conn, url_id, url_info)
    db.close(conn)

    return redirect(url_for('show_url_page', url_id=url_id))


@app.errorhandler(404)
def page_not_found(_):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(_):
    return render_template('errors/500.html'), 500


if __name__ == '__main__':
    app.run()
