import pytest
import application
import json


@pytest.fixture
def client():
     application.app.config['TESTING'] = True
     testing_client = application.app.test_client()
     yield testing_client


### HOME PAGE
def test_root(client):
    rv = client.get('/')
    assert b'Welcome' in rv.data

## REGISTER ###

def test_newuser(client):
    rv = client.get('/register')
    assert b'Create Account' in rv.data

def test_register_name_already_in_db(client):
    username = "admin"
    password = "123"

    rv = client.post('/register', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

    assert b'all ready in use' in rv.data

def test_register_blank_name(client):
    username = "    "
    password = "123"

    rv = client.post('/register', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

    assert b'username/password field empty.' in rv.data

def test_register_blank_password(client):
    username = "admin"
    password = "   "

    rv = client.post('/register', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

    assert b'username/password field empty.' in rv.data

def test_register_blank_both(client):
    username = " \n\n "
    password = "   "

    rv = client.post('/register', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

    assert b'username/password field empty.' in rv.data

# Test can only be done once unless able to remove user somehow
# def test_register_success(client):
#     username = "test_user"
#     password = "987"
#
#     rv = client.post('/register', data=dict(
#         username=username,
#         password=password
#     ), follow_redirects=True)
#
#     assert b'Registration complete!' in rv.data


## LOGIN ##
#  good credentials
#  good credentials again
#  good user name, bad password
#  bad user name, good password
#  blank user name or password

def login(client, username, password):
    """Wrapper function to test login feauture

    Args:
        username: String representing user's username.
        password: String representing user's password.

    Returns:
        rv: object containing response from posted request

    """
    rv = client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

    return rv

def test_login_good_credentials(client):
    assert b'Search' in login(client, "admin", "123").data

def test_login_good_credentials_again(client):
    assert b'Search' in login(client, "borat", "999").data

def test_login_good_name_bad_pw(client):
    assert b'Incorrect user name' in login(client, "admin", "900").data

def test_login_bad_name_good_pw(client):
    assert b'Incorrect user name' in login(client, "adminy", "123").data

def test_login_blank_data(client):
    assert b'Unable to complete login: username/password field empty.' in login(client, " ", " ").data


## LOGOUT ##
#  logging out when no-one logged in
#  logging out when someone logged in

def test_logout_someone_logged_in(client):
    login(client, "admin", "123")
    rv = client.get('/logout')
    assert b'logged out' in rv.data


def test_logout_noone_loggedin(client):
    rv = client.get('/logout', follow_redirects=True)
    assert b'Login' in rv.data


### SEARCH ###

# User not logged in
def test_search_not_loggedin(client):
    rv = client.get('/logout')
    rv = client.get('/search', follow_redirects=True)
    assert b'Login' in rv.data

def test_search_login(client):
    assert b'Search' in login(client, "admin", "123").data


def search_db(client, isbn="", title="", author=""):
    """Wrapper function to test search feauture.

    Args:
        isbn: String representing book's isbn.
        title: String representing book's title.
        author: String representing book's author.

    Returns:
        rv: object containing response from posted request
    """
    route_start = '/search-results'
    route_args = f'?isbn={isbn}&title={title}&author={author}'

    rv = client.get(route_start + route_args, follow_redirects=True)

    return rv


def test_search_fields_empty(client):
    assert b'Search error' in search_db(client).data

def test_search_only_isbn(client):
    assert b'number9dream' in search_db(client,
                                        isbn="08129",
                                        title="",
                                        author="").data

def test_search_only_title(client):
    assert b'Mitchell' in search_db(client,
                                        isbn="",
                                        title="9drea",
                                        author="").data


def test_search_only_author(client):
    assert b'number9dream' in search_db(client,
                                        isbn="",
                                        title="",
                                        author="Mitchell").data

def test_search_only_all(client):
    assert b'number9dream' in search_db(client,
                                        isbn="08129",
                                        title="number9dream",
                                        author="Mitchell").data

def test_search_noresults(client):
    assert b'No matches found' in search_db(client,
                                        isbn="-4454jfdg",
                                        title="number9dream",
                                        author="Mitchell").data

### Book page ###
# Accessing a book page when not logged in
def test_book_notloggedin(client):
    rv = client.get('/logout')
    rv = client.get('/book/1', follow_redirects=True)
    assert b'Login' in rv.data

# Accessing a book page when logged in
def test_book_login(client):
    login(client, "admin", "123")
    rv = client.get('/book/1', follow_redirects=True)
    assert b'Krondor' in rv.data

# Accessing a book page for an illegal id
def test_book_illegal_id(client):
    login(client, "admin", "123")
    rv = client.get('/book/5002', follow_redirects=True)
    assert b'Error' in rv.data

# Accessing route /book without id; redirect back to search page
def test_book_no_id(client):
    login(client, "admin", "123")
    rv = client.get('/book', follow_redirects=True)
    assert b'Search' in rv.data

# Submitting a review, no other reviews written
# YOU CAN ONLY DO THIS ONCE!!
# def test_review_first_time(client):
#     login(client, "admin", "123")
#     rv = client.post('/book/3/review', data=dict(
#         reviewtext="Rad read!!",
#         rating="5"
#     ), follow_redirects=True)



# Submitting a review when user has already written one
def test_review_already_submitted(client):
    login(client, "admin", "123")
    rv = client.post('/book/1/review', data=dict(
        reviewtext="I read it again!! Amazing",
        rating="5"
    ), follow_redirects=True)
    assert b'Error' in rv.data


# Submitting a review with blank fields
def test_review_blank_data(client):
    login(client, "admin", "123")
    rv = client.post('/book/4999/review', data=dict(
        reviewtext="",
        rating=""
    ), follow_redirects=True)
    assert b'Unable to add review to database' in rv.data


# Submitting review with illegal rating value
# Test does not work because 'required' attribute in input tags
# prevents illegal values from being posted in the first place
# def test_review_illegal_rating(client):
#     login(client, "admin", "123")
#     rv = client.post('/book/4999/review', data=dict(
#         reviewtext="Great book!",
#         rating="6"
#     ), follow_redirects=True)
#     assert b'Rating is not an integer between 1 and 5' in rv.data

# Submitting a non-integer value between 1 and 5
# idem: type attribute ensures only integers passed
# def test_review_decimal_rating(client):
#     login(client, "admin", "123")
#     rv = client.post('/book/4/review', data=dict(
#         reviewtext="The BOMB!!",
#         rating="4.56789"
#     ), follow_redirects=True)
#     assert b'Unable to add review to database' in rv.data


### API ###

# Invalid isbn; test for status code
def test_api_bad_isbn(client):
    login(client, "admin", "123")
    isbn = "dsgkdfgkjfgkjdfhg"
    rv = client.get(f"/api/{isbn}")
    json_data = json.loads(rv.data)

    assert "Invalid ISBN." == json_data['error']
    assert rv.status_code == 404

# Valid Isbn, no reviews
def test_api_goodisbn_no_reviews(client):
    login(client, "admin", "123")
    isbn = "0553803700"
    rv = client.get(f"/api/{isbn}")
    json_data = json.loads(rv.data)

    assert "Isaac Asimov" == json_data['author']
    assert 0 == json_data['average_score']
    assert 0 == json_data['review_count']


# Need to run INSERT statements found in schema.sql to run this test
# successfully
# Valid isbn, one or more reviews 0380795272
# def test_api_goodisbn_reviews(client):
#     login(client, "admin", "123")
#     isbn = "0380795272"
#     rv = client.get(f"/api/{isbn}")
#     json_data = json.loads(rv.data)
#
#     assert "Raymond E. Feist" == json_data['author']
#     assert 2.5 == json_data['average_score']
#     assert 2 == json_data['review_count']
