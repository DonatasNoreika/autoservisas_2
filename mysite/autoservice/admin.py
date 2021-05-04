from django.contrib import admin

# Register your models here.

from .models import Service, Car, OwnerCar, Order, OrderLine


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0  # išjungia placeholder'ius


class OrderAdmin(admin.ModelAdmin):
    list_display = ('owner_car', 'due_date', 'status')
    list_editable = ('due_date', 'status')
    inlines = [OrderLineInline]


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


class CarAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model', 'engine')


class OwnerCarAdmin(admin.ModelAdmin):
    list_display = ('year', 'owner', 'car', 'licence_plate', 'vin_code')
    list_filter = ('owner', 'car')
    search_fields = ('licence_plate', 'vin_code')

admin.site.register(Service, ServiceAdmin)
admin.site.register(Car)
admin.site.register(OwnerCar, OwnerCarAdmin)
admin.site.register(Order, OrderAdmin)
