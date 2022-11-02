from django.urls import path
from . import views

urlpatterns = [
    path('create-sheet', views.create_spreadsheet),
]
