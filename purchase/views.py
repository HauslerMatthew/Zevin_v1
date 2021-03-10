from django.shortcuts import render, redirect
from .models import Cart, Merch, CartItem
from django.contrib import messages
from login.models import User

# Create your views here.
def merch(request):
    if 'current_cart_id' in request.session:
        this_cart = Cart.objects.get(id=request.session['current_cart_id'])
        context = {
            "cart" : this_cart.cart_items.all()
        }
    else:
        context = {}
    return render(request, "merch.html", context)

def add_to_cart(request, merch_id):
    if not "current_cart_id" in request.session:
        new_cart = Cart.objects.create()
        if "user_id" in request.session:
            active_user = User.objects.get(id=request.session['user_id'])
            new_cart.user = active_user
            print(f"active user is {active_user}, new cart is {new_cart}, new cart's active user is {new_cart.user}")
        request.session['current_cart_id'] = new_cart.id
    item_to_add = Merch.objects.get(id=merch_id)
    this_cart = Cart.objects.get(id=request.session['current_cart_id'])
    CartItem.objects.create(merch_item=item_to_add, cart=this_cart)
    messages.success(request, 'Item successfully added to cart!')
    return redirect("/merch")

def remove_from_cart(request, cart_item_id):
    item_to_delete = CartItem.objects.get(id=cart_item_id)
    item_to_delete.delete()
    return redirect('/merch/cart')

def cart(request):
    # if 'user_id' in request.session:
    #     active_user = User.objects.get(id=request.session['user_id'])
    #     if Cart.objects.filter(user=active_user).count() > 1:
    #         print("this user has some carts boiii")

    if 'current_cart_id' in request.session:
        this_cart = Cart.objects.get(id=request.session['current_cart_id'])
        cart = this_cart.cart_items.all()
        total_price = 0
        for item in cart:
            total_price += item.merch_item.price
        tax = round(total_price/10, 2)
        context = {
            "cart" : this_cart.cart_items.all(),
            "cart_id" : this_cart.id,
            "total_price" : total_price,
            "tax" : tax,
            "subtotal" : total_price + tax
        }
    else:
        context = {}
    return render(request, "cart.html", context)

def checkout(request, cart_id):
    this_cart = Cart.objects.get(id=request.session['current_cart_id'])
    cart = this_cart.cart_items.all()
    total_price = 0
    shipping = 6.99
    for item in cart:
        total_price += item.merch_item.price
    tax = round(total_price/10, 2)
    grand_total = float(total_price) + float(tax) + float(shipping)
    context = {
        "cart" : this_cart.cart_items.all(),
        "cart_id" : this_cart.id,
        "total_price" : total_price,
        "tax" : tax,
        "subtotal" : total_price + tax,
        "grand_total" : grand_total
    }
    return render(request, "checkout.html", context)

# def process_order(request):
#     return redirect("/confirmation") #Fix this redirect

def confirmation(request):
    return render(request, "order_confirmation.html")

def clearsession(request):
    request.session.clear()
    return redirect('/merch/cart')