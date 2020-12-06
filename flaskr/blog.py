from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__, url_prefix='/blog')

@bp.route('/')
def blog():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username '
        'FROM post p  JOIN user u ON p.author_id = u.id '
        'ORDER BY created DSEC'
    ).fetchall()
    return render_template('blog/posts.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id) '
                'VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog'))

    return render_template('blog/create.html')
    