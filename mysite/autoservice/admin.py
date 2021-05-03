from django.contrib import admin

# Register your models here.

from .models import Service, Car, OwnerCar, Order, OrderLine

admin.site.register(Service)
admin.site.register(Car)
admin.site.register(OwnerCar)
admin.site.register(Order)
admin.site.register(OrderLine)