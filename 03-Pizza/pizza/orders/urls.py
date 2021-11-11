from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("menu", views.menu, name="menu"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("create_order", views.create_order, name="create_order"),
    path("view_orders", views.view_orders, name="view_order"),
    path("order/<int:order_id>/", views.order_summary, name="order_summary"),
    path("credit_card", views.credit_card, name="credit_card"),
    path("stripe-key", views.fetch_key, name="fetch_key"),
    path("pay", views.pay, name="pay"),
    path("order-confirmed", views.order_confirmed, name="order_confirmed")
]
