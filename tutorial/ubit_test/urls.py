from django.urls import path
from ubit_test import views

urlpatterns = [
    path('ubit-trunk/', views.ubitTrunk)
]