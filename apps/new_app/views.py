from django.shortcuts import render, redirect, HttpResponse, 
from .models import *
import bcrypt
from datetime import *

def main(request):
	if 'user' in request.session:
		return redirect('/travels')
	if 'errors' not in request.session:
		request.session['errors'] = {}
	context = request.session['errors']
	request.session.pop('errors')
	return render(request,'new_app/main.html',context)


def registration(request):
	if request.method =="POST":
		form_data = request.POST
		varerror = User.objects.registration(form_data)
		request.session['errors'] = varerror
		if not varerror['boolerror']:
			varuser = User.objects.create_user(form_data)
			request.session['user'] = varuser.id
			return redirect('/travels')
		else:
			return redirect('/')
	return redirect('/')		

def login(request):
	if request.method == "POST":
		form_data = request.POST
		validate = User.objects.validate(form_data)
		if not validate['boolerror']:
			request.session['user'] = validate['user'].id
			return redirect('/travels')
		else:	
			errors = {
				'loginusername':validate['loginusername'],
				'loginpassword':validate['loginpassword'],
				}
			request.session['errors'] = errors
			pass
	return redirect('/')	


def logout(request):
	request.session.flush()
	return redirect('/')

def travels(request):
	if 'user'	 in request.session:
		user = User.objects.filter(id = request.session['user']).first()
		usertrips = Trips.objects.filter(user_id = user.id)
		joined = Joinedtrips.objects.filter(user_id = user.id)
		othertrips = Trips.objects.exclude(user_id = user.id)
		listjoined = []
		for i in joined:
			listjoined.append(i.trip_id)
		print listjoined
		context = {
		'user': user,
		'usertrips': usertrips,
		'joined': joined,
		'othertrips': othertrips,
		'listjoined': listjoined
		}
		return render(request, 'new_app/travels.html', context)
	else:
		return redirect('/')	
		
def addtravel(request):
	error = []
	if 'adderror' in request.session:
		print "went to error", request.session['adderror']
		error = request.session['adderror']
		request.session.pop('adderror')

	context = {
	'errors': error
	}
	
	return render(request,'new_app/addtravel.html', context)

def createtravel(request):
	if request.method == "POST":
		form_data = request.POST
		userid = request.session['user']
		error = Trips.objects.validate_trip(form_data, userid)
		if not error['boolerror']:
			
			return redirect('/travels')
		else:
			request.session['adderror'] = error['error']
			return redirect('travels/add')
	return redirect('travels/add')
		
def join(request,id):
	user = User.objects.filter(id = request.session['user']).first()
	join = Joinedtrips.objects.create(user_id = user.id, trip_id = id)
	return redirect('/travels')

def destination(request,id):
	varid = id
	trips = Trips.objects.filter(id = varid).first()
	joined = Joinedtrips.objects.filter(trip_id = varid)
	# joined = Joinedtrips.objects.raw("select j.id  from new_app_joinedtrips as j join new_app_trips as t on j.trip_id = t.id on")
	context = {
	'trips': trips,
	'joined': joined
	}
	return render(request,'new_app/destination.html',context)
