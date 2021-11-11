from django.contrib import admin

from .models import (
    Pasta, Salad, DinnerPlatter, RegularPizza, SicilianPizza, PizzaTopping,
    Sub, SubTopping, Cart, CartItem, Order, OrderItem
)

# Register your models here.
admin.site.register(RegularPizza)
admin.site.register(SicilianPizza)
admin.site.register(PizzaTopping)
admin.site.register(Sub)
admin.site.register(SubTopping)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(DinnerPlatter)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
