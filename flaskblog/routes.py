from flaskblog import app, bcrypt, db
from flask import render_template, url_for, flash, redirect, request
from flaskblog.forms import Login, Register, AccountInfo
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image

# list of posts for blog
posts = [
    {
        'author': 'Shivam Swarnkar',
        'date_posted': '20/04/19',
        'title': 'Blog 1',
        'content': 'La ba bbab ke babba ne haa baba'
    },
    {
        'author': 'Shriyan Blue',
        'date_posted': '19/07/18',
        'title': 'Blog 2',
        'content': 'Yada yada hi dharmshya, glarin bhavit bharata'
    }
]


@app.route("/")
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Register()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    password=hashed_password,
                    email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account has been created. Please login for account access.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Successfully Logged In', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Email address or password is incorrect. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    # random file name
    random_hex = secrets.token_hex(8)

    # getting picture path
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex+f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # resizing image
    output_size = (125,125)
    picture = Image.open(form_picture)
    picture.thumbnail(output_size)

    # saving image
    picture.save(picture_path)
    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountInfo()
    if form.validate_on_submit():
        if form.picture.data:
            # delete current profile image if current is not default.jpg
            if current_user.image_file != 'default.jpg':
                current_image_path = os.path.join(app.root_path, 'static/profile_pics', current_user.image_file)
                os.remove(current_image_path)
            # save new profile image
            current_user.image_file = save_picture(form.picture.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/'+current_user.image_file)

    return render_template('account.html', title='Account', form=form, image_file=image_file)


