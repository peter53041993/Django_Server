from django.contrib import admin
from project_swagger import views
from django.urls import path

urlpatterns = [
    path('', views.some_view),
]
