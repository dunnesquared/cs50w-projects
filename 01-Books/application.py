"""Supports features and database access for Bookr website"""
import os

import requests
from flask import Flask, session, render_template, jsonify, request, url_for, redirect
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_session import Session

# Goodreads API key
KEY = "DO NOT WRITE YOUR API KEY!"

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html", user_name=session.get('user_name', None))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Displays form that new user needs to fill out to register for website;
    Adds new user to database to access site."""

    if request.method == 'GET':
        return render_template("register.html",
                                message=None,
                                user_name=session.get('user_name', None))

    if request.method == 'POST':
        # Get form data
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        # Ensure not getting strings made up of whitespaces
        # Should never see this message if JavaScript enabled on client browser
        if len(username) == 0 or len(password) == 0:
            message = "Unable add user to database: username/password field empty."
            return render_template("error.html",
                                    message=message,
                                    user_name=session.get('user_name', None))

        # Insert username into database
        try:
            # Check to see that username is not already taken
            if db.execute("SELECT * FROM users WHERE name = :name",
                          {"name": username}).rowcount > 0:

                message = f"Username '{username}' all ready in use. \
                            Please choose another name."

                return render_template("register.html",
                                        message=message,
                                        user_name=session.get('user_name', None))


            # Insert username and password
            db.execute("INSERT INTO users (name, password) VALUES (:name, :password)",
                        {"name": username, "password": password})

            # Ensure new data is actually saved to db
            db.commit()

            message = f"Registration complete! Welcome to Rook Beview, {username}!"
            return render_template("success.html",
                                    message=message,
                                    user_name=session.get('user_name', None))

        except exc.SQLAlchemyError as err:
            return "SQLAlchemy Error: {0}".format(err)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Logs user into website."""

    if request.method == "GET":
        return render_template("login.html",
                                message=request.args.get('message'),
                                user_name=session.get('user_name', None))

    if request.method == "POST":
        # Create a session variable to track if user logged in if no such
        # variable exists yet.
        if session.get('logged_in') is None:
            session["logged_in"] = False

        # Get form data
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        # Ensure not getting strings made up of whitespaces
        # Should never see this message if JavaScript enabled on client browser
        if len(username) == 0 or len(password) == 0:
            message = "Unable to complete login: username/password field empty."
            return render_template("error.html",
                                    message=message,
                                    user_name=session.get('user_name', None))


        # Check user credentials
        users = db.execute("SELECT * FROM users WHERE name = :name AND password = :password",
                       {"name": username, "password": password}).fetchall()

        if len(users) != 1:
            message = "Incorrect user name or password."
            return render_template("login.html",
                                    message=message,
                                    user_name=session.get('user_name', None))

        # Log user in; keep track of id for later processing
        session['logged_in'] = True
        session['user_id'] = users[0].id
        session['user_name'] = users[0].name
        message = f"Login successful! Welcome {users[0].name}!"
        return redirect(url_for("search",
                                login_confirmation=message,
                                user_name=session.get('user_name', None)))


@app.route("/logout")
def logout():
    """Logs user out of current session."""

    # Check to see whether session variable exists
    if session.get("logged_in") is None:
        message = "Please login first if you wish to logout ;-)."
        return redirect(url_for("login",
                                message=message,
                                user_name=session.get('user_name', None)))

    # Logout user; clear session variables
    user_name = session.get("user_name")

    session.pop("logged_in", None)
    session.pop("user_id", None)
    session.pop("user_name", None)

    message = f"User {user_name} successfully logged out."
    return render_template("success.html",
                            message=message,
                            user_name=session.get('user_name', None))


@app.route("/search")
def search():
    """Displays page where user can search for book."""

    # Need to check if logged in before rendering page
    if session.get('logged_in') is None:
        message = "You must login before you can search for a book."
        return redirect(url_for("login",
                                message=message,
                                user_name=session.get('user_name', None)))

    # Let user she has logged in succesfully if coming straight from
    # login page
    if request.args.get('login_confirmation') is not None:
        login_confirmation = request.args.get('login_confirmation')
    else:
        login_confirmation = None

    return render_template("search.html",
                            login_confirmation=login_confirmation,
                            message=None,
                            user_name=session.get('user_name', None))


@app.route("/search-results")
def search_results():
    """Processes search criteria; renders results page"""

    # Check for empty fields; at least one musth have data
    isbn = request.args.get("isbn")
    title = request.args.get("title")
    author = request.args.get("author")

    # Empty fields don't return empty strings like ""
    if isbn is None:
        isbn = ""
    if title is None:
        title = ""
    if author is None:
        author = ""

    # Don't want blank spaces messing up queries
    isbn, title, author = isbn.strip(), title.strip(), author.strip()

    # Ensure not getting strings made up of whitespaces
    # Should never see this message if JavaScript enabled on client browser
    if len(isbn) == 0 and len(title) == 0 and len(author) == 0:
        message = "Search error: No search criteria specified."
        return render_template("error.html",
                                message=message,
                                user_name=session.get('user_name', None))

    # Search database
    # Use LOWER function to make title and author searches case-insensitive
    books = db.execute("SELECT * FROM books WHERE \
                        (isbn LIKE :isbn AND \
                        LOWER(title) LIKE LOWER(:title) AND  \
                        LOWER(author) LIKE LOWER(:author))",
                        { "isbn": "%" + isbn + "%" ,
                          "title": "%" + title + "%",
                          "author": "%" + author + "%"}).fetchall()

    # Customize message depending whether any results found or not
    if books:
        if len(books) > 1:
            message = f"{len(books)} matches found!"
        else:
            message = "One match found."
    else:
        message = "No matches found."

    return render_template("search-results.html",
                            books=books,
                            message=message,
                            user_name=session.get('user_name', None))


@app.route("/book")
def go_back_to_search():
    """Brings user back to search if the above route specified in url"""
    return redirect(url_for("search",
                            message=None,
                            user_name=session.get('user_name', None)))


@app.route("/book/<int:book_id>")
def book(book_id):
    """Displays book details, user reviews Goodreads review data,
    and a form for the user to submit a review.

    Args:
        book_id: Integer representing id number of book in database.
    """

    # Need to check if logged in before rendering page
    if session.get('logged_in') is None:
        message = "You must login before you can see book details."
        return redirect(url_for("login", message=message,
                                user_name=session.get('user_name', None)))

    # Get basic book info from project db
    book = db.execute("SELECT * FROM books \
                       WHERE id = :book_id",
                       {"book_id": book_id}).fetchone()

    if not book:
        message = "Book id does not exist."
        return render_template("error.html",
                                message=message,
                                user_name=session.get('user_name', None))

    # Get Goodreads data
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                        params={"key": KEY, "isbns": book.isbn})

    # The dict we want is encapsulated in a list inside a dict; not sure why...
    goodreads_data = res.json()
    goodreads_data  = goodreads_data['books'][0]

    # Get any reviews written for book and the name of each review's author
    reviews = db.execute("SELECT opinion, rating, name, user_id FROM reviews \
                        JOIN users ON reviews.user_id = users.id \
                        WHERE book_id = :book_id ",
                        {"book_id": book_id}).fetchall()

    # Check whether user has written review for this book already
    user_ids = [review.user_id for review in reviews]
    wrote_review = session.get('user_id') in user_ids

    return render_template("book.html",
                            book=book,
                            goodreads_data=goodreads_data,
                            reviews=reviews,
                            wrote_review=wrote_review,
                            user_name=session.get('user_name', None))


@app.route("/book/<int:book_id>/review", methods=['GET', 'POST'])
def review(book_id):
    """ Processes book review submitted by user; prevents user from submitting
    review twice.
    """

    # Check that user is logged before submitting review
    if session.get('logged_in') is None:
        message = "You must login before you can submit a review."
        return redirect(url_for("login",
                                message=message,
                                user_name=session.get('user_name', None)))

    # Double-check book-id to make sure it's valid.
    # N.B. Should never be executed so long as method post used to submit
    # reviews
    bookid_okay = db.execute("SELECT * FROM books where id = :book_id",
                                {"book_id": book_id}).fetchone()
    if bookid_okay is None:
        message = "Invalid book id; submission of review denied."
        return render_template("error.html", message=message,
                                user_name=session.get('user_name', None))

    # In case user refreshes url after submission
    if request.method == 'GET':
        return redirect(url_for('book', book_id=book_id,
                                user_name=session.get('user_name', None)))

    # Check to ensure user has not already submitted a review for this book
    wrote_review = db.execute("SELECT * FROM reviews \
                               WHERE book_id = :book_id \
                               AND user_id = :user_id",
                               {"book_id": book_id,
                               "user_id": session.get('user_id')}).rowcount

    if wrote_review:
        message = "You've already written a review for this book."
        return render_template("error.html",
                                message=message,
                                user_name=session.get('user_name', None))


    # First-time reviewer. Go ahead and add it to the db
    reviewtext = request.form.get('reviewtext').strip()
    rating = request.form.get('rating')

    # Ensure not getting strings made up of whitespaces
    # Should never see this message if JavaScript enabled on client browser
    if len(reviewtext.strip()) == 0 or len(rating.strip()) == 0:
        message = "Unable to add review to database: opinion/rating fields empty."
        return render_template("error.html",
                                message=message,
                                user_name=session.get('user_name', None))

    # Don't insert illegal ratings in to database
    if int(rating) < 1 or int(rating) > 5:
        message = "Rating is not an integer between 1 and 5. Submission of \
                   review denied"
        return render_template("error.html",
                                message=message,
                                user_name=session.get('user_name', None))


    db.execute("INSERT INTO reviews \
                (opinion, rating, book_id, user_id) \
                VALUES (:opinion, :rating, :book_id, :user_id )",
                { "opinion":reviewtext,
                  "rating": rating,
                  "book_id": book_id,
                  "user_id": session.get('user_id')})

    db.commit()

    message = f"Thank you for your book review!"
    return render_template("success.html",
                            message=message,
                            user_name=session.get('user_name', None))

@app.route("/api/<isbn>")
def book_api(isbn):
    """Returns JSON object containing details of book as per ISBN"""

    # Check that user is logged before submitting review
    if session.get('logged_in') is None:
        message = "You must login before you can access the API."
        return redirect(url_for("login",
                                message=message,
                                user_name=session.get('user_name', None)))

    # Ensure that isbn is valid; plus get all its info
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn",
                      {"isbn": isbn}).fetchone()

    if book is None:
        return jsonify({"error": "Invalid ISBN."}), 404

    reviews = db.execute("SELECT rating FROM reviews \
                               WHERE book_id = :book_id",
                               {"book_id": book.id}).fetchall()

    # Get number of reviews for book and the averagg rating
    review_count = len(reviews)
    avg_score = 0

    if review_count > 0:
        ratings = [review.rating for review in reviews]
        avg_score = round(sum(ratings)/review_count, 1)

    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn,
        "review_count": review_count,
        "average_score": avg_score
    })


@app.route("/debug")
def debug():
    """Debugging Flask handler method"""

    # Print all users and their passwords
    users = db.execute("SELECT * FROM users").fetchall()

    result = "<p>USERS</p><ul>"
    for user in users:
        result += f"<li>{user.id}: ({user.name}, {user.password})</li>"

    result += "</ul>"

    if session.get("logged_in") is not None and session.get("logged_in") == True:
        result += f"<p>Current user logged in: {session['user_id']}</p>"
    else:
        result += f"<p>No-one currently logged-in.</p>"

    return result
