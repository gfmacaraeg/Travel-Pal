from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import *
class UserManager(models.Manager):
	def registration(self, form_data):
		name =[]
		username =[]
		password = []
		confirm =[]
		boolerror = False

		if len(form_data['name'] ) < 4:
			name.append('*Name cannot be less than 4 characters')
			boolerror = True
		if len(form_data['username'] )< 4:
			username.append('*Username cannot be less than 4 characters')
			boolerror = True
		# if not re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)' , form_data['username']):
		# 	username.append('*That is not a valid username format')
		# 	boolerror = True
		duplicate = User.objects.filter(username = form_data['username']).first()
		if duplicate:
			username.append("That username has already been registered")
			boolerror = True
		if len(form_data['password'] ) == 0:
			password.append('*Password is required')
			boolerror = True
		if len(form_data['password'] ) < 8:
			password.append('*Password must be at least 8 characters')
			boolerror = True
		if form_data['password'] != form_data['confirm']:
			confirm.append('*Password doesn\'t match')
			boolerror = True
		errors = {
		'name':name,
		'username':username,
		'password':password,
		'confirm':confirm,
		'boolerror':boolerror,
		}
		return errors

	def validate(self,form_data):
		username =[]
		password = []
		boolerror = False
		if len(form_data['username']) == 0:
			username.append('*username cannot be blank')
			boolerror = True
		if len(form_data['password']) == 0:
			password.append('*Password cannot be blank')
			boolerror = True
		varlogin = User.objects.filter(username=form_data['username']).first()
		if varlogin:
			userpassword = str(form_data['password'])
			db_password = str(varlogin.password)
			hashed_pw = bcrypt.hashpw(userpassword, db_password)
			if hashed_pw == db_password:
				boolerror = False
			else:
				password.append("*Password doesn't match our records")
				boolerror = True
		else:
			username.append("*username does not match our records")
			boolerror = True	
		errors = {
		'loginusername':username,
		'loginpassword':password,
		'boolerror':boolerror,
		'user': varlogin
		}
		return errors

	def create_user(self,form_data):
		password = str(form_data['password'])
		hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
		varuser = User.objects.create(name = form_data['name'],
						 username = form_data['username'],
						 password = hashed_pw)
		return varuser

class  User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	objects = UserManager()


class TripsManager(models.Manager):
	def validate_trip(self, form_data, userid):
		error = []
		boolerror = False
		if len(form_data['destination']) == 0:
			error.append('*Destination cannot be blank')
			boolerror = True
		if len(form_data['description']) == 0:
			error.append('*Description cannot be blank')
			boolerror = True
		if len(form_data['travel_start']) == 0:
			error.append('*Travel date from cannot be blank')
			boolerror = True
		if len(form_data['travel_end']) == 0:
			error.append('*Travel date to cannot be blank')
			boolerror = True
		try:
			if datetime.strptime(form_data['travel_start'], "%Y-%m-%d") > datetime.strptime(form_data['travel_end'], "%Y-%m-%d"):
				error.append('*Travel date from canot be greater than travel date to')
				boolerror = True
		except:
			error.append('*Enter a vaild Date format')
			boolerror = True
		if not boolerror:
			
			varuser = User.objects.filter(id = userid).first()
			if varuser:
				vartrips = Trips.objects.create(destination = form_data['destination'],
							description = form_data['description'],
							travel_start = form_data['travel_start'],
							travel_end = form_data['travel_end'],
							user_id = varuser.id
							)
			else:
				error.append("*Failed to register trip")
				boolerror = True
		errors = {
		'error':error,
		'boolerror':boolerror,
		}
		return errors

class Trips(models.Model):
	destination = models.CharField(max_length=255)
	description = models.TextField()
	travel_start = models.DateField()
	travel_end = models.DateField()
	user = models.ForeignKey(User,related_name ="usertrips", on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	objects = TripsManager()

class Joinedtrips(models.Model):
	user = models.ForeignKey(User,related_name = 'userjoined',on_delete=models.CASCADE)
	trip = models.ForeignKey(Trips,related_name = 'tripsjoined',on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)



