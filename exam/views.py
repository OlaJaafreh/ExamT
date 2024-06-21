from django.shortcuts import render ,redirect
from .models import Users , Dashboard
import bcrypt
from django.contrib import messages

def loginPage(request):
    return render(request,'login.html')


def login(request):
    email = request.POST['emailLog']
    password = request.POST['pass']
    user = Users.objects.filter(email=email)
    if user:
        logged_user = user[0] 
        if bcrypt.checkpw(password.encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect("dashboard")
        else:
            messages.error(request, 'Incorrect User name or Password')
    else:
        messages.error(request, 'Incorrect User name or Password')
    return redirect('loginPage')


def register(request):
    errors = Users.objects.basic_validator(request.POST)
    if len(errors) > 0:
        messages.error(request, 'Registration failed.')
        return render(request,'login.html', {'errors': errors})
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        Users.objects.create(first_name=first_name,last_name=last_name,email=email,password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode())
        messages.success(request, 'Registration successful. You can now log in.')
        return render(request ,"login.html")
    
def dashboard(request):
    user = Users.objects.get(id = request.session['userid'])
    dash = Dashboard.objects.all()
    return render(request,'dashboard.html',{'user':user,'trips':dash})


def new(request):
    user = Users.objects.get(id= request.session['userid'])
    return render(request,'newTrip.html',{'user':user})

def newTrip(request):

    errors = Dashboard.objects.basic_validator(request.POST, is_edit=False)
    if len(errors) > 0:
        messages.error(request, 'Failed.')
        return render(request,'newTrip.html', {'errors': errors})
    else:
        des = request.POST['destination']
        startDay = request.POST['startDay']
        endDay = request.POST['endDay']
        itinerary = request.POST['itinerary']
        user = Users.objects.get(id= request.session['userid'])
        trip = Dashboard.objects.create(destination = des , itinerary = itinerary , startDay = startDay , endDay = endDay,organizer = user)
        # trip.traveler.add(user)
        # messages.success(request, 'Successful. New Trip added')
        return redirect('new')

def joinTrip(request,Tid):
        user = Users.objects.get(id= request.session['userid'])
        trip = Dashboard.objects.get(id = Tid)
        trip.traveler.add(user)
        # messages.success(request, 'Successful. New Trip added')
        return redirect('myTrips')

def cancelTrip(request,Tid):
    user = Users.objects.get(id=request.session['userid'])
    trip = Dashboard.objects.get(id=Tid)
    if user in trip.traveler.all():
        trip.traveler.remove(user)
        trip.save()
    # traveler.delete()
    return redirect('myTrips')
    

def edit(request,Tid):
    dash = Dashboard.objects.get(id = Tid)
    user = Users.objects.get(id= request.session['userid'])
    return render(request,'editTrip.html',{'trip':dash,'user':user})

def editTrip(request,Tid):
    dash = Dashboard.objects.get(id = Tid)
    if request.method == "POST":
        errors = Dashboard.objects.basic_validator(request.POST, is_edit=True)
        if errors:
            messages.error(request, 'Failed.')
            return render(request,'editTrip.html', {'errors': errors , 'trip':dash})
        else:
            des = request.POST['Edestination']
            startDay = request.POST['EstartDay']
            endDay = request.POST['EendDay']
            itinerary = request.POST['Eitinerary']
            
            dash.destination = des
            dash.startDay = startDay
            dash.endDay = endDay
            dash.itinerary = itinerary
            dash.save()
            messages.success(request, 'Successful. Trip edited')
            return redirect('edit',Tid)
    else:
        return redirect('edit',Tid)
    
def deleteTrip(request,Tid):
    # user = Users.objects.get(id=request.session['userid'])
    dash = Dashboard.objects.get(id = Tid)
    dash.delete()
    return redirect('dashboard')

def details(request,Tid):
    user = Users.objects.get(id= request.session['userid'])
    dash = Dashboard.objects.get(id = Tid)
    return render(request,'details.html',{'trip':dash,'user':user})

def myTrips(request):
    user = Users.objects.get(id= request.session['userid'])
    dash = Dashboard.objects.all
    return render(request,'myTrip.html',{'trips':dash,'user':user})