'''
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required

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
    

def get_post(id):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, '
        'FROM post p JOIN user u ON p.author_id = u.id, '
        'WHERE p.id = ?', (id,)
    ).fetchone()

    error = None

    if post is None:
        abort(404, "Post doesn't exist.")
    elif post['author_id'] != g.user:
        abort(403, 'Access denied.')
    
    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update_post(id):
    post = get_post(id)
    error = None

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
    
        if title is None:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db().execute(
                'UPDATE post SET title = ?, '
                'body = ? WHERE id = ?',
                (title, body, id))
            db.commit()
            return redirect(url_for('blog'))
        
    return render_template('blog/update.html',post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete_post(id):
    get_post(id)
    db = get_db()
    db.execute(
        'DELETE FROM post WHERE id = ?', (id,)
    )
    db.commit()
    return redirect(url_for('blog'))
'''