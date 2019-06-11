from flaskblog import app
from flask import render_template, url_for, flash, redirect
from flaskblog.forms import Login, Register

# list of posts for blog
posts = [
    {
        'author': 'Shivam Swarnkar',
        'date_posted': '20/04/19',
        'content': 'La ba bbab ke babba ne haa baba'
    },
    {
        'author': 'Shriyan Blue',
        'date_posted': '19/07/18',
        'content': 'Yada yada hi dharmshya, glarin bhavit bharata'
    }
]
# test
dummy_email = 'shivam_swarnkar@rediffmail.com'
dummy_password = '12345678'


@app.route("/")
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        if(form.email.data == dummy_email
                and form.password.data == dummy_password):
            flash('Successfully Logged In', 'success')
            return redirect(url_for('home'))
        else:
            flash('Email address or password is incorrect. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form )

