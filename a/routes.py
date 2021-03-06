import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from a import app, db, bcrypt
from a.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from a.model import User, Post
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
@app.route('/home')
def home():
	posts = Post.query.all()
	return render_template("home.html", posts=posts)
    
    
@app.route('/about')
def about():
    return render_template("about.html", title="About")

@app.route('/social_activities')
def social_activities():
    return render_template("social and activities.html", title="social and activities")


@app.route('/events')
def events():
    return render_template("events.html", title="Events")

@app.route('/learn')
def learn():
    return render_template("learn.html", title="Learn")

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, 
			firstname=form.firstname.data,
			lastname=form.lastname.data,
			email=form.email.data, 
			password=hashed_password, 
			age=form.age.data, 
			city=form.city.data, 
			phonenumber=form.phonenumber.data)
		db.session.add(user)
		db.session.commit()
		flash('your account created!', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title = 'Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			if next_page:
				return redirect(next_page)
			else:
				return redirect(url_for('home'))
		else:
			flash("Invalid username or password", 'danger')
	return render_template('login.html', title = 'Login', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))

def save_picture(form_picture):
	random_hex=secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

	output_size = (125, 125)
	p = Image.open(form_picture)
	p.thumbnail(output_size)
	p.save(picture_path)

	return picture_fn


@app.route('/membership', methods=['GET', 'POST'])
@login_required
def membership():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.firstname = form.firstname.data
		current_user.lastname = form.lastname.data
		current_user.age = form.age.data
		current_user.city = form.city.data
		current_user.email = form.email.data
		current_user.phonenumber = form.phonenumber.data
		db.session.commit()
		flash('your account has been update', 'success')
		return redirect(url_for('membership'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.firstname.data = current_user.firstname
		form.lastname.data = current_user.lastname
		form.age.data = current_user.age
		form.city.data = current_user.city
		form.email.data = current_user.email
		form.phonenumber.data = current_user.phonenumber
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('membership.html', title = 'Membership', image_file=image_file, form=form)





@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('your post has been created', 'success')
		return redirect(url_for('home'))
	return render_template('create_post.html', title='New Post', 
		form=form, legend='New Post')

@app.route('/post/<int:post_id>')
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('your post has been updated', 'success')
		return redirect(url_for('post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title='Update Post', 
		form=form, legend='Update Post')

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('your post has been deleted', 'success')
	return redirect(url_for('home'))

