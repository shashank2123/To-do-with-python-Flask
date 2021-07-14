from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():

	app = Flask(__name__)

	app.config['SECRET_KEY'] = 'secret_key'
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	db.init_app(app)

	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	from models import user

	@login_manager.user_loader
	def load_user(user_id):
		return user.query.get(int(user_id))

	from main import main as main_blueprint
	from auth import auth as auth_blueprint

	app.register_blueprint(main_blueprint)
	app.register_blueprint(auth_blueprint)

	return app

app = create_app()

if __name__=="__main__":
	app.run()


