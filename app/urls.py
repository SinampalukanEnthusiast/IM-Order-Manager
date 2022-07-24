from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('orders/', views.orders, name='orders'),
    path('orders/view/<int:id>', views.order_detail, name='order_detail'),
    path('orders/delete/<int:id>', views.order_delete, name='order_delete'),
    path('orders/create/', views.create_order, name='create_order'),
    path('add_product/', views.add_product, name='add_product'),


]
