from django.shortcuts import render, HttpResponse, redirect
from apps.trip_buddy_app.models import *
from django.contrib import messages
import bcrypt

# html 1 - index (login)
def index(request):
    return render(request, 'trip_buddy_app/index.html')
    # return HttpResponse("login pate")

# html 2 - dashboard
def dashboard(request) :
    # TODO - enable below logic (only logged in user)
    if not 'user_id' in request.session :
        return redirect('/')
    # current user
    user = User.objects.get(id=request.session['user_id'])
    my_trips_created = user.trips_created.all().order_by('created_at')
    my_trips_all = user.trips_joined.all().order_by('created_at')
    # my_trips = Trip.objects.filter(user_created=user).all()
    all_trips = Trip.objects.all()
    context = {"my_trips_created" : my_trips_created,
            "my_trips_all": my_trips_all,
            "all_trips" : all_trips,
            "cur_user" : user
            }
    return render(request, 'trip_buddy_app/dashboard.html', context)

# html 3 - edit
def edit_trip(request, trip_id) :
    # TODO - enable below logic (only logged in user)
    if not 'user_id' in request.session :
        return redirect('/')
    trip = Trip.objects.get(id=trip_id)
    context = {"trip":trip}
    return render(request, 'trip_buddy_app/edit.html', context)

# html 4 - add a new trip
def new_trip(request) :
    # TODO - enable below logic (only logged in user)
    if not 'user_id' in request.session :
        return redirect('/')
    context = {}
    return render(request, 'trip_buddy_app/new.html', context)

# html 5 - view trip detail
def view_trip(request, trip_id) :
    # TODO - enable below logic (only logged in user)
    if not 'user_id' in request.session :
        return redirect('/')
    trip = Trip.objects.get(id=trip_id)
    cur_user = User.objects.get(id=request.session['user_id'])
    context = {"trip":trip,
                "cur_user":cur_user
            }
    return render(request, 'trip_buddy_app/trip.html', context)


# method 1 - register (from login page)
def register(request) :
    errors = User.objects.validator(request.POST)
    if (len(errors) > 0) :
        for key, value in errors.items():
            # messages.error(request, value)
            messages.add_message(request, messages.ERROR, value, extra_tags='register')
        # messages.error(request, errors)
        temp_inputs={"first_name":request.POST['first_name'],
                    "last_name":request.POST['last_name'],
                    "email":request.POST['email']}
        request.session['temp_inputs'] = temp_inputs
        return redirect('/')
        
    else :
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name=request.POST['first_name'], 
                            last_name=request.POST['last_name'],
                                email=request.POST['email'], 
                                password=hashed_pw)
        messages.success(request, "User succesfully registered")
        request.session['user_id'] = user.id
        request.session['user_fname'] = user.first_name
        return redirect('/dashboard')


# method 2 - login
def login(request) :
    print ("--request.method : ", request.method)
    print ("--request.post : ", request.POST)
    email = request.POST['login_email']
    try :
        user = User.objects.get(email=email)
        if bcrypt.checkpw(request.POST['login_pw'].encode(), user.password.encode()) :
            # print ("here")
            request.session['user_id'] = user.id
            request.session['user_fname'] = user.first_name
            messages.add_message(request, messages.SUCCESS, 'Successfully logged in!')
            return redirect('/dashboard')
        else :
            messages.add_message(request, messages.ERROR, 'Invalid user information - not correct password', extra_tags='login')
    except :
        messages.add_message(request, messages.ERROR, 'Invalid user information', extra_tags='login')
    return redirect('/')

# method 3 - logout
def logout(request) :
    request.session.clear()
    return redirect('/')

# method 4 - delete a trip (from dashboard link)
def delete_trip(request, trip_id) :
    # pass
    trip = Trip.objects.get(id=trip_id)
    trip.delete()
    return redirect('/dashboard')

# method 5.1 - join the trip
def join_trip(request, trip_id) :
    user = User.objects.get(id=request.session['user_id'])
    user.trips_joined.add(Trip.objects.get(id=trip_id))

    return redirect('/dashboard')

# method 5.2 - cancel the trip
def cancel_trip(request, trip_id) :
    user = User.objects.get(id=request.session['user_id'])
    user.trips_joined.remove(Trip.objects.get(id=trip_id))
    return redirect('/dashboard')


# method 7 - create a new trip
def create_trip(request) :
    print ("--request.method : ", request.method)
    print ("--request.post : ", request.POST)

    # validate request
    errors = Trip.objects.validator(request.POST)
    # user error message extra tag - create_trip
    if (len(errors) > 0) :
        for key, value in errors.items():
            messages.add_message(request, messages.ERROR, value, extra_tags='create_trip')
        # save input values
        temp_inputs = {"destination" : request.POST['destination'],
                        "plan" : request.POST['plan'],
                        "start_date" :request.POST['start_date'],
                        "end_date" : request.POST['end_date']
                    }
        request.session['temp_inputs'] = temp_inputs
        return redirect('/trips/new')
    else :
        # create a new trip
        user = User.objects.get(id=request.session['user_id'])
        trip = Trip.objects.create(destination=request.POST['destination'],
                                    plan=request.POST['plan'],
                                    start_date=request.POST['start_date'],
                                    end_date=request.POST['end_date'],
                                    user_created=user
                                    )
        trip.users_joined.add(user)
        return redirect('/dashboard')

# method 6 - edit trip information
def edit_trip_edit(request, trip_id) :
    # validate request
    errors = Trip.objects.validator(request.POST)
    # user error message extra tag - create_trip
    if (len(errors) > 0) :
        for key, value in errors.items():
            messages.add_message(request, messages.ERROR, value, extra_tags='edit_trip')
        # save input values
        temp_inputs = {"destination" : request.POST['destination'],
                        "plan" : request.POST['plan'],
                        "start_date" :request.POST['start_date'],
                        "end_date" : request.POST['end_date']
                    }
        request.session['temp_inputs'] = temp_inputs
        return redirect(f'/trips/edit/{trip_id}')
    else :
        # create a new trip
        user = User.objects.get(id=request.session['user_id'])
        trip = Trip.objects.get(id=trip_id)
        trip.destination = request.POST['destination']
        trip.plan = request.POST['plan']
        trip.start_date = request.POST['start_date']
        trip.end_date = request.POST['end_date']
        trip.save()
        # trip.users_joined.add(user)
        return redirect('/dashboard')
