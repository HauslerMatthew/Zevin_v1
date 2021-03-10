from django.db import models
from login.models import User, Shipping_Address

class Billing_AddressManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if (post_data['street'] == "" or post_data['city'] == "" or post_data['state'] == "" or post_data['zip_code'] == ""):
            errors["req_field"] = "Star indicates required field" #Make sure to actually include stars on the form
        if (len(post_data['zip_code']) != 5):
            errors["5_digit_zip"] = "Please enter a valid 5-digit zip code"
        return errors

class Billing_Address(models.Model):
    street = models.CharField(max_length = 255)
    street_optional = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    state = models.CharField(max_length = 255)
    zip_code = models.IntegerField()
    same_as_shipping = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = Billing_AddressManager()

class Merch(models.Model):
    name = models.CharField(max_length = 255)
    size = models.CharField(max_length = 255, default = "small") #only relevant for apparel, set some generic default for audio product
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

#Definitely need a Credit_CardManager

class Credit_Card(models.Model):
    number = models.BigIntegerField()
    cvv = models.IntegerField()
    exp = models.CharField(max_length = 10)
    user_id = models.ForeignKey(User, related_name="credit_cards", on_delete = models.CASCADE)
    billing_address = models.ForeignKey(Billing_Address, related_name="credit_cards", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Cart(models.Model):
    user = models.ForeignKey(User, related_name="cart", null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class CartItem(models.Model):
    merch_item = models.ForeignKey(Merch, related_name="cart_items", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Order(models.Model):
    user_id = models.ForeignKey(User, related_name="orders", on_delete = models.CASCADE)
    shipping_address = models.ForeignKey(Shipping_Address, related_name = "orders", on_delete = models.CASCADE)
    cart_id = models.ForeignKey(Cart, related_name="order_id", on_delete = models.CASCADE)
    credit_card = models.ForeignKey(Credit_Card, related_name="orders", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)