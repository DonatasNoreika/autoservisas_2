"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.info, name='info'),
    path('owner_cars/', views.owner_cars, name='owner_cars'),
    path('owner_car/<int:owner_car_id>', views.owner_car, name='owner_car'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('search/', views.search, name='search'),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name='order'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('myorders/', views.UserOrderListView.as_view(), name='my_orders'),
    path('myorders/<int:pk>', views.UserOrderDetailView.as_view(), name='my_order'),
    path('myorders/new', views.UserOrderCreateView.as_view(), name='my_order-new'),
]
