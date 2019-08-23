from django.db import models
from datetime import datetime
import re

# Create your models here.
class UserManager(models.Manager) :
    def validator(self, postData) :
        errors = {}
        first_name = postData['first_name']
        # first name & last_anme >=2 characters
        if (len(first_name) == 0) :
            errors['first_name'] = "First name is required"
        elif (len(first_name) < 2) :
            errors['first_name'] = "First name should be at least 2 characters"

        last_name = postData['last_name']
        if (len(last_name) == 0) :
            errors['last_name'] = "Last name is required"
        elif (len(last_name) < 2) :
            errors['last_name'] = "Last name should be at least 2 characters"

        # email should be valid
        email = postData['email']
        if (len(email) == 0) :
            errors['email'] = "Email is required"
        else :
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-z]+$')
            if not EMAIL_REGEX.match(email) :
                errors['email'] = "Email should be valid"
            else : # check uniqueness
                users = User.objects.filter(email=email)
                if (len(users) > 0) :
                    errors['email'] = "Email already exists!"

        # password should be at least 8 characters
        password = postData['password']
        if (len(password) < 8) :
            errors['password'] = "Password should be at least 8 characters"
        
            # hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        else :
            # password should match
            confirm_pw = postData['confirm_password']
            if (not password == confirm_pw) :
                errors['confirm_password'] = "Password should match!"

        return errors

class User(models.Model) :
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class TripManager(models.Manager) :
    def validator(self, postData) :
        errors = {}
        
        # destination
        destination = postData['destination']
        # destination >=3 characters
        if (len(destination) == 0) :
            errors['destination'] = "Destination must be provided"
        elif (len(destination) < 3) :
            errors['destination'] = "Destination should be at least 3 characters"

        # start_date
        start_date = postData['start_date']
        if (len(start_date) == 0) :
            errors['start_date'] = "Start date must be provided"
        else :
            try : 
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                if (start_date <= datetime.now()) : # startdate in the past
                    errors['start_date'] = "Start date should be in the future (from tomorrw)"
            except : # any errors from try
                errors['start_date'] = "Start date should be a valid date"

        # end_date
        end_date = postData['end_date']
        if (len(end_date) == 0) :
            errors['end_date'] = "End date must be provided"
        else :
            try :
                # start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                # check if end_date is after start_date
                if (end_date < start_date) : 
                    errors['end_date'] = "End date should be after the start date (can be same day)"
            except : 
                errors['end_date'] = "End date should be a valid date"
        
        # plan
        plan = postData['plan']
        # plan >=3 characters
        if (len(plan) == 0) :
            errors['plan'] = "Plan must be provided"
        elif (len(plan) < 3) :
            errors['plan'] = "Plan should be at least 3 characters"


        return errors

class Trip(models.Model) :
    destination = models.CharField(max_length=255)
    plan = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    user_created = models.ForeignKey(User, related_name="trips_created")
    users_joined = models.ManyToManyField(User, related_name="trips_joined")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()