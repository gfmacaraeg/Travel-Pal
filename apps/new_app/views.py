from django.shortcuts import render, redirect
from .models import *
import bcrypt
def index(request):
	if 'user' in request.session:
		return redirect('/books')
	if 'errors' not in request.session:
		request.session['errors'] = {}
	context = request.session['errors']

	return render(request,'new_app/index.html',context)

def registration(request):
	if request.method =="POST":

		form_data = request.POST
		x = User.objects.registration(form_data)
		request.session['errors'] = x
		print "This is value of x", x
		duplicate = User.objects.filter(email = form_data['email'])
		if duplicate:
			x['email'].append("That email has already been registered")
		
		if x['name'] == [] and x['password'] == [] and x['email'] == [] and x['confirm'] == []:
			password = str(form_data['password'])
			hashed_pw = bcrypt.hashpw(password,bcrypt.gensalt())
			y = User.objects.create(name = form_data['name'], alias = form_data['alias'], email = form_data['email'], password = hashed_pw)
			request.session['user'] = y.id
			return redirect('/books')
		else:
			return redirect('/')
	
def login(request):
	if request.method == "POST":
		form_data = request.POST
		x=User.objects.validate(form_data)
		if x['loginpassword'] == [] and x['loginemail'] == []:
			varlogin = User.objects.filter(email=form_data['email']).first()
			if varlogin:
				password = str(form_data['password'])
				db_password = str(varlogin.password)
				hashed_pw = bcrypt.hashpw(password, db_password)
				if hashed_pw == db_password:
					request.session['user'] = varlogin.id
					return redirect('/books')
				else:
					x['loginpassword'].append("Login or Password doesn't match our records")
					request.session['errors'] = x
					return redirect('/')
			else:	
				x['loginpassword'].append("Login or Password doesn't match our records")
				request.session['errors'] = x
				return redirect('/')		
		else:	
			x['loginpassword'].append("Login or Password doesn't match our records")
			request.session['errors'] = x
			return redirect('/')
	# else:	
	# 	return redirect('/')	

def books(request):
	if 'user'	 in request.session:
		user = User.objects.filter(id = request.session['user']).first()
		# allbooks = Books.objects.raw("select * from new_app_books as b join new_app_reviews as r on b.id = r.book_id join new_app_user as u on r.user_id = u.id order by r.created_at desc limit 3")
		allbooks = Books.objects.raw("select * from new_app_reviews as r left join new_app_books as b on r.book_id = b.id left join new_app_user u on r.user_id = u.id order by r.created_at desc limit 3")
		allbooks2 = Books.objects.raw("select * from new_app_books as b join new_app_reviews as r on b.id = r.book_id join new_app_user as u on r.user_id = u.id")
		context = {
		'first_name': user.name,
		'booklist': allbooks,
		'star': "12345",
		'allbooks':allbooks2
		}
	return render(request, 'new_app/books.html', context)

def logout(request):
	request.session.flush()
	return redirect('/')

def addbook(request):
	x = Books.objects.raw("select id,  author from new_app_books group by author")
	authors = []
	for some in x:
		authors.append(some.author)
		print some.author
	
	context ={
	'authorlist': authors,
	}

	return render(request,'new_app/add.html', context)

def registerbook(request):
	if request.method == "POST":
		print "this is author1", request.POST['author1']
		print "this is author2", request.POST['author2']
		if request.POST['author1'] == "None":
			author = request.POST['author2']
		else:
			author = request.POST['author1']	
		x = Books.objects.create(title = request.POST['title'], author= author, user_id = request.session['user'])
		y = Reviews.objects.create(user_id=x.user_id, book_id = x.id, rating = request.POST['rating'], content = request.POST['contentreview'])
		request.session['book'] = x.id
	return redirect('/books/999999')

def showbooks(request,id):
	if 'user'	 in request.session:
		# book = Books.objects.raw("select * from new_app_books as b join new_app_reviews as r on b.id = r.book_id join new_app_user as u on r.user_id = u.id where b.id = %s",[id])
		if id == "999999":
			id = request.session['book']
			request.session.pop('book')
		book = Books.objects.filter(id=id).first()
		user = User.objects.filter(id = request.session['user']).first()
		print "This is the value of book", book
		varbook = book.id
		review = Reviews.objects.raw("select * from new_app_reviews as r left join new_app_books as b on r.book_id = b.id left join new_app_user u on r.user_id = u.id where b.id = %s", [varbook])
		reviewed = []
		for i in review:
			reviewed.append(i.user_id)
		context ={
		'bookresult':book,
		'review': review,
		'star': "12345",
		'reviewed':reviewed,
		}
	return render(request,'new_app/showbook.html', context)

def registerbookshow(request,id):
	if request.method == "POST":
		request.session['book'] = id
		user = User.objects.filter(id=request.session['user']).first()
		varx = Reviews.objects.create(user_id = user.id, book_id = id, content = request.POST['contentreview'], rating = request.POST['rating'])
		return redirect('/books/999999')

def delete(request,id):
	varuser = Reviews.objects.filter(id= id).first()
	print varuser
	if str(request.session['user']) == str(varuser.user_id):
		varuser.delete()
		request.session['book'] = varuser.book_id
	return redirect('/books/999999')


def users(request, id):
	user = User.objects.filter(id=id).first()
	x = Reviews.objects.raw("select b.id, b.title from new_app_reviews as r left join new_app_books as b on r.book_id = b.id left join new_app_user u on b.user_id = u.id where r.user_id = %s group by b.title", [id])
	count = Reviews.objects.raw("select r.id, count(content) as total from new_app_reviews as r where r.user_id = %s", [id])
	context = {
	'user': user,
	'booksreviewed': x,
	'count': count
	}
	return render(request,'new_app/users.html',context)






