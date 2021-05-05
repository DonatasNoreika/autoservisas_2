from django.shortcuts import render
from .models import Service, Car, Order

# Create your views here.

def info(request):
    num_services = Service.objects.all().count()
    num_cars = Car.objects.all().count()
    num_orders_done = Order.objects.filter(status__exact='d').count()

    context = {
        'num_services': num_services,
        'num_cars': num_cars,
        'num_orders_done': num_orders_done,
    }
    return render(request, 'info.html', context=context)