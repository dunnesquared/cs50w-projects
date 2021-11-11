"""Backend feature support for online ordering system web application."""
import os
import json

import stripe # for credit card payments

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.views.decorators.csrf import csrf_exempt

from .models import (
    Pasta, Salad, DinnerPlatter, RegularPizza, SicilianPizza, PizzaTopping,
    Sub, SubTopping, Cart, CartItem, Order, OrderItem
)


# For security keys should always be stored in a local environment file
# and loaded from there.
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


# Create your views here.
def index(request):
    """Reroutes non logged-in users to login page automatically.
    Otherwise sends user to Menu page."""

    if not request.user.is_authenticated:
        print("User not authenticated redirecting to login...")
        return render(request, "orders/login.html")
    else:
        context = {
            "user": request.user
        }
        return HttpResponseRedirect(reverse("menu"))


def login_view(request):
    """Processes login credentials."""

    if request.method == 'GET':
        return render(request, "orders/login.html")

    # Get user input.
    username = request.POST["username"]
    password = request.POST["password"]

    err_message = ""

    # Assuming credentials are not blank...
    if len(username.strip()) and len(password.strip()):
        # Check credentials.
        print("User attempting login...")
        user = authenticate(request, username=username, password=password)

        # Log user in if all good. Otherwise, return to login page with error
        # message.
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            err_message = "INVALID CREDENTIALS!"
    else:
        err_message = "USERNAME AND PASSWORD CANNOT BE BLANK!"

    # Return error message
    print(err_message)
    return render(request, "orders/login.html", {"message": err_message})


def logout_view(request):
    """Logs current user out of application."""

    # Not logged in? Send back to home page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    print("User logging out...")
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})


def register_view(request):
    """Adds new user to db; checks that username is unique."""

    # Handle get request
    if request.method == 'GET':
        return render(request, "orders/register.html")

    # Get registration data
    username = request.POST["username"].strip()
    email = request.POST["email"].strip()
    first_name = request.POST["firstname"].strip()
    last_name = request.POST["lastname"].strip()
    password = request.POST["password"].strip()

    all_fields_filled = bool(username and email and first_name
                            and last_name and password)

    message = ""

    print("User attempting registration...")
    if all_fields_filled:
        # Check that username not already in use.
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            message =  "Registration successful!"
        except IntegrityError:
            message = "Username already in use. Please choose another."

    else:
        message = "Registration cancelled: One or more fields blank."

    print(message)
    return render(request, "orders/register.html", {'message': message})


def menu(request):
    """Displays menu if user has logged in successfully."""

    if not request.user.is_authenticated:
        message = "Please login before trying to access the menu."
        return render(request, "orders/login.html", {"message": message})

    # User authenticated
    print("Loading menu...")

    context = {
        "regular_pizzas": RegularPizza.objects.all(),
        "sicilian_pizzas": SicilianPizza.objects.all(),
        "subs": Sub.objects.all(),
        "sub_toppings": SubTopping.objects.all(),
        "pizza_toppings": PizzaTopping.objects.all(),
        "pastas": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "dinnerplatters": DinnerPlatter.objects.all()
    }

    return render(request, "orders/menu.html", context)


def cart(request):
    """Displays current contents of shopping cart."""

    if not request.user.is_authenticated:
        message = "Please login before trying to access your cart."
        return render(request, "orders/login.html", {"message": message})

    # Needed to get the right cart!
    user_id = request.user.id

    # Show what's currently in a user's cart.
    if request.method == 'GET':
        cart, cart_items = None, None

        try:
            print(f"Fetching cart data from db for User# {user_id}...")
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
        except ObjectDoesNotExist:
            print(f"There is currently no cart or cart items for User# {user_id}...")

        context = {
            "cart": cart,
            "cart_items": cart_items
        }
        return render(request, "orders/cart.html", context)

    # Add item to cart; create one if none exists yet.
    if request.method == 'POST':
        try:
            print(f"Creating new cart for user {user_id}!!")
            cart = Cart.objects.create(user=request.user)
        except IntegrityError:
            print(f"Cart object for user {user_id} already exists. Loading cart...")
            cart = Cart.objects.get(user=request.user)

        # Fetch info from db to create a cart item.
        # Default value as pastas and salads don't have a size
        item_size = '—'

        print("Processing menu item to add to cart...")

        if "regular-pizza" in request.POST:
            food_id = int(request.POST["regular-pizza"])

            # Get food info
            food = RegularPizza.objects.get(id=food_id)
            # Create name for cart item
            item_name = f"Regular Pizza, {food.name}"
            # Define size of item
            item_size = f"{food.size}"
            # Get price for cart item
            item_price = food.price

            # Get toppings
            if food.num_toppings > 0:
                topping_ids = request.POST.getlist('pizza-topping')

                # Add descr and extra cost of topping to food
                toppings = ""

                for topping_id in topping_ids:
                    topping = PizzaTopping.objects.get(id=topping_id)
                    toppings += topping.name +  ", "

                if topping_ids:
                    # Complete description; remove last comma.
                    toppings = toppings[:-2]
                    item_name += ": " + toppings

        if "sicilian-pizza" in request.POST:
            food_id = int(request.POST["sicilian-pizza"])

            # Get food info
            food = SicilianPizza.objects.get(id=food_id)
            # Create name for cart item
            item_name = f"Sicilian Pizza, {food.name}"
            # Define size of item
            item_size = f"{food.size}"
            # Get price for cart item
            item_price = food.price

            # Get toppings
            if food.num_toppings > 0:
                topping_ids = request.POST.getlist('pizza-topping')

                # Add descr and extra cost of topping to food
                toppings = ""

                for topping_id in topping_ids:
                    topping = PizzaTopping.objects.get(id=topping_id)
                    toppings += topping.name +  ", "

                if topping_ids:
                    # Complete description; remove last comma.
                    toppings = toppings[:-2]
                    item_name += ": " + toppings

        if "sub-sandwich" in request.POST:
            food_id = int(request.POST["sub-sandwich"])

            # Get food info
            food = Sub.objects.get(id=food_id)
            # Create name for cart item
            item_name = f"Sub, {food.name}"
            # Define size of item
            item_size = f"{food.size}"
            # Get price for cart item
            item_price = food.price

            # Get toppings
            topping_ids = request.POST.getlist('sub-topping')

            # Add descr and extra cost of topping to food
            toppings = ""
            toppings_price = 0

            for topping_id in topping_ids:
                topping = SubTopping.objects.get(id=topping_id)
                toppings += topping.name +  ", "
                toppings_price += topping.price

            if topping_ids:
                # Complete description; remove last comma.
                toppings = toppings[:-2]
                item_name += "; Extras: " + toppings

                # Get the total price
                item_price += toppings_price

        if "pasta" in request.POST:
            food_id = int(request.POST["pasta"])

            # Get food info
            food = Pasta.objects.get(id=food_id)

            # Create name for cart item
            item_name = f"Pasta, {food.name}"

            # Calculate total price for cart item
            item_price = food.price

        if "salad" in request.POST:
            food_id = int(request.POST["salad"])

            # Get food info
            food = Salad.objects.get(id=food_id)

            # Create name for cart item
            item_name = f"Salad, {food.name}"

            # Calculate total price for cart item
            item_price = food.price

        if "dinnerplatter" in request.POST:
            food_id = int(request.POST["dinnerplatter"])

            # Get food info
            food = DinnerPlatter.objects.get(id=food_id)

            # Create name for cart item
            item_name = f"Dinner Platter, {food.name}"

            # Define size of item
            item_size = f"{food.size}"

            # Calculate total price for cart item
            item_price = food.price

        # Add cart item.
        print("Adding item to cart...")
        cart_item = CartItem.objects.create(cart=cart,
                                name=item_name,
                                size=item_size,
                                price=item_price,
                                qty=1)

        print(f"Added🍕! {cart_item.name}, ${cart_item.price}")
        # Go back to menu.
        return HttpResponseRedirect(reverse("menu"))


def calculate_total(request):
    """Helper function that calculates the total of given order.

    Args:
        request: Django request object.

    Returns:
        total: Floating-point value representing total cost of order.
    """

    print("Calculating cart total cost...", end="")

    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate total price of order
    item_prices = [cart_item.price for cart_item in cart_items]
    total = 0

    for item_price in item_prices:
        total += item_price

    # Just in case ou have more than two decimals in your sum.
    print(f"${round(total, 2)}")
    return round(total, 2)


def checkout(request):
    """Displays final order; removes items from shopping cart."""

    if not request.user.is_authenticated:
        message = "Please login before trying to access this feature."
        return render(request, "orders/login.html", {"message": message})

    # This should probably return an error, not the cart state...
    print("Loading checkout summary...")
    if request.method == 'GET':
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)

            if len(cart_items) == 0:
                message = "Checkout failed: No cart items. Cart is empty."
                print(message)
                return render(request, "orders/error.html", {"err_message": message})

            context = {
                'cart': cart,
                'cart_items': cart_items,
                'total': calculate_total(request)
            }

        except ObjectDoesNotExist:
            message = "Checkout failed: Cart object does not exist."
            print(message)
            return render(request, "orders/error.html", {"err_message": message})

        return render(request, "orders/placeorder.html", context)

    if request.method == 'POST':

        if request.POST.get('remove'):
            # Remove item from db

            cart_item_id = request.POST.get('remove')
            cart_item = CartItem.objects.get(id=cart_item_id)
            print("Removing cart item...")
            cart_item.delete()
            print(f"Removing cart item...{cart_item.name} removed!🗑")
            return HttpResponseRedirect(reverse('cart'))

        elif request.POST.get('checkout'):
            cart_id = request.POST.get('checkout')

            try:
                cart = Cart.objects.get(id=cart_id)
                cart_items = CartItem.objects.filter(cart=cart)

                if len(cart_items) == 0:
                    message = "Checkout failed: No cart items. Cart is empty."
                    print(message)
                    return render(request, "orders/error.html", {"err_message": message})

                context = {
                    'cart': cart,
                    'cart_items': cart_items,
                    'total': calculate_total(request)
                }

            except ObjectDoesNotExist:
                message = "Checkout failed: Cart object does not exist."
                print(message)
                return render(request, "orders/error.html", {"err_message": message})

            return render(request, "orders/placeorder.html", context)


@csrf_exempt
def create_order(request):
    """Creates order based on shopping cart contents; removes shopping cart
       from db.
     """

    # Prevent users from placing an order via GET request by raising a
    # 403 Forbidden error
    if request.method == "GET":
        raise PermissionDenied

    # Create order and order items based on cart contents
    if request.method == "POST":
        # Get cart info
        cart = Cart.objects.get(user=request.user)

        # Get cart items
        cart_items = CartItem.objects.filter(cart=cart)

        # Get the amounf to charge to customer
        total = calculate_total(request)

        # Create order
        print("Creating order...")
        order = Order.objects.create(user=request.user,
                                     status='P',
                                     total=total)

        # Copy cart_items to order_items
        order_items = []
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(name=cart_item.name,
                                                    price=cart_item.price,
                                                    size=cart_item.size,
                                                    qty=cart_item.qty,
                                                    order=order)

            order_items.append(order_item)

        # Delete cart and cart items
        cart.delete()
        print("Cart deleted!")

        # Send back order info
        context = {
            'order': order,
            'order_items': order_items
        }

        print("Displaying confirmation page to customer...")
        return render(request, "orders/confirmation.html", context)


def view_orders(request):
    """Displays all placed orders to administrator."""

    if request.method == "GET":
        print("Checking credentials for order summary...")
        if request.user.is_authenticated and request.user.username == 'admin':
            # Get all orders in db
            context = {
                'orders': Order.objects.all()
            }
            print("Displaying order summary...")
            return render(request, "orders/vieworders.html", context)
        else:
            raise PermissionDenied


def credit_card(request):
    """Displays form for user to enter credit details."""

    if request.method == 'POST':

        # Make sure there are actually items from which a total can be calculated.
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)

            # Calculate the total cost of items in cart (should always be done
            # server-side)
            total = calculate_total(request)

            context = {
                'total': total
            }

            print(f"Cart Total🛒= ${total}!")

            print("Displaying Stripe credit card form...")
            return render(request, "orders/creditcard.html", context)

        except ObjectDoesNotExist:
            message = "Credit_card error: Cart or CartItems do not exist."
            print(message)
            return render(request, "orders/error.html", {"err_message" : message})

    else:
        raise PermissionDenied


def fetch_key(request):
    """Returns public Stripe key to client."""

    print("Fetching Stripe publishable test key...")
    return JsonResponse({'publishableKey': os.getenv('STRIPE_PUBLISHABLE_KEY')})


@csrf_exempt
def pay(request):
    """Processes and finalizes payment of order.

    Decorator @csrf_exempt required to for view to work properly.
    See https://stackoverflow.com/questions/35690997/django-1-9-csrf-token-missing-or-incorrect-using-stripe
    """

    try:
        print("Processing credit card credentials....")

        data = json.loads(request.body)

        # Stripe acccepts only integer amount values (in USD, this would be cents)
        order_total = int(calculate_total(request) * 100)

        # Create a new PaymentIntent with a PayementMethod ID from client
        intent = stripe.PaymentIntent.create(
            amount=order_total,
            currency=data['currency'],
            payment_method=data['paymentMethodId'],
            error_on_requires_action=True,
            confirm=True,
        )

        print("Payment received😸💰!!")

        # The payment is complete; money has been transferred
        return JsonResponse({'clientSecret':intent['client_secret']})

    except stripe.error.CardError as e:
        if e.code == 'authentication_required':
            print("Error: Credit card authentication required.😩")
            return JsonResponse({'error': 'This card requires authentication in order to proceed. Please use a different card.'})
        else:
            print(f"Error: {e.user_message}😩")
            return JsonResponse({'error': e.user_message})


def order_summary(request, order_id):
    """Displays summary of an order."""
    
    if request.method == "GET":
        print("Checking credentials for order summary...")
        if request.user.is_authenticated and request.user.is_superuser:
            # Get order info
            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                raise Http404("Order does not exist.")

            order_items = OrderItem.objects.filter(order=order)

            context = {
                'order': order,
                'order_items': order_items
            }
            print("Displaying order summary....")
            return render(request, "orders/order.html", context)
    else:
        raise PermissionDenied #


def order_confirmed(request):
    """Users shouldn't be trying to fetch this page. Bring up error page."""

    message = "Order confirmed failed: You are not allowed to refresh on the order-confirmed page."
    print(message)
    return render(request, "orders/error.html", {"err_message": message})
