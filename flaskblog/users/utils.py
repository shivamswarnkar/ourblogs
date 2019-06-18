import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


def save_picture(form_picture):
    # random file name
    random_hex = secrets.token_hex(8)

    # getting picture path
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex+f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # resizing image
    output_size = (125, 125)
    picture = Image.open(form_picture)
    picture.thumbnail(output_size)

    # saving image
    picture.save(picture_path)
    return picture_fn


def delete_picture(image_file):
    current_image_path = os.path.join(current_app.root_path,
                                      'static/profile_pics', image_file)
    os.remove(current_image_path)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, please do not share this link with \
    anyone else and visit the following link to reset your password.
    {url_for('users.reset_token', token=token, _external=True)}
Note : This link will only be active for next 30 minutes. 
If you did not make this request then simply ignore this \
email and no changes will be made to your account. 
    '''
    mail.send(msg)
