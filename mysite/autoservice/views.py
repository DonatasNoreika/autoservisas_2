from django.shortcuts import render, get_object_or_404
from .models import Service, Car, Order, OwnerCar
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

def info(request):
    num_services = Service.objects.all().count()
    num_cars = OwnerCar.objects.all().count()
    num_orders_done = Order.objects.filter(status__exact='d').count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_services': num_services,
        'num_cars': num_cars,
        'num_orders_done': num_orders_done,
        'num_visits': num_visits,
    }
    return render(request, 'info.html', context=context)


def owner_cars(request):
    paginator = Paginator(OwnerCar.objects.all(), 1)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    return render(request, 'owner_cars.html', {'cars': paged_cars})


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

def search(request):
    """
    paprasta paieška. query ima informaciją iš paieškos laukelio,
    search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės
    didžiosios/mažosios.
    """
    query = request.GET.get('query')
    search_results = OwnerCar.objects.filter(Q(licence_plate__icontains=query) | Q(vin_code__icontains=query) | Q(car__manufacturer__icontains=query)  | Q(car__model__icontains=query))
    return render(request, 'search.html', {'cars': search_results, 'query': query})