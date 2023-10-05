from flask import url_for
from marefiya import db, login_manager, app
from flask_login import UserMixin

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	full_name = db.Column(db.String(50), nullable=False)
	email = db.Column(db.String(120), nullable=False, unique=True)
	image_file = db.Column(db.String(20), nullable=False ,default='default.jpg')
	password = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f"USER({self.full_name}, {self.email} , {self.image_file})"

class Owner(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	full_name = db.Column(db.String(50), nullable=False)
	phone = db.Column(db.Integer, nullable=False, unique=True)
	email = db.Column(db.String(120), nullable=False, unique=True)
	image_file = db.Column(db.String(20), nullable=False ,default='static/img/profile_pic/admin.jpg')
	password = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f"Owner({self.full_name}, {self.email} , {self.image_file})"	

class Assets(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	owner_id = db.Column(db.Integer, nullable=False, unique=True)
	title = db.Column(db.String(50), nullable=False, unique=True)
	description = db.Column(db.Text, nullable=False)
	asset_longtude = db.Column(db.Integer, nullable=False, unique=True)
	asset_latitude = db.Column(db.Integer, nullable=False, unique=True)
	rent_or_buy = db.Column(db.String(20), nullable=False)
	thumbnail = db.Column(db.String(20), nullable=False ,default='default.jpg')
	price = db.Column(db.Integer, nullable=False)
	price_rate = db.Column(db.String(50), nullable=False)
	gallery = 'admin.jpg'
	asset_gallery = db.Column(db.String(20), nullable=False ,default=gallery)

	def __repr__(self):
		return f"Owner({self.title}, {self.asset_longtude} , {self.thumbnail})"

