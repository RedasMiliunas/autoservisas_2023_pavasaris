from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('orders/<int:pk>', views.OrderDetailView.as_view(), name='order')
]