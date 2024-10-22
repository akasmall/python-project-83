import os

from flask import (
    Flask, flash, redirect, render_template,
    abort, request, url_for
)
from page_analyzer import db_manager as db
from page_analyzer.utils import normalize_url, validate_url

try:
    from dotenv import load_dotenv

    load_dotenv('.env.dev')
except ModuleNotFoundError:
    pass


# load_dotenv('.env')
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls/')
def show_urls_page():
    conn = db.connect_db(app)
    urls_check = db.get_urls_with_latest_check(conn)
    db.close(conn)
    return render_template('urls/list.html', urls_check=urls_check)


@app.route('/urls/<url_id>/')
def show_url_page(url_id):
    conn = db.connect_db(app)
    url = db.get_url(conn, url_id)
    if not url:
        abort(404)
    checks = db.get_url_checks(conn, url_id)
    db.close(conn)
    return render_template('urls/default.html', url=url, checks=checks)


@app.route('/urls/', methods=['POST'])
def add_url():
    url = request.form.get('url')
    normal_url = normalize_url(url)
    url_check_result = validate_url(normal_url)
    if url_check_result:
        flash(url_check_result, 'danger')
        return render_template('index.html'), 422
    conn = db.connect_db(app)
    url_info = db.check_url_exists(conn, normal_url)
    if url_info:
        # flash('Страница уже существует', 'success')
        url_id = url_info.id
    else:
        # flash('Страница успешно добавлена', 'success')
        url_id = db.insert_url(conn, normal_url)
    db.close(conn)

    return redirect(url_for('show_url_page', url_id=url_id))


@app.route('/urls/<url_id>/check/', methods=['POST'])
def check_url_page(url_id):
    conn = db.connect_db(app)
    flash('Страница успешно проверена', 'success')
    url_info = {}
    db.insert_check(conn, url_id, url_info)
    db.close(conn)

    return redirect(url_for('show_url_page', url_id=url_id))


if __name__ == '__main__':
    app.run()
