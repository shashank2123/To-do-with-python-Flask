from flask import Blueprint , render_template , request, url_for , redirect , flash
from werkzeug.security import generate_password_hash , check_password_hash
from app import db
from models import user
from flask_login import login_required , login_user , logout_user

auth = Blueprint("auth",__name__)

@auth.route("/signup")
def signup():
	return render_template("signup.html")

@auth.route("/signup", methods = ['POST'])
def signup_post():
	name = request.form.get('name')
	username = request.form.get('username')
	password = request.form.get('password')

	get_user = user.query.filter_by(username=username).first()
	print(password,get_user)
	if get_user:
		return render_template("signup.html",error="Username already taken")

	new_user = user(name=name,username=username,password=generate_password_hash(password, method='sha256'))
	db.session.add(new_user)
	db.session.commit()
	flash(" Account Successfully created ")
	return redirect(url_for('auth.login'))

@auth.route("/login")
def login():
	return render_template("login.html")

@auth.route("/login", methods = ['POST'])
def login_post():
	username = request.form.get('username')
	password = request.form.get('password')

	get_user = user.query.filter_by(username=username).first()

	if not get_user or not check_password_hash(get_user.password,password):
		return render_template("login.html",error="Incorrect password or username")

	login_user(get_user,remember=True)

	flash("Successfully Logged in ")
	
	return redirect(url_for('main.index'))



@auth.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for('main.index'))