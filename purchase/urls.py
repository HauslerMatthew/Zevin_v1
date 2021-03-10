from django.urls import path
from . import views

urlpatterns = [
    path('', views.merch),
    path('addtocart/<int:merch_id>', views.add_to_cart),
    path('clearsession', views.clearsession),
    path('cart', views.cart),
    path('remove_item/<int:cart_item_id>', views.remove_from_cart),
    path('checkout/<int:cart_id>', views.checkout),
    # path('checkout/<int:cart_id>/process_order', views.process_order),
    #need paths to empty cart and cancel order
]