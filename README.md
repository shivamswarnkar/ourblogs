# OurBlogs 
A light weight blogging app for sharing common knowledge and interests. [Sign Up Here](https://ourblogs.herokuapp.com)
### About
 OurBlogs is a flask powered webapp which allows users to create/update account, add/update/delete posts and share. It uses Flask-Login for handling user sessions along with Flask-Bcrypt for secure token generation. User can also request password reseting through email verification (implemented using Flask-Mail). 
 
### How to Run locally
First clone this repo & install all the dependencies.
```
$ git clone https://github.com/shivamswarnkar/ourblogs.git
$ cd ourblogs
$ pip install -r requirements.txt
```
Once everything is installed successfully, you should follow one of the following methods. 

**First Method (setup environment variables)** 
You need to add following env variables. You can generate new SECRET_KEY using python's secrets.token_hex(16)

- SECRET_KEY
- SQLALCHEMY_DATABASE_URI 
- MAIL_USERNAME
- MAIL_PASSWORD

***Recommendations***: set SQLALCHEMY_DATABASE_URI='sqlite:///site.db'

**Second Method (edit flaskblog/config.py)** 
First use python's secrets module to generate a SECRET_KEY
```
>>> import secrets
>>> token = secrets.token_hex(16)
```
Now set following vars in flaskblog/config.py
If you want to use mail services then enter your correct informations for mail username and password.
```
SECRET_KEY = token #generated in previous step
SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
MAIL_USERNAME = 'email@address.com' 
MAIL_PASSWORD = 'YOUR_EMAIL_PASSWORD' 
```

Now simply run following
```
$ python run.py
```
Your local server should be running. By default server not run on debug mode and use host=0.0.0.0 (in other words, it'll be visible on your private network. Edit routes and templates however you want.

***Note: Procfile is for Heroku deployment.***

### Dependencies

- bcrypt==3.1.7
- blinker==1.4
- cffi==1.12.3
- Click==7.0
- Flask==1.1.1
- Flask-Bcrypt==0.7.1
- Flask-Login==0.4.1
- Flask-Mail==0.9.1
- Flask-SQLAlchemy==2.4.0
- Flask-WTF==0.14.2
- gunicorn==19.9.0
- itsdangerous==1.1.0
- Jinja2==2.10.1
- MarkupSafe==1.1.1
- Pillow==6.1.0
- pycparser==2.19
- six==1.12.0
- SQLAlchemy==1.3.5
- Werkzeug==0.15.4
- WTForms==2.2.1