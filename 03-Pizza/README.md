# Project 3

Web Programming with Python and JavaScript

## Pizza (version 1.0.2)

For Project 3, I created an a mock online ordering system for the real-life
Italian restaurant [Pinnochio's Pizza and Subs](http://pinnochiospizza.net)
in Cambridge, MA. The app was implemented using the Django framework and
maintains the original minimalist aesthetic of the parent website. Using the
web app customers can register, login and order food items for pickup.
Customers pay for their orders by credit card, a feature largely handled
via [Stripe](https://stripe.com/en-ca), an easy-to-use platform to integrate online payments into an application. Administrators can view orders via the Django app or easily update the database
through Django's own admin portal.

Note that a "Special" pizza has **five** toppings.

## Running Django project on your machine

To run the online ordering system on your machine, do the following:

1. Download/clone `Project 3 - Pizza` to your computer.
2. Setup and launch a virtual environment.
3. Install the required modules. In your shell type ```pip install -r requirements.txt```.
4. Change directory so that you're inside the `pizza` folder, the root of the Django project.

5. Create a superuser account. On the shell, type ```python manage.py createsuperuser```
to create an administrator account. Use this username and password to
make any modifications to the database via Django's built-in admin portal.

6. Set up the `stripe` environment variables. Stripe uses private and public keys
to secure online transactions. See the `Personal Touch` section below for what to do.

7. Launch the app with `python manage.py runserver`.

8. Access the web app at url `http://http://127.0.0.1:8000/`. The admin portal
can be accessed via `http://http://127.0.0.1:8000/admin`

9. Start using the online ordering system! You can begin by either logging in
with your admin credentials, or by creating a new user account using the
registration feature.

N.B.
It may be that you will need to setup the `sqlite` database. To do so,
you must 'migrate' the app's relation models defined in `models.py` to
the database proper.

    Run the following
    ```
    python manage.py makemigrations
    ```
    followed by
    ```
    python manage.py migrate.
    ```


## Personal touch - Stripe credit card payments

As a personal touch for this project, I decided to implement a feature
that allowed users to make credit card payments via Stripe's API. To use
the feature, you will need to register with Stripe, to access your own
public and secret test API keys. Once you have these, you need to
save them as environment variables. This can be done with the following
commands

```
export STRIPE_PUBLISHABLE_KEY=pk_test_...
```
```
export STRIPE_SECRET_KEY=sk_test_...
```

To use the credit card feature, it's important that your machine is *online*.
If you don't see anything in the credit card input box, it's either because
the keys have not been saved as environment variables or the app is having
trouble connecting to the internet.

Use the following credit numbers to test the pay feature (you can make-up the
the card's expiry date and ZIP code),

- 4242424242424242: Valid credit card number. Payment will succeed.
- 4000002500003155: Requires authentication. Card will be declined.
- 4000000000009995: Insufficient funds. Card will be declined.

## Folders/files of note

All relevant functionality for this project resides in the `orders` app folder.
The following directories and files are children of that directory.

`static\orders\`
Directory containing all JavaScript and stylesheet files.

- `checkfields.js`: Checks whether all form fields are filled in login/registration forms.
- `creditcard.js`: Important script that handles transactions with `stripe` API. Code for this script was largely adapted from `stripe` github [sample](https://github.com/stripe-samples).
- `menu.js': Ensures that users cannot add an item to their shopping carts until something has been selected; ensures that the correct number of toppings are added to a given pizza/sub.
- `style.css`: Style sheet of project. Special thanks to Captain Anonymous for his/her code that helped me implement the Italian flag as I envisaged it. [Source](https://codepen.io/anon/pen/ZywmeO). Code for nav bar buttons was copied and adapted from the Pinnochio's website to
maintain a consistent look between it and the online ordering system.

`templates\orders\*.html`: Django HTML templates used to render site functionality.

`admin.py`: Django file where database models are registered so they can be accessed using Django's built-in admin portal.

`models.py`: Django models used to create relations in the database.

`tests.py`: Django unit and functional test script for the project. See 'Running tests' below.

`urls.py`: Django file to to map address-bar urls to view routes.

`views.py`: Django file that contains server routes that implement core functionality.
Core domain logic and database interfacing found here.


## Running tests

If you want to run Selenium tests on your computer, ensure that you have `selenium` module installed via `pip`, as well as the **Google Chrome** web browser. Moreover, you'll need to download [`ChromeDriver`](https://chromedriver.chromium.org/). Install the version that is right for your system in a folder where `python` can find it,
i.e. in some directory specified in your PATH environment variable.

To run all the tests, enter the following in your shell.

```
python manage.py tests
```

Should you just want to run Django's unittest tests, type

```
python manage.py test orders.tests.OrdersTestCase
```

Should you just want to run Selenium tests, type

```
python manage.py test orders.tests.MySeleniumTests
```

N.B. The Selenium tests are incomplete. There was a bug that I could not
solve regarding testing the JavaScript features of the project. I hope to have
this resolved in a future update.
