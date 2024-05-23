from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('', adminlogin, name='adminlogin'),
    path('adminlogout/', adminlogout, name='adminlogout'),
    path('addtrain/', addtrain, name='addtrain'),
    path('deletetrain/<str:train_no>', deletetrain, name='deletetrain'),
    path('update/<str:train_no>/', update, name='update'),
    path('canceltrain/',canceltrain, name='canceltrain'),
    path('trainslist/',trainslist, name='trainslist'),
    
]