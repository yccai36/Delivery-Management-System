from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('submit/', views.form, name='form'),

]