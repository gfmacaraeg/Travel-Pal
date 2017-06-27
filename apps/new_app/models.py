from __future__ import unicode_literals

from django.db import models
import re
class UserManager(models.Manager):
	def registration(self, form_data):
		name =[]
		alias =[]
		email =[]
		password = []
		confirm =[]
		if len(form_data['name'] ) < 2:
			name.append('*Name cannot be less than 2 characters')
		if len(form_data['alias'] )< 2:
			alias.append('*Alias cannot be less than 2 characters')
		if not re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)' , form_data['email']):
			email.append('*That is not a valid email format')
		if len(form_data['password'] )== 0:
			password.append('*Password is required')
		if len(form_data['password'] )< 8:
			password.append('*Password must be at least 8 characters')
		if form_data['password'] != form_data['confirm']:
			confirm.append('*Password doesn\'t match')
		errors = {
		'name':name,
		'alias':alias,
		'email':email,
		'password':password,
		'confirm':confirm,
		}
		return errors

	def validate(self,form_data):
		email =[]
		password = []
		if len(form_data['email']) == 0:
			email.append('*Email cannot be blank')
		if len(form_data['password']) == 0:
			password.append('*Password cannot be blank')
		errors = {
		'loginemail':email,
		'loginpassword':password,
		}
		return errors

class  User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.EmailField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()


class Books(models.Model):
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	user = models.ForeignKey(User,related_name ="userbooks", on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Reviews(models.Model):
	user = models.ForeignKey(User,related_name ="userreviews", on_delete=models.CASCADE)
	book = models.ForeignKey(Books,related_name ="bookreviews", on_delete=models.CASCADE)
	content = models.TextField()
	rating = models.CharField(max_length=5)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


