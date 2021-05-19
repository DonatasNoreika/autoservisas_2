from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from tinymce.models import HTMLField
from PIL import Image
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

import pytz
utc = pytz.UTC


# Create your models here.

class Service(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=200)
    price = models.FloatField(verbose_name=_("Price"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')


class Car(models.Model):
    manufacturer = models.CharField(verbose_name=_('Manufacturer'), max_length=200)
    model = models.CharField(verbose_name=_('Model'), max_length=200)
    engine = models.CharField(verbose_name=_('Engine'), max_length=200)

    def __str__(self):
        return f"{self.manufacturer} {self.model}, {self.engine}"

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')


class OwnerCar(models.Model):
    year = models.IntegerField(_('Year'), null=True)
    owner = models.ForeignKey(User, verbose_name=_("Owner"), on_delete=models.SET_NULL, null=True, blank=True)
    car = models.ForeignKey('Car', verbose_name=_("Model"), on_delete=models.SET_NULL, null=True)
    licence_plate = models.CharField(verbose_name=_('Licence plate'), max_length=200)
    vin_code = models.CharField(verbose_name=_('VIN code'), max_length=200)
    photo = models.ImageField(verbose_name=_('Photo'), upload_to='cars', null=True)
    description = HTMLField(verbose_name=_("Description"), null=True)

    def __str__(self):
        return f"{self.owner}: {self.car}, {self.licence_plate}, {self.vin_code}"

    class Meta:
        verbose_name = _('Owner Car')
        verbose_name_plural = _('Owners Cars')


class Order(models.Model):
    owner_car = models.ForeignKey('OwnerCar', verbose_name=_("Model"), on_delete=models.SET_NULL, null=True)
    due_date = models.DateTimeField(verbose_name=_('Due Date'), null=True, blank=True)

    @property
    def final(self):
        total = 0
        lines = OrderLine.objects.filter(order=self.id)
        for line in lines:
            total += line.service.price * line.qty
        return total

    def __str__(self):
        return f"{self.owner_car}: {self.owner_car.owner}, {self.due_date}"

    @property
    def is_overdue(self):
        if self.due_date and datetime.today().replace(tzinfo=utc) > self.due_date.replace(tzinfo=utc):
            return True
        return False

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    STATUS = (
        ('r', _('Draft')),
        ('i', _('In progress')),
        ('d', _('Done')),
        ('c', _('Canceled')),
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        blank=True,
        default='r',
        help_text=_('Status'),
    )

    def get_absolute_url(self):
        """Nurodo konkretaus aprašymo galinį adresą"""
        return reverse('my_order', args=[str(self.id)])

class OrderLine(models.Model):
    order = models.ForeignKey('Order', verbose_name=_("Order"), on_delete=models.SET_NULL, null=True, related_name='lines')
    service = models.ForeignKey('Service', verbose_name=_("Service"), on_delete=models.SET_NULL, null=True)
    qty = models.IntegerField(_("Quantity"))

    @property
    def total(self):
        return self.service.price * self.qty

    class Meta:
        verbose_name = _('Order Line')
        verbose_name_plural = _('Order Lines')

    def __str__(self):
        return f"{self.order}: {self.service}, {self.qty}"


class OrderComment(models.Model):
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(verbose_name=_("Date"), auto_now_add=True)
    content = models.TextField(_('Comment'), max_length=2000)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name=_("Photo"), default="default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profile"

    def save(self):
        super().save()
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)
