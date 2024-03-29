from django.urls import path
from . import views

urlpatterns = [
    path('create-sheet', views.create_spreadsheet),
    path('update', views.update_spreadsheet),
    path('get', views.get_headers_from_table),
    path('get-spreadsheets-id', views.get_spreadsheets_id),
    path('download-raw', views.download_spreadsheet),
]
