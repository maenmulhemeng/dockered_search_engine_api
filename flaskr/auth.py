import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db,close_db,get_real_dict_cursor

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                cur = db.cursor()
                cur.execute(
                    'INSERT INTO public.user (username, password) VALUES (%s, %s);',
                    (username, generate_password_hash(password)),
                )               
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)
        close_db()
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        try:
            cur = get_real_dict_cursor()
            q = cur.mogrify('SELECT * FROM public.user WHERE username=%s ;',(username,))
            cur.execute(q)
            user = cur.fetchone()
            error = None
            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'

            if error is None:
                close_db()
                session.clear()
                session['user_id'] = user['id']
                u = url_for('index.index')
                return redirect(u)
            else:
                flash(error)
        except  Exception as e: 
            error = repr(e)
            pass
    else:
        return render_template('auth/login.html')
       

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


