from django.contrib.auth.models import User
from django.test import Client, TestCase, LiveServerTestCase
from django.core.exceptions import ObjectDoesNotExist

# from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException

from .models import (
    Pasta, Salad, DinnerPlatter, RegularPizza, SicilianPizza, PizzaTopping,
    Sub, SubTopping, Cart, CartItem, Order, OrderItem
)


# Create your tests here
class OrdersTestCase(TestCase):

    def setUp(self):
        self.credentials =  {
            'username': 'test_user',
            'password': 'secret'
        }

        self.credentials_admin = {
            'username': 'admin',
            'password': 'adminsecret',
            'email': 'admin@admin.admin'
        }

        self.credentials_user2 =  {
            'username': 'user2',
            'password': 'secret2'
        }

        self.user1 = User.objects.create_user(**self.credentials)
        self.user2 = User.objects.create_user(**self.credentials_user2)
        self.superuser1 = User.objects.create_superuser(**self.credentials_admin)

        self.regPizza1 = RegularPizza.objects.create(name="Cheese", size="S", num_toppings=0, price=12.70)
        self.regPizza2 = RegularPizza.objects.create(name="1 topping", size="S", num_toppings=1, price=13.70)
        self.pizzaTopping1 = PizzaTopping.objects.create(name="Tuna")
        self.sub1 = Sub.objects.create(name="Italian", size="S", price=6.50)
        self.subTopping1 = SubTopping.objects.create(name="Cheese", price=0.50)

        # New cart doesn't seem to be created in tests. Items are just added to this cart???
        # self.cart1 = Cart.objects.create(user=self.user2)
        # self.cartItem1 = CartItem.objects.create(cart=self.cart1, name="Pizza, Cheese", size="S", price=12.70, qty=1)
        #
        # self.order1 = Order.objects.create(user=self.user2, status='P', total=self.cartItem1.price)
        # self.ordertem1 = OrderItem.objects.create(order=self.order1, name="Pizza, Cheese", size="S", price=12.70, qty=1)


    def test_loginOK(self):
        """Check that user with good credentials can login"""
        c = Client()
        login = c.login(username='test_user', password='secret')
        self.assertTrue(login)

    def test_loginBadCred(self):
        """Check that user with bad credentials not logged"""
        c = Client()
        # Bad pw
        login = c.login(username='test_user', password='yo')
        self.assertFalse(login)
        # Bad username
        login = c.login(username='best_user', password='secret')
        self.assertFalse(login)

    def test_index_notLoggedIn(self):
        """Check that index returns login form if user not logged-in"""
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.content)

    def test_index_loggedIn(self):
        """Check that index returns Menu form if user is logged-in."""
        c = Client()
        c.login(username='test_user', password='secret')
        response = c.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Menu', response.content)

    def test_index_loggedinAdmin(self):
        """Check that redirected to Menu with url to view orders"""
        c = Client()
        c.login(username='admin', password='adminsecret')
        response = c.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'View Orders', response.content)

    def test_login_view_BadCred(self):
        """Check that user redirected to login form with warning message"""
        c = Client()
        c.login(username='FAKEUSER', password='secret')
        response = c.post('/login', {'username': 'FAKEUSER', 'password': 'secret'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'INVALID CREDENTIALS!', response.content)

    def test_login_view_GET(self):
        """Check that user redirected to login form page on GET request"""
        c = Client()
        response = c.get('/login', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.content)

    def test_logout_view_loggedin(self):
        """Check that user is redirected back to login form page with logout message"""
        c = Client()
        c.login(username='test_user', password='secret')
        response = c.get('/logout', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged out.', response.content)

    def test_login_view_blankCredentials(self):
        """Check that user is redirected back to login form page if trying to
        login with blank credentials."""
        c = Client()
        # Blank username
        c.login(username='   ', password='secret')
        response = c.post('/login', {'username': '   ', 'password': 'secret'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'USERNAME AND PASSWORD CANNOT BE BLANK!', response.content)
        c.logout()
        # Blank password
        c.login(username='FAKEUSER', password='  ')
        response = c.post('/login', {'username': '   ', 'password': '  '}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'USERNAME AND PASSWORD CANNOT BE BLANK!', response.content)

    def test_register_GET(self):
        """Checks that registration form when GET request made to route."""
        c = Client()
        response = c.get("/register")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.content)

    def test_register_createNewUser(self):
        """Checks that registration results in a new user being added to db."""
        c = Client()
        register_info = {
            "username": "registerMan",
            "email": 'register@register.com',
            "firstname": "Reginald",
            "lastname": 'Register',
            "password": "secret"
        }
        response = c.post("/register", register_info, follow=True)
        self.assertEqual(response.status_code, 200)

        try:
            user = User.objects.get(username="registerMan")
        except ObjectDoesNotExist:
            user = None

        self.assertTrue(user)
        self.assertIn(b'Registration successful!', response.content)


    def test_register_emptyFields(self):
        """Checks that users are not able register with incomplete information."""
        c = Client()
        register_info = {
            "username": "",
            "email": '  ',
            "firstname": "\n",
            "lastname": '\t',
            "password": "\r\t\n"
        }
        response = c.post("/register", register_info, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration cancelled: One or more fields blank.',
                        response.content)


    def test_register_username_taken(self):
        """Checks that users cannot register with a username that has been taken"""
        c = Client()
        register_info = {
            "username": "test_user",
            "email": 'register@register.com',
            "firstname": "Reginald",
            "lastname": 'Register',
            "password": "secret"
        }
        response = c.post("/register", register_info, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username already in use. Please choose another.',
                        response.content)


    def test_menu_notloggedin(self):
        c = Client()
        response = c.get("/menu", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please login before trying to access the menu.',
                        response.content)


    def test_cart_notloggedin(self):
        c = Client()
        response = c.get("/cart", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please login before trying to access your cart.',
                        response.content)


    def test_cart_GET(self):
        c = Client()
        c.login(username='test_user', password='secret')
        response = c.get("/cart")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Shopping Cart',
                        response.content)

    def test_cart_FirstTime(self):
        c = Client()
        c.login(username='test_user', password='secret')
        response = c.get("/cart")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cart does not exist. To create a cart, add an item from the menu.',
                        response.content)

    def test_cart_addItem(self):
        c = Client()
        c.login(username='test_user', password='secret')
        response = c.post("/cart", {"regular-pizza": 1}, follow=True)
        response = c.get("/cart")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Regular Pizza, Cheese',
                        response.content)
        self.assertIn(b'Small', response.content)
        self.assertIn(b'$12.70', response.content)

    def test_cart_removeItemEmptyCart(self):
        c = Client()
        c.login(username='test_user', password='secret')
        # add an item
        response = c.post("/cart", {"regular-pizza": 1}, follow=True)
        response = c.get("/cart")
        self.assertEqual(response.status_code, 200)
        # remove the item
        response = c.post("/checkout", {"remove": 1}, follow=True)
        self.assertIn(b"Your cart is empty. Why don't you fill it up with pizza",
                            response.content)

    def test_cart_foodWithTopping(self):
        c = Client()
        c.login(username='test_user', password='secret')
        # add an item
        response = c.post("/cart", {"regular-pizza": 2, "pizza-topping": 1},
                                    follow=True)
        response = c.get("/cart")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Regular Pizza, 1 topping: Tuna',
                        response.content)
        self.assertIn(b'Small', response.content)
        self.assertIn(b'$13.70', response.content)

    def test_cart_AddToppingWhenCant(self):
        c = Client()
        c.login(username='test_user', password='secret')
        # add an item: "1" is a reg cheese pizza, no toppings
        response = c.post("/cart", {"regular-pizza": 1, "pizza-topping": 1},
                                    follow=True)
        response = c.get("/cart")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Tuna',
                        response.content)

    def test_cart_SubToppingSum(self):
        c = Client()
        c.login(username='test_user', password='secret')
        # add an item
        response = c.post("/cart", {"sub-sandwich": 1, "sub-topping": 1},
                                    follow=True)
        response = c.get("/cart")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sub, Italian; Extras: Cheese',
                        response.content)
        self.assertIn(b'Small', response.content)
        self.assertIn(b'$7.00', response.content)


    def test_checkout_notloggedin(self):
        c = Client()
        response = c.get("/checkout", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please login before trying to access this feature.',
                        response.content)

    def test_checkout_CartDoesNotExist(self):
        c = Client()
        c.login(username='test_user', password='secret')
        response = c.get("/checkout")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Checkout failed: Cart object does not exist.',
                        response.content)

    def test_checkout_CartEmpty(self):
        c = Client()
        c.login(username='test_user', password='secret')
        # add an item
        response = c.post("/cart", {"regular-pizza": 1}, follow=True)
        response = c.get("/cart")
        self.assertEqual(response.status_code, 200)
        # remove the item
        response = c.post("/checkout", {"remove": 1}, follow=True)
        # Try accessing checkout even if you don't have anything in your cart
        response = c.get("/checkout")
        self.assertIn(b"Checkout failed: No cart items. Cart is empty.",
                        response.content)

    # Unable to make test work!!!
    # def test_checkout_Sum(self):
    #     c = Client()
    #     c.login(username='test_user', password='secret')
    #     # add an two items, one with a topping
    #     response = c.post("/cart", {"regular-pizza": 1}, follow=True)
    #     response = c.post("/cart", {"sub-sandwich": 1, "sub-topping": 1}, follow=True)
    #     response = c.get("/checkout")
    #     self.assertIn(b"Total = $19.70", response.content)


    # Credit Card
    # not logged in - not needed (GET is forbidden regardless of login status)
    # GET 403 forbidden error
    # POST Checkout loads credit card page
    def test_creditcard_GET_forbidden(self):
        c = Client()
        c.login(username='test_user', password='secret')
        response = c.get('/credit_card', follow=True)
        self.assertEqual(response.status_code, 403)

    def test_creditcard(self):
        c = Client()
        c.login(username='test_user', password='secret')
        # add an item
        response = c.post("/cart", {"regular-pizza": 1}, follow=True)
        response = c.post("/credit_card", {"confirm": 12.70}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Credit Card Details",
                        response.content)



    # View_orders
    # not logged in
    # not logged in as admin (should be checking for superuser status, not name)
    # see if page loads correctly
    def test_viewOrders_notloggedin(self):
        c = Client()
        response = c.get("/view_orders", follow=True)
        self.assertEqual(response.status_code, 403)

    def test_viewOrders_notsuperuser(self):
        c = Client()
        c.login(username='test_user', password='secret')
        response = c.get("/view_orders", follow=True)
        self.assertEqual(response.status_code, 403)


    def test_viewOrders_issuperuser(self):
        c = Client()
        c.login(username='admin', password='adminsecret')
        response = c.get("/view_orders", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Orders",
                        response.content)

    # Problem
        # You'll need to create a fake order in your setUp to test this
        # feature as you cannot place credit card payments!


    # Order_summary
    # not logged in as superuser
    # Good order id
    # Bad order id

    # Unable to create order, cart without other tests failing. Why???


class MySeleniumTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # cls.selenium = WebDriver()

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--allow-running-insecure-content")
        cls.selenium = webdriver.Chrome(chrome_options=chrome_options)

        cls.selenium.implicitly_wait(10)


    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_index(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assertEqual(self.selenium.title, "Pinocchio's Pizza & Subs: Login")

    def test_login(self):
        """Checks that users can't click button until both fields are filled;
        users can't login with bad credentials; users can login with good
        credentials.
         """
        self.selenium.get('%s%s' % (self.live_server_url, '/login'))
        self.assertEqual(self.selenium.title, "Pinocchio's Pizza & Subs: Login")
        #
        # Get input elements
        # username_input = self.selenium.find_element_by_name("username")
        # password_input = self.selenium.find_element_by_name("password")
        # submitbutton_input = self.selenium.find_element_by_name("login")
        #
        # # TEST: Try logging in with blank data
        # username_input.send_keys(' ')
        # password_input.send_keys(" ")
        # submitbutton_input.click()
        #
        # try:
        #     # WebDriverWait(self.selenium, 3).until(EC.alert_is_present(), 'Timed out waiting for alert to appear.')
        #
        #     alert = self.selenium.switch_to_alert()
        #     self.assertIn('One or more input fields empty. Please fill all fields!',
        #                 alert.get_text)
        #     alert.accept()
        #     print("Alert accepted!!")
        #
        # except TimeoutException:
        #     print("No alert!!")

        # Login with bad username and password
        username_input = self.selenium.find_element_by_name("username")
        password_input = self.selenium.find_element_by_name("password")
        submitbutton_input = self.selenium.find_element_by_name("login")


        username_input.send_keys('fakeuser')
        password_input.send_keys("123")
        submitbutton_input.click()


        # Check that message returned and button is enabled
        self.assertIn("INVALID CREDENTIALS!", self.selenium.find_element_by_id("message").text)
        self.assertTrue(self.selenium.find_element_by_name("login").is_enabled())


        # # TEST: Login with real credentials
        # from selenium.webdriver.support.wait import WebDriverWait
        # timeout = 2
        #
        # # Get input elements (as they go stale...)
        # username_input = self.selenium.find_element_by_name("username")
        # password_input = self.selenium.find_element_by_name("password")
        # submitbutton_input = self.selenium.find_element_by_name("login")
        #
        # username_input.send_keys('alexD9')
        # password_input.send_keys("alex12345")
        # submitbutton_input.click()
        #
        # # self.selenium.find_element_by_id("input-form").submit()
        #  # Wait until the response is received
        #
        # WebDriverWait(self.selenium, timeout).until(lambda driver: driver.find_element_by_tag_name('body'))
        #
        # self.assertEqual(self.selenium.title, "Pinocchio's Pizza: Menu")

    #
    # def test_menu(self):
    #     """Checks that users 'Add to Cart' buttons are disabled when initially accessing it."""
    #     c = Client()
    #     login = c.login(username='test_user', password='secret')
    #     self.selenium.get('%s%s' % (self.live_server_url, '/menu'))
    #     self.assertEqual(self.selenium.title, "Pinocchio's Pizza: Menu")
