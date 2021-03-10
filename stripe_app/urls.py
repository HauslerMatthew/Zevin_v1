from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('confirmation/', views.confirmation),
]