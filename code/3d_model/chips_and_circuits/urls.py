"""
urls.py

Chips & Circuits 2021
Martijn van Veen, Olaf Stringer, Jan-Joost Raedts

Gives an overview of the available URLS.
"""

from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    url("upload_csv", views.upload_csv, name='upload_csv'),
]