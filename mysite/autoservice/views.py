from django.shortcuts import render, get_object_or_404
from .models import Service, Car, Order, OwnerCar
from django.views import generic

# Create your views here.

def info(request):
    num_services = Service.objects.all().count()
    num_cars = OwnerCar.objects.all().count()
    num_orders_done = Order.objects.filter(status__exact='d').count()

    context = {
        'num_services': num_services,
        'num_cars': num_cars,
        'num_orders_done': num_orders_done,
    }
    return render(request, 'info.html', context=context)


def owner_cars(request):
    return render(request, 'owner_cars.html', {'cars': OwnerCar.objects.all()})


def owner_car(request, owner_car_id):
    single_owner_car = get_object_or_404(OwnerCar, pk=owner_car_id)
    return render(request, 'owner_car.html', {'owner_car': single_owner_car})


class OrderListView(generic.ListView):
    model = Order
    paginate_by = 2
    template_name = 'orders.html'


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order.html'