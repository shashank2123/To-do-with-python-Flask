from flask import Blueprint , render_template , request, url_for , redirect , flash
from flask_login import login_required , current_user
import datetime
from models import Works,user
from app import db

main = Blueprint("main",__name__)

@main.route("/")
def index():
	return render_template("index.html")

@main.route("/add")
@login_required
def add():
	return render_template("new_add.html")

@main.route("/add", methods=['POST'])
@login_required
def add_post():
	title = request.form.get('title')
	start_date = request.form.get('start_date').replace('T'," ")
	end_date = request.form.get("end_date").replace('T'," ")
	description = request.form.get("description")


	start_date_obj = datetime.datetime.strptime(start_date,'%Y-%m-%d %H:%M')
	end_date_obj = datetime.datetime.strptime(end_date,'%Y-%m-%d %H:%M')


	if start_date_obj>end_date_obj or start_date_obj<datetime.datetime.now():
		return render_template("new_add.html",error = "start must be less than end and today")

	new_work = Works(author = current_user,title=title,start_datetime=start_date_obj,end_datetime=end_date_obj,discription=description)
	db.session.add(new_work)
	db.session.commit()

	flash(" Work is added successfully")

	return redirect(url_for('main.list_all'))


@main.route("/list")
@login_required
def list_all():
	return render_template("list.html",works=current_user.works)

@main.route("/list/<int:work_id>/change", methods=['GET'])
@login_required
def change_status(work_id):
	work = Works.query.get_or_404(int(work_id))
	if work.is_completed == 0:
		work.is_completed=1
	else:
		work.is_completed=0

	db.session.commit()

	return redirect(url_for('main.list_all'))

@main.route("/list/<int:work_id>/delete",methods=['GET'])
@login_required
def delete(work_id):
	work = Works.query.get_or_404(int(work_id))
	db.session.delete(work)
	db.session.commit()
	flash("Successfully deteted ")
	return redirect(url_for('main.list_all'))


@main.route("/list/<int:work_id>/edit",methods=['GET','POST'])
@login_required
def edit(work_id):
	work = Works.query.get_or_404(int(work_id))
	if request.method == 'POST':
		title = request.form.get('title')
		start_date = request.form.get('start_date').replace('T'," ")
		end_date = request.form.get("end_date").replace('T'," ")
		description = request.form.get("description")


		start_date_obj = datetime.datetime.strptime(start_date,'%Y-%m-%d %H:%M')
		end_date_obj = datetime.datetime.strptime(end_date,'%Y-%m-%d %H:%M')


		if start_date_obj>end_date_obj:
			return render_template("new_add.html",error = "start must be less than end")
		work.title = title
		work.start_datetime = start_date_obj
		work.end_datetime = end_date_obj
		work.description = description
		db.session.commit()
		print(Works.query.get_or_404(int(work_id)).description)
		flash("Successfully updated ")
		return redirect(url_for('main.list_all'))

	return render_template("edit.html",work=work)




