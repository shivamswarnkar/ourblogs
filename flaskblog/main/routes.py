from flask import Blueprint, request, render_template
from flaskblog.models import Post

# create a blueprint
main = Blueprint('main', __name__)


@main.route("/")
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=3, page=page)
    return render_template('home.html', posts=posts)


@main.route('/about')
def about():
    return render_template('about.html', title='About')

@main.route('/privacy')
def privacy():
	return render_template('privacy.html', title='Privacy')

@main.route('/terms')
def terms():
	return render_template('terms.html', title='Privacy')