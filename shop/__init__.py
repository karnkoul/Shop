from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from flask_uploads import IMAGES, UploadSet, configure_uploads

import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'
app.config['SECRET_KEY'] = 'kjshadbvaksdjlhb123124'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir,'static/images')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOADED_PHOTOS_ALLOW'] = {'jpg', 'jpeg', 'png', 'gif', 'jfif'}
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos) 


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from shop.admin import routes
from shop.products import routes

def initialize_db():
    with app.app_context():
        db.create_all()