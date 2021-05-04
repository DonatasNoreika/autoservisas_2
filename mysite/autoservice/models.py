from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Service(models.Model):
    name = models.CharField('Name', max_length=200)
    price = models.FloatField("Price")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'


class Car(models.Model):
    manufacturer = models.CharField('Manufacturer', max_length=200)
    model = models.CharField('Model', max_length=200)
    engine = models.CharField('Engine', max_length=200)

    def __str__(self):
        return f"{self.manufacturer} {self.model}, {self.engine}"

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'


class OwnerCar(models.Model):
    year = models.IntegerField('Year', null=True)
    owner = models.ForeignKey(User, verbose_name="Owner", on_delete=models.SET_NULL, null=True, blank=True)
    car = models.ForeignKey('Car', verbose_name="Model", on_delete=models.SET_NULL, null=True)
    licence_plate = models.CharField('Licence plate', max_length=200)
    vin_code = models.CharField('VIN code', max_length=200)

    def __str__(self):
        return f"{self.owner}: {self.car}, {self.licence_plate}, {self.vin_code}"

    class Meta:
        verbose_name = 'Owner Car'
        verbose_name_plural = 'Owners Cars'


class Order(models.Model):
    owner_car = models.ForeignKey('OwnerCar', verbose_name="Model", on_delete=models.SET_NULL, null=True)
    due_date = models.DateTimeField('Due Date', null=True, blank=True)

    def __str__(self):
        return f"{self.owner_car}: {self.owner_car.owner}, {self.due_date}"

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    STATUS = (
        ('r', 'Draft'),
        ('i', 'In progress'),
        ('d', 'Done'),
        ('c', 'Canceled'),
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        blank=True,
        default='r',
        help_text='Status',
    )


class OrderLine(models.Model):
    order = models.ForeignKey('Order', verbose_name="Order", on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey('Service', verbose_name="Service", on_delete=models.SET_NULL, null=True)
    qty = models.IntegerField("Quantity")

    class Meta:
        verbose_name = 'Order Line'
        verbose_name_plural = 'Order Lines'

    def __str__(self):
        return f"{self.order}: {self.service}, {self.qty}"