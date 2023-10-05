from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from marefiya.models import User, Owner
from marefiya import login_manager

@login_manager.user_loader
def load_user(user_id):
	return User().query.get(int(user_id))

@login_manager.user_loader
def load_user(user_id):
	return Owner().query.get(int(user_id))

class UserRegistrationForm(FlaskForm):
	full_name = StringField('Full Name:', validators=[DataRequired(), Length(min=5, max=50)])
	email = StringField('Email:', validators=[DataRequired(), Email()])
	password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=100)])
	confirm_password = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Signup')

	def validate_email(self, email):
		email = User.query.filter_by(email=email.data).first()
		if email:
			raise ValidationError("A user already exists with that email.")

class AdminRegistrationForm(FlaskForm):
	full_name = StringField('Full Name:', validators=[DataRequired(), Length(min=5, max=50)])
	email = StringField('Email:', validators=[DataRequired(), Email()])
	phone = StringField('Phone:', validators=[DataRequired()])
	password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=100)])
	confirm_password = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password')])
	submit2 = SubmitField('Signup')

	def validate_email(self, email):
		email = Owner.query.filter_by(email=email.data).first()
		if email:
			raise ValidationError("A user already exists with that email.")

	def validate_phone(self, phone):
		phone = Owner.query.filter_by(phone=phone.data).first()
		if phone:
			raise ValidationError("A user already exists with that phone number.")

class UserLoginForm(FlaskForm):
	email = StringField('Email:', validators=[DataRequired(), Email()])
	password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=100)])
	submit = SubmitField('Login')

class AdminLoginForm(FlaskForm):
	email = StringField('Admin Email:', validators=[DataRequired(), Email()])
	password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=100)])
	submit2 = SubmitField('Login')

class NewAssetForm(FlaskForm):
	title = StringField('Asset Title:', validators=[DataRequired(), Length(min=5, max=50)])
	location_1 = StringField('Asset Location:', validators=[DataRequired()])
	location_2 = StringField('Asset Location:', validators=[DataRequired()])
	myChoices1 = ['Rent', 'Sell']
	own_type = SelectField('Asset Ownership Type:', choices = myChoices1, validators = [DataRequired()])
	price = StringField('Asset Price:', validators=[DataRequired()])
	myChoices2 = ['Night', 'Day', 'Month']
	price_dur = SelectField('Asset price:', choices = myChoices2)
	description = TextAreaField('Asset Description:', validators=[DataRequired()])
	thumbnail = FileField('Asset Thumbnail:', validators=[FileAllowed(['jpg', 'png', 'gif'])])
	gallery = FileField('Asset Image Gallery:', validators=[FileAllowed(['jpg', 'png', 'gif'])])
	submit = SubmitField('Add Asset')

class AssetSearch(FlaskForm):
	name = StringField('Name:', validators=[DataRequired()])
	start_price = StringField('Start Price:')
	final_price = StringField('Final Price:')
	myChoices2 = ['Rent-Buy', 'Rent', 'Sell']
	rent_or_buy = SelectField('Asset price:', choices = myChoices2)
	submit = SubmitField('Search')

class SearchAgain(FlaskForm):
	name = StringField('Search:', validators=[DataRequired()])
	submit = SubmitField('Search')

class FilterResults(FlaskForm):
	start_price = IntegerField('Start Price: ')
	final_price = IntegerField('Final Price: ')
	choices = ['Rent', 'Sell']
	own_type = SelectField('Ownership Type:', choices=choices)
	rooms = StringField('Rooms: ')
	submit = SubmitField('Filter')

class EditAssetForm(FlaskForm):
	title = StringField('Asset Title:', validators=[DataRequired(), Length(min=5, max=50)])
	location_1 = StringField('Asset Location:', validators=[DataRequired()])
	location_2 = StringField('Asset Location:', validators=[DataRequired()])
	myChoices1 = ['Rent', 'Sell']
	own_type = SelectField('Asset Ownership Type:', choices = myChoices1, validators = [DataRequired()])
	price = StringField('Asset Price:', validators=[DataRequired()])
	myChoices2 = ['Night', 'Day', 'Month']
	price_dur = SelectField('Asset price:', choices = myChoices2)
	description = TextAreaField('Asset Description:', validators=[DataRequired()])
	thumbnail = FileField('Asset Thumbnail:', validators=[FileAllowed(['jpg', 'png', 'gif'])])
	gallery = FileField('Asset Image Gallery:', validators=[FileAllowed(['jpg', 'png', 'gif'])])
	submit = SubmitField('Edit Asset')

class UpdateAdminAccount(FlaskForm):
	full_name = StringField('Full Name:', validators=[DataRequired(), Length(min=5, max=50)])
	email = StringField('Email:', validators=[DataRequired(), Email()])
	phone = IntegerField('Phone:', validators=[DataRequired()])
	submit = SubmitField('Update')

class UpdateUserAccount(FlaskForm):
	full_name = StringField('Full Name:', validators=[DataRequired(), Length(min=5, max=50)])
	email = StringField('Email:', validators=[DataRequired(), Email()])
	submit = SubmitField('Update')
