from django.shortcuts import render, get_object_or_404, reverse
from .models import Service, Car, Order, OwnerCar
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import OrderCommentForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)

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


class OrderListView(ListView):
    model = Order
    paginate_by = 6
    template_name = 'orders.html'


class OrderDetailView(FormMixin, DetailView):
    model = Order
    template_name = 'order.html'
    form_class = OrderCommentForm

    # nurodome, kur atsidursime komentaro s??km??s atveju.
    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.object.id})

    # ??traukiame form?? ?? kontekst??, inicijuojame pradin?? 'book' reik??m??.
    def get_context_data(self, *args, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['form'] = OrderCommentForm()
        return context

    # standartinis post metodo perra??ymas, naudojant FormMixin, galite kopijuoti tiesiai ?? savo projekt??.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # ??tai ??ia nurodome, kad knyga bus b??tent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijung??s.
    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.user = self.request.user
        form.save()
        return super(OrderDetailView, self).form_valid(form)


def search(request):
    """
    paprasta paie??ka. query ima informacij?? i?? paie??kos laukelio,
    search_results prafiltruoja pagal ??vest?? tekst?? knyg?? pavadinimus ir apra??ymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raid??s
    did??iosios/ma??osios.
    """
    query = request.GET.get('query')
    search_results = OwnerCar.objects.filter(
        Q(licence_plate__icontains=query) | Q(vin_code__icontains=query) | Q(car__manufacturer__icontains=query) | Q(
            car__model__icontains=query))
    return render(request, 'search.html', {'cars': search_results, 'query': query})



@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reik??mes i?? registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slapta??od??iai
        if password == password2:
            # tikriname, ar neu??imtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, _('Username %(username)s already exists!') % {'username': username})
                return redirect('register')
            else:
                # tikriname, ar n??ra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, _('Email %(email)s already exists!') % {'email': email})
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame nauj?? vartotoj??
                    User.objects.create_user(username=username, email=email, password=password)
                    return redirect('login')
        else:
            messages.error(request, _('Passwords do not match!'))
            return redirect('register')
    return render(request, 'register.html')


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, _('Profile updated'))
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)


class UserOrderListView(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'user_orders.html'

    def get_queryset(self):
        return Order.objects.filter(owner_car__owner=self.request.user)


class UserOrderDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'user_order.html'
    form_class = OrderCommentForm

    # nurodome, kur atsidursime komentaro s??km??s atveju.
    def get_success_url(self):
        return reverse('my_order', kwargs={'pk': self.object.id})

    # ??traukiame form?? ?? kontekst??, inicijuojame pradin?? 'book' reik??m??.
    def get_context_data(self, *args, **kwargs):
        context = super(UserOrderDetailView, self).get_context_data(**kwargs)
        context['form'] = OrderCommentForm()
        return context

    # standartinis post metodo perra??ymas, naudojant FormMixin, galite kopijuoti tiesiai ?? savo projekt??.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # ??tai ??ia nurodome, kad knyga bus b??tent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijung??s.
    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.user = self.request.user
        form.save()
        return super(UserOrderDetailView, self).form_valid(form)


class UserOrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ['owner_car', 'due_date']
    template_name = 'user_order_form.html'

    def get_form(self, *args, **kwargs):
        form = super(UserOrderCreateView, self).get_form(*args, **kwargs)
        form.fields['owner_car'].queryset = OwnerCar.objects.filter(owner=self.request.user)
        return form


class UserOrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    fields = ['owner_car', 'due_date']
    template_name = 'user_order_form.html'

    def get_form(self, *args, **kwargs):
        form = super(UserOrderUpdateView, self).get_form(*args, **kwargs)
        form.fields['owner_car'].queryset = OwnerCar.objects.filter(owner=self.request.user)
        return form

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.owner_car.owner


class UserOrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    success_url = "/autoservice/myorders/"
    template_name = 'user_order_delete.html'

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.owner_car.owner
