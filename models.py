from app import db
from flask_login import UserMixin

class user(db.Model,UserMixin):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(100),nullable=False)
	username = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(100), nullable=False)
	works = db.relationship('Works', backref='author', lazy = True)


class Works(db.Model):
	word_id = db.Column(db.Integer,primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	title = db.Column(db.String(100),nullable=False)
	discription = db.Column(db.String(256),nullable=False)
	start_datetime = db.Column(db.DateTime,nullable=False)
	end_datetime = db.Column(db.DateTime,nullable=False)
	is_completed = db.Column(db.Integer, nullable=False,default=0)
