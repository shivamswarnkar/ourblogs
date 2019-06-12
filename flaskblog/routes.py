from flaskblog import app, bcrypt, db
from flask import render_template, url_for, flash, redirect
from flaskblog.forms import Login, Register
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user

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
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('home'))
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
            return redirect(url_for('home'))
        else:
            flash('Email address or password is incorrect. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


