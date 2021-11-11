from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone # To create timezone 'aware' datetime object
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


# Add new food sizes here
SIZES = (
    ('S', 'Small'),
    ('L', 'Large')
)

class RegularPizza(models.Model):
    name = models.CharField(max_length=64)
    size = models.CharField(max_length=1, choices=SIZES)
    num_toppings = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.name}, {self.get_size_display()}, ${self.price}"


class SicilianPizza(models.Model):
    name = models.CharField(max_length=64)
    size = models.CharField(max_length=1, choices=SIZES)
    num_toppings = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.name}, {self.get_size_display()}, ${self.price}"


class PizzaTopping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Sub(models.Model):
    name = models.CharField(max_length=64)
    size = models.CharField(max_length=1, choices=SIZES)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.name}, {self.get_size_display()}, ${self.price}"


class SubTopping(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.name}, ${self.price}"


class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.name}, ${self.price}"


class Salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.name}, ${self.price}"


class DinnerPlatter(models.Model):
    name = models.CharField(max_length=64)
    size = models.CharField(max_length=1, choices=SIZES)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.name}, {self.get_size_display()}, ${self.price}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Cart# {self.id}, User# {self.user.id}, created {self.created_at}"


class CartItem(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    size = models.CharField(max_length=1, default='—', choices=SIZES)
    qty = models.PositiveSmallIntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return f"CartItem_Id: {self.id}, Cart#: {self.cart.id}, User#: {self.cart.user.id}, Item: {self.name}, Qty: {self.qty}: Price: ${self.price}"


class Order(models.Model):
    STATUS = (
        ('P', 'Pending'),
        ('O', 'Out for Delivery'),
        ('C', 'Completed'),
        ('R', 'Ready for Pickup')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=1, choices=STATUS)
    total = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):

        descr = f"""
        Order# : {self.id},
        Customer ID: {self.user.id},
        Created: {self.created_at},
        Total: {self.total},
        Status: {self.get_status_display()}
        """
        return descr


class OrderItem(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    size = models.CharField(max_length=1, default='—', choices=SIZES)
    qty = models.PositiveSmallIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        descr = f"""
        OrderItem_ID: {self.id},
        Order#: {self.order.id},
        Customer#: {self.order.user.id},
        Item: {self.name},
        Qty: {self.qty}:
        Price: ${self.price}
        """
        return descr
