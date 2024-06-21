from django.db import models
import re
from datetime import date

class UsersManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        Name_REGEX = re.compile(r'^[a-zA-Z]+$')
        if len(postData['first_name']) <= 2 or not Name_REGEX.match(postData['first_name']):
            errors["first_name"] = "First name should be at least 2 characters"
            
        if len(postData['last_name']) <= 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if self.filter(email=postData['email']).exists():
            errors['email'] = "Email already exists. Please use a different email address."

        if not EMAIL_REGEX.match(postData['email']):   
            errors['email'] = "Invalid email address!"

        if len(postData['password']) <= 8:
            errors["password"] = "password should be at least 8 characters"

        if  postData['password'] != postData['Confirmpassword']:
            errors["Confirmpassword"] = "password didnt match"

        return errors
    

class DashManager(models.Manager):
    def basic_validator(self, postData, is_edit=False):
        errors = {}
        if not is_edit:
            if len(postData['destination']) <= 2 :
                errors["destination"] = "Destination should be at least 2 characters"
                
            if len(postData['itinerary']) > 50 :
                errors["itinerary"] = "itinerary should not be more than 50 characters"

            if date.fromisoformat(postData['startDay']) < date.today() :
                errors["startDay"] = "start Day should not be in a future"

            if postData['endDay'] < postData.get('startDay') :
                errors["endDay"] = "End Day should not be before start day"

        
        else:
            if len(postData['Edestination']) <= 2 :
                errors["Edestination"] = "Destination should be at least 2 characters"
                
            if len(postData['Eitinerary']) > 50 :
                errors["Eitinerary"] = "itinerary should not be more than 50 characters"

            if date.fromisoformat(postData['EstartDay']) < date.today() :
                errors["EstartDay"] = "start Day should not be in a future"

            if postData['EendDay'] < postData.get('EstartDay') :
                errors["EendDay"] = "End Day should not be before start day"
            

        return errors
    

class Users(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    objects = UsersManager()


class Dashboard(models.Model):
    traveler = models.ManyToManyField(Users,related_name='traveler')
    destination = models.TextField()
    organizer = models.ForeignKey(Users,related_name='organizer',on_delete=models.CASCADE)
    startDay = models.DateField()
    endDay = models.DateField()
    itinerary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    objects = DashManager()

