from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Shipping_Address
from purchase.models import Cart
import bcrypt

def login(request):
    return render(request, "merch_login.html")

def validate_registration(request):
    regerrors = User.objects.registration_validator(request.POST)
    adderrors = Shipping_Address.objects.address_validator(request.POST)

    if (regerrors):
        for key, value in regerrors.items():
            messages.error(request, value)
        return redirect('/login')
    if (adderrors):
        for key, value in adderrors.items():
            messages.error(request, value)
        return redirect('/login')

    password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=password_hash,
        mailing_list=request.POST['mailing_list'],
    )
    address = Shipping_Address.objects.create(
        street = request.POST['street'],
        street_optional = request.POST['street_optional'],
        city = request.POST['city'],
        state = request.POST['state'],
        zip_code = request.POST['zip_code'],
    )
    address.user_id.add(user.id)
    address.save()
    request.session['user_id'] = user.id
    request.session['user_name'] = user.first_name
    #associates any existing cart with the user that just registered
    if 'current_cart_id' in request.session:
        current_cart = Cart.objects.get(id=request.session['current_cart_id'])
        current_cart.user = user

    return redirect('/merch')

def validate_login(request):
    try:
        user = User.objects.get(email = request.POST['email'])
    except:
        messages.error(request, "email or password is incorrect")
        return redirect('/login')
    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request, "email or password is incorrect")
        return redirect('/login')
    request.session['user_id'] = user.id
    request.session['user_name'] = user.first_name
    #associates any existing cart with the user that just logged in
    if 'current_cart_id' in request.session:
        current_cart = Cart.objects.get(id=request.session['current_cart_id'])
        user = User.objects.get(id=request.session['user_id'])
        current_cart.user = user
    
    active_user = User.objects.get(id=request.session['user_id'])
    past_cart = Cart.objects.filter(user=active_user.id)
    if past_cart.count() > 0:
        current_cart = past_cart
        request.session['current_cart_id'] = current_cart.id

    return redirect('/merch')

def logout(request):
    del request.session['user_id']
    del request.session['user_name']
    if 'current_cart_id' in request.session:
        del request.session['current_cart_id']
    return redirect('/')