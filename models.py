from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from flask_login import UserMixin, LoginManager
from flask_login import AnonymousUserMixin

from config import Config

db = SQLAlchemy()
Base = declarative_base()

login_manager = LoginManager()
login_manager.login_view = 'display_login'


def setup_db(app, database_path=Config.SQLALCHEMY_DATABASE_URI):
    """
    setup_db(app)
        binds a flask application and a SQLAlchemy service
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

    # db.drop_all()
    db.create_all()

    login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    email = Column(String(64), unique=True, index=True)
    password = Column(String)
    notes = relationship('Note')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def rollback(self):
        db.session.rollback()


class Note(db.Model):
    __tablename__ = 'note'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    author_id = Column(Integer, ForeignKey('user.id'))
    created_on = Column(DateTime)
    modified_on = Column(DateTime)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def rollback(self):
        db.session.rollback()
