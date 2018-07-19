from django.db import models
from apps.book_manager_app.models import *

class UserManager(models.Manager):
    def login_validator(self, postData):
        errors = {}
        user = self.filter(email=postData['email'])
        if len(user) > 0:
            print("email matched")
            import bcrypt
            user = user[0]
            print(user.first_name)
            if bcrypt.checkpw(postData['password'].encode(), user.hashed_password.encode()):
                print("password matched")
            else:
                errors["login"] = "User could not be logged in."
        else:
            errors["login"] = "User could not be logged in."
            print("failed email")
        return errors

    def register_validator(self, postData):
        errors = {}
        import re
        name_pattern = re.compile(r'^[a-zA-Z]*(-[a-zA-Z]*)?$')
        email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        email_query = self.filter(email=postData['email'])
        if len(postData['first_name']) < 1:
            errors['first_name'] = "First name field is required"
        elif not name_pattern.match(postData['first_name']):
            errors['first_name'] = "Invalid first name"
        if len(postData['last_name']) < 1:
            errors['last_name'] = "Last name field is required"
        elif not name_pattern.match(postData['last_name']):
            errors['last_name'] = "Invalid last name"
        if len(postData['email']) < 1:
            errors['email'] = "Email field is required"
        elif not email_pattern.match(postData['email']):
            errors['email'] = "Invalid email"
        elif len(email_query) > 0:
            errors['email'] = "Email is already taken"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        elif postData['password'] != postData['password_cf']:
            errors['password'] = "Passwords must match"
        return errors




class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    hashed_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def fullname(self):
        return self.first_name + " " + self.last_name
    
    def total_reviews(self):
        reviews = self.reviews.all()
        return len(reviews)

    objects = UserManager()
