import sqlite3
from flask import Blueprint, render_template, url_for, redirect, session, request, flash, g

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


menu = [{'url': '.index', 'title': 'Panel'},
        {'url': '.listpubs', 'title': 'List of articles'},
        {'url': '.listusers', 'title': 'List of users'},
        {'url': '.logout', 'title': 'Logout'}]

db = None


@admin.before_request
def before_request():
    global db
    db = g.get('link_db')


@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


def isLogged():
    return True if session.get('admin_logged') else False


def login_admin():
    session['admin_logged'] = 1


def logout_admin():
    session.pop('admin_logged', None)


@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.login'))

    return render_template('admin/index.html', menu=menu, title='Admin panel')


@admin.route('/login', methods=["POST", "GET"])
def login():
    if isLogged():
        return redirect(url_for('.index'))

    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['psw'] == "12345":
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash('Wrong email or password', 'error')
    return render_template('admin/login.html', title='Admin-panel')


@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))

    logout_admin()

    return redirect(url_for('.login'))

@admin.route('/list-pubs')
def listpubs():
    if not isLogged():
        return redirect(url_for('.login'))

    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT title, text, url FROM posts")
            list = cur.fetchall()
        except sqlite3.Error as e:
            print('Articles getting from DB error' + str(e))

    return render_template('admin/listpubs.html', title='List of articles', menu=menu, list=list)


@admin.route('/list-users')
def listusers():
    if not isLogged():
        return redirect(url_for('.login'))

    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT name, email FROM users ORDER BY time DESC")
            list = cur.fetchall()
        except sqlite3.Error as e:
            print('List of users getting from DB error' + str(e))

    return render_template('admin/listusers.html', title='List of users', menu=menu, list=list)
