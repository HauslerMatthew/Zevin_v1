from django.db import models
import re

class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]{2,3}$')
        if (post_data['first_name'] == "" or post_data['last_name'] == "" or post_data['email'] == "" or post_data['password'] == ""):
            errors["req_field"] = "***All fields required***"
        if not EMAIL_REGEX.match(post_data['email']):
            errors['valid-email'] = "***Invalid email address format***"
        try:
            User.objects.get(email = post_data['email'])
            errors['email_taken'] = "***email address already in use***"
        except:
            pass
        if (len(post_data['password']) < 8):
            errors['password_length'] = "***Password must be at least 8 characters***"
        if (post_data['password'] != post_data['confirm_password']):
            errors['password_match'] = "***Passwords do not match. Be careful when you type***"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    mailing_list = models.BooleanField(default = False)
    #add permissions? i.e. admin capabilities?
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Shipping_AddressManager(models.Manager):
    def address_validator(self, post_data):
        errors = {}

        if (post_data['street'] == "" or post_data['city'] == "" or post_data['state'] == "" or post_data['zip_code'] == ""):
            errors["req_field"] = "***Please complete all address fields***" 
        if (len(post_data['zip_code']) != 5):
            errors["5_digit_zip"] = "***Please enter a valid 5-digit zip code***"
        return errors

class Shipping_Address(models.Model):
    street = models.CharField(max_length = 255)
    street_optional = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    state = models.CharField(max_length = 255)
    zip_code = models.IntegerField()
    user_id = models.ManyToManyField(User, related_name="shipping_addresses")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = Shipping_AddressManager()
