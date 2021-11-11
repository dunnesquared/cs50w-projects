# Project 1

Web Programming with Python and JavaScript

## Books

To meet the requirements of Project 1, I created `Bookr`. `Bookr`
is a responsive website that allows registered users to get basic information
about books from the site's database. The site also provides rating data from
Goodreads.com via that  site's API. `Bookr` users can also rate and write
reviews for books. Developers can get book information as a JSON object via
`Bookr`'s own API. Both users and developers must be logged-in to access
these features.

## To run `Bookr` on your machine
Assuming PostgreSQL and Flask are setup correctly, first run `schema.sql` to
create the tables `users`, `books` and `reviews`. If you are working with
PostgreSQL via the console this can be easily done by running the command

```sh
\i schema.sql
```

Next, run the Python script that will import book data into the database.

```sh
python3 import.py
```


## Files

### `static/credentials.js, static/review.js, static/review.js`
All the JavaScript files above provide extra-checking of input when the
user is registering, logging-in, searching for a book or writing a review.
While the checked fields in each script maybe different, they generally serve the
same purpose: ensuring that users cannot submit the form until the necessary
fields have been filled with non-whitespace characters. In the case of
registering and logging-in, both username and passwords fields need to be
filled before form submission is allowed. In the case of searching for a book,
only one of the fields needs to be filled. For reviewing a book, the text-area
for the written review and the number rating field must be filled out.


### `static/style.css`
While the site heavily relies on Bootstrap 4 classes, this file contains
any extra stylings needed to improve the look of the site.


### `templates\*.html`
The pages that make up the website are found in this folder. Rendering is
accomplished using Flask and Jinja2 template code. Features shared across
all the pages, such as the responsive navigation bar, are found in
`layout.html`. Many pages have conditional statements that will display
an alert message should the server pass one. Bootstrap 4 CSS classes and
Javascript libraries are used throughout the HTML pages to give the site
a clean and modern look.

### `tests/test_application.py`
A unit test script that tests site features implemented in `application.py`.
To run the tests, please install `pytest` first. Once done, the script
can be run from the root of the project directory by simply typing `pytest` on
the console.

### `application.py`
The 'heart' of the website. It is here that all the business logic,
database access, rendering and redirecting of site pages is implemented.
The name of the routes in `application.py` describe their namesake features.

* `/register`: Handle user registration; prevent user from registering with a username that's already been taken.
* `/login`: Login a registered user. Refuse access if username or password is incorrect. If users try to search for a book, see book details, etc. before logging-in, redirect to the login page.
* `/search`: Let users search for a book using ISBN, book title or author.
* `/search-results`: Display unordered list of results, if any.
* `/book/<int:book_id>`: Display book details as well as data pulled from Goodreads; present form for users to write a review and leave a rating. Don't allow user to do this if user has already reviewed the book.
* `/api/<isbn>`: Return JSON object containing book information. Returns error message in JSON object if isbn is not in the database or user is not logged in.

### `import.py`
Python script that imports data from `books.csv`. If the table `books` does
not yet exist in the database, the script will alert the user accordingly and
end.

### `schema.sql`
An SQL script that creates the tables required for `Bookr` to store and
insert data. This script must be run before book data is imported using
`import.py`. Two fictional users are inserted into the database via this
script for testing and demonstration purposes.

## Warning!
`Bookr` uses a naive implementation for its registration and login features:
it does not hash user passwords, but stores them as plain text in the database.
Consequently, `Bookr` can easily be hacked and should not be deployed
for use in the real world with real users. Use `Bookr` for learning and
teaching purposes only.
