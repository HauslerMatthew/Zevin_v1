from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('validate_registration', views.validate_registration),
    path('validate_login', views.validate_login),
    path('logout', views.logout)
]