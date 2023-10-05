import os, secrets
from flask import render_template, url_for, flash, redirect, request
from marefiya.forms import UserRegistrationForm, AdminRegistrationForm, UserLoginForm, AdminLoginForm, NewAssetForm, AssetSearch, SearchAgain, FilterResults, EditAssetForm, UpdateAdminAccount, UpdateUserAccount
from marefiya.models import User, Owner, Assets
from marefiya import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
	form = AssetSearch()
	if request.method == "POST":
		if form.start_price.data:
			pass
		else: 	
			form.start_price.data = 0

		if form.final_price.data:
			pass
		else:
			form.final_price.data = 10000000000000000000000000000
		return redirect(f'search/{form.name.data}/{form.start_price.data}/{form.final_price.data}/{form.rent_or_buy.data}')
	

	return render_template('index.html', form=form)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = UserRegistrationForm()
	form2 = AdminRegistrationForm()
	
	if form.submit.data and form.validate():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(full_name=form.full_name.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created you can now login!', 'success')
		return redirect(url_for('login'))
	
	elif form2.submit2.data and form2.validate():
		hashed_password = bcrypt.generate_password_hash(form2.password.data).decode('utf-8')
		owner = Owner(full_name=form2.full_name.data, email=form2.email.data, phone=form2.phone.data, password=hashed_password)
		db.session.add(owner)
		db.session.commit()
		flash('Your account has been created you can now login!', 'success')
		return redirect(url_for('login'))
	
	return render_template('signup.html', form=form, form2=form2)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = UserLoginForm()
	form2 = AdminLoginForm()

	if form.submit.data and form.validate():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user)
			next_page = request.args.get('next')
			flash('You have succesfully logged in.', 'success')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Attempt was unsuccessful check email and password', 'danger')
			return redirect(url_for('login'))
		return redirect(url_for('home'))
	
	if form2.submit2.data and form2.validate():
		owner = Owner.query.filter_by(email=form2.email.data).first()
		if owner and bcrypt.check_password_hash(owner.password, form2.password.data):
			login_user(owner)
			flash('You have succesfully logged in.', 'success')
			return redirect(url_for('admin_dashboard'))
		else:
			flash('Login Attempt was unsuccessful check email and password', 'danger')
			return redirect(url_for('login'))
		return redirect(url_for('home'))

	return render_template('login.html', form=form, form2=form2)

@app.route('/logout_users')
@login_required
def logout_users():
	logout_user()
	flash('You have been successfully logged out.', 'success')
	return redirect(url_for('home'))

@app.route('/logout_owners')
@login_required
def logout_owners():
	logout_user()
	flash('You have been successfully logged out.', 'success')
	return redirect(url_for('home'))
	
@app.route('/user_account', methods=['GET', 'POST'])
@login_required
def user_account():
	form = UpdateUserAccount()
	user = User.query.filter_by(id=current_user.id).first()
	if request.method == "POST":
		if form.full_name.data != user.full_name:
			user.full_name = form.full_name.data
			db.session.commit()
		if form.email.data != user.email:	
			user.email = form.email.data
			db.session.commit()
		flash('Account Updated Succesfully!', 'success')
		return redirect(url_for('user_account'))
	return render_template('user_profile.html', user=user, form=form)

@app.route('/admin_account', methods=['POST', 'GET'])
@login_required
def admin_account():
	form = UpdateAdminAccount()
	owner = Owner.query.filter_by(id=current_user.id).first()
	if request.method == "POST":
		if form.full_name.data != owner.full_name:
			owner.full_name = form.full_name.data
			db.session.commit()
		if form.email.data != owner.email:	
			owner.email = form.email.data
			db.session.commit()
		if form.phone.data != owner.phone:
			owner.phone = form.phone.data
			db.session.commit()
		flash('Account Updated Succesfully!', 'success')
		return redirect(url_for('admin_account'))
	return render_template('admin_profile.html', owner=owner, form=form)

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
	assets = Assets.query.filter_by(owner_id=current_user.id).order_by(Assets.id.desc()).all()
	if current_user.phone:
		return render_template('admin_panel.html', assets=assets)
	else:
		flash('You are not authortized to access this page.', 'info')
		return redirect(url_for('home'))

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static\\img\\Marefiyas\\', picture_fn)
	form_picture.save(picture_path) 
	
	return picture_path

@app.route('/new_asset', methods=['GET', 'POST'])
@login_required
def new_asset():
	form = NewAssetForm()
	if form.validate_on_submit():
		picture_file = save_picture(form.thumbnail.data)
		asset = Assets(owner_id=current_user.id, title=form.title.data, description=form.description.data,
		asset_longtude=form.location_2.data, asset_latitude=form.location_1.data, rent_or_buy=form.own_type.data,
		price=form.price.data,price_rate=form.price_dur.data, thumbnail=picture_file)
		db.session.add(asset)
		db.session.commit()	
		flash('Your new Asset has been added.', 'success')
		return redirect(url_for('admin_dashboard'))
	
	elif current_user.phone:
		return render_template('new_asset.html', form=form)
	else:
		flash('You are not authortized to access this page.', 'info')
		return redirect(url_for('home'))

@app.route('/search/<string:q>/<int:start_price>/<int:final_price>/<string:rent>', methods=['GET', 'POST'])
def search(q, start_price, final_price,rent):
	form = SearchAgain()
	form2 = FilterResults()

	if form.submit.data and form.validate():
		if form2.start_price.data:
			pass
		else:
			form2.start_price.data = 0
		
		if form2.final_price.data:
			pass
		else:
			form2.final_price.data = 100000000000000000000000000000

		if form2.own_type.data:
			pass
		else:
			form2.own_type.data = 'Rent-Buy'	
		return redirect(url_for('search',form=form,form2=form2 , q=form.name.data, start_price=form2.start_price.data, final_price=form2.final_price.data ,rent=form2.own_type.data))

	elif request.method == "POST":
		if form2.start_price.data:
			pass
		else:
			form2.start_price.data = 0
		
		if form2.final_price.data:
			pass
		else:
			form2.final_price.data = 100000000000000000000000000000

		if form.name.data:
			return redirect(url_for('search', q=form.name.data, start_price=form2.start_price.data, final_price=form2.final_price.data, rent=str(form2.own_type.data)))
		else:	
			return redirect(url_for('search', q=q, start_price=form2.start_price.data, final_price=form2.final_price.data, rent=str(form2.own_type.data)))

	elif request.method == "GET":
		assets = Assets.query.filter_by(title=q).all()

		if start_price != 0:
			for asset in assets:
				if asset.price >= start_price:
					pass
				else:
					assets.remove(asset)
		if final_price != 0:
			for asset in assets:
				if asset.price <= final_price:
					pass
				else:
					assets.remove(asset)
		if rent != 'Rent-Buy':
			for asset in assets:
				if asset.rent_or_buy == rent:
					pass
				else:
					assets.remove(asset)
		return render_template('search_results.html', assets=assets, form2=form2, form=form, q=q, start_price=start_price, final_price=final_price,rent=rent)

@app.route('/detail/<int:id>', methods=['GET','POST'])
def detail(id):
	asset = Assets.query.filter_by(id=id).first()
	owner = Owner.query.filter_by(id=asset.owner_id).first()
	return render_template('product_detail.html', asset=asset, owner=owner)

@app.route('/delete_asset/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_asset(id):
	asset = Assets.query.filter_by(id=id).first()
	db.session.delete(asset)
	db.session.commit()
	flash('Your selected asset has been deleted.', 'success')
	return redirect(url_for('admin_dashboard'))

@app.route('/edit_asset/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_asset(id):
	form = EditAssetForm()
	first_asset = Assets.query.filter_by(id=id).first()
	if form.validate_on_submit():
		db.session.delete(first_asset)
		db.session.commit()
		picture_file = save_picture(form.thumbnail.data)
		asset = Assets(owner_id=current_user.id, title=form.title.data, description=form.description.data,
		asset_longtude=form.location_2.data, asset_latitude=form.location_1.data, rent_or_buy=form.own_type.data,
		price=form.price.data,price_rate=form.price_dur.data, thumbnail=picture_file)
		db.session.add(asset)
		db.session.commit()	
		flash('Your asset has been updated.', 'success')
		return redirect(url_for('admin_dashboard'))
	
	return render_template('edit_asset.html', form=form, asset=first_asset)