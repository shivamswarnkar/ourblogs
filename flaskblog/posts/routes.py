from flask import (Blueprint, request, render_template,
                   flash, abort, redirect, url_for)
from flask_login import login_required, current_user
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm
from flaskblog import db

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post was created successfully.', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', legend='New Post', form=form)


@posts.route('/post/<int:post_id>')
def read_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    return render_template('post.html', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post was updated successfully.', 'success')
        return redirect(url_for('posts.read_post', post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', legend='Update Post', form=form)


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if current_user != post.author:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post was deleted successfully.', 'info')
    return redirect(url_for('main.home'))
