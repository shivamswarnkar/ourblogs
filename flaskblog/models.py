from flaskblog import db


class User(db.model):
    username = db.Column(db.Integer, primary_key=True)


class Post(db.model):
    content = db.Column(db.Text, nullable=False)
