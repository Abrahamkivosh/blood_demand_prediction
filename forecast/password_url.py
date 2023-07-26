# urls.py

from django.urls import path
from . import passwordViews as views

# app_name = 'forecast'
urlpatterns = [
    # Other URL patterns...
    path('password_reset/', views.password_reset_index, name='password_reset'),
    path('password_reset/request/', views.password_reset_request, name='password_reset_request'),
    path('reset', views.password_reset_confirm, name='password_reset_confirm'),
   
]
