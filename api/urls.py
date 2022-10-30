# from django.conf.urls import url
from django.urls import path, include

from . import views

urlpatterns = [
    path('stocks/', views.read_all),
    path('stocks/<str:name>', views.read_one),
    path('sales/', views.sales)
]
